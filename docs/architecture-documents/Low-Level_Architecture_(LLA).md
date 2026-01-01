# Low-Level Architecture (LLA)

## 2️⃣ Low-Level Architecture (LLA)

Now let’s go concrete: objects, flows, and logic.

---

### A. Data Models (simplified)

**Request DTO (internal)**

```json
{
"request_id":"uuid",
"channel":"email",
"user_id":"john.doe@company.com",
"subject":"Password reset ASAP",
"text":"I'm locked out of my workstation and need a new password",
"raw_metadata":{
"email_message_id":"...",
"received_at":"2026-01-02T10:15:00Z"
}
}

```

**Agent Output DTO**

```json
{
"request_id":"uuid",
"intent":"password_reset",
"confidence":0.86,
"actions_taken":[
{
"type":"KB_LOOKUP",
"success":true,
"details":{"policy_id":"pw-reset-remote-001"}
},
{
"type":"SNOW_USER_LOOKUP",
"success":true,
"details":{"user_sys_id":"abc123"}
},
{
"type":"SNOW_TICKET_CREATE",
"success":true,
"details":{"incident_number":"INC0012345"}
}
],
"final_user_message":"Hi John, I’ve created a password reset ticket INC0012345 following the remote reset policy. You’ll receive a separate message with reset instructions or a call from IT.",
"needs_handoff":false
}

```

**DB Tables (minimum)**

- `conversations`
    - `id`, `user_id`, `created_at`, `last_intent`, `last_updated_at`
- `messages`
    - `id`, `conversation_id`, `role` (user/agent), `content`, `created_at`
- `actions_log`
    - `id`, `request_id`, `action_type`, `payload_json`, `success`, `created_at`
- `metrics_daily`
    - `date`, `total_requests`, `auto_resolved`, `escalated`, `avg_confidence`

---

### B. Agent Orchestrator: UPRA in Code Terms

Think of `AgentOrchestrator.handle_request(request: AgentRequest)` doing:

1. `understanding = IntentEngine.classify(request.text)`
2. `plan = Planner.build_plan(understanding, request)`
3. `context = Retriever.enrich(plan, request)`
4. `result = Actor.execute(plan, context)`
5. `validated_result = Validator.check(result, context)`
6. `Telemetry.log(...)`
7. return `validated_result`

---

### C. “Understand” – How It Works

**Inputs:**

- `text` (“I’m locked out…”)
- optional history

**Steps:**

1. **Rule Pre-Pass**
    - Quick regex / keyword:
        - if text contains {“password”, “reset”, “locked out”} → candidate: `password_reset`
2. **LLM Classification Call**
    
    Prompt example:
    
    > “Classify this IT helpdesk request into one of: [password_reset, account_unlock, access_request, knowledge_question, unknown].
    > 
    > 
    > Return JSON with fields: intent, confidence (0–1), entities (user, system, urgency).”
    > 
3. **Merge & Threshold Logic**
    - If LLM `intent=password_reset` and confidence ≥ 0.7 AND rules agree → accept.
    - Else if confidence 0.4–0.7 → maybe ask a clarifying question in reply.
    - Else → treat as generic helpdesk / knowledge question.

**Output example:**

```json
{
"intent":"password_reset",
"confidence":0.82,
"entities":{
"system":"AD",
"urgency":"high"
}
}

```

---

### D. “Plan” – Execution Strategy Object

Planner takes `{intent, confidence, entities}` and builds a list of steps.

For `password_reset`:

```json
{
"intent":"password_reset",
"steps":[
"VERIFY_IDENTITY",
"FETCH_POLICY_FOR_CONTEXT",
"CHECK_USER_STATE_IN_SNOW",
"DECIDE_AUTOMATION_ELIGIBILITY",
"EXECUTE_RESET_OR_CREATE_TICKET",
"CONFIRM_AND_NOTIFY"
]
}

```

Key behaviours:

- If confidence < 0.7 → insert `ASK_CLARIFICATION` before `VERIFY_IDENTITY`.
- If entity `system` is unknown → insert `ASK_SYSTEM_TYPE` (VPN, AD, email, etc.).

---

### E. “Retrieve” – RAG + System Lookups

**1. RAG Policy Retrieval**

Given `intent=password_reset` and maybe `context=remote_user`:

- Query vector store:
    
    > “password reset policy remote employees MFA”
    > 
- Get top policy docs:
    - `pw_reset_remote_policy`
    - `mfa_requirements`
- Extract:
    - MFA required?
    - Allowed channels?
    - Any blacklisted scenarios?

**2. ServiceNow Lookups**

- Find user:
    - `GET /api/now/table/sys_user?email=john.doe@company.com`
- Get current state:
    - attributes like `locked_out`, `active`, `vip_flag`, etc.

**3. Combine Into a Context Object**

```json
{
"policy":{
"requires_mfa":true,
"mfa_channel":"sms",
"allow_auto_reset":true
},
"user_record":{
"sys_id":"abc123",
"active":true,
"phone":"+1-555-123-4567",
"is_vip":false
}
}

```

---

### F. “Act” – Tools + Validation

Based on plan & context:

1. **Identity / MFA**
    - Using SNOW Notify or mock:
        - Generate OTP
        - Send SMS or email
        - Wait for user reply ⇒ verified / failed
2. **Decision**
    - If `verified && policy.allow_auto_reset`:
        - Call reset script:
            - `POST /api/now/table/x_password_reset` (or a mock endpoint)
    - Else:
        - Create incident:
            - `POST /api/now/table/incident`
                - `short_description`: “Password reset request – MFA failed or not eligible”
                - `description`: include email text + context
3. **Validation**
    - Confirm `HTTP 2xx` and a valid `incident_number` or `status=SUCCESS`
    - If call fails:
        - Log failure
        - Fall back to: “We’ve created an incident for IT to help you.”
4. **Compose Final Answer**
    - Natural language summary of:
        - What was done (ticket, reset, MFA, etc.)
        - What user will see next (email / SMS / call)
    - Include ticket number if created.

---

### G. Email Integration – Low-Level

**Inbound:**

- Cron job every 30s checks IMAP for new unread emails to `helpdesk-ai@…`
- For each new message:
    - Parse sender as `user_id`
    - Subject + body → `text`
    - Call backend `/inbound/email`
    - Store original message ID.

**Outbound:**

- Backend gets `final_user_message`
- Uses SMTP or SendGrid-style API:
    - `to = user_id`
    - `in-reply-to` = original message ID
    - Subject: `Re: [AI Helpdesk] Password reset request`

> “Channel-agnostic, but I implemented the first channel as email — so this demonstrates orchestration between email, AI, and ServiceNow.”
> 

---

### H. Security & Governance (Low-Level Points)

You can list:

- No credentials or reset tokens are ever sent to LLM.
- LLM sees:
    - abstracted policy text,
    - anonymized user info (e.g., `user_123`) for reasoning.
- ServiceNow credentials handled via:
    - environment variables,
    - service account,
    - HTTPS.
- Logs:
    - contain `request_id`, not full secrets.
- Role-based:
    - Only a service account with limited rights can execute reset / create incidents.

---

### I. Metrics & Observability

Minimum:

- Log each request with:
    - `intent`
    - `confidence`
    - `auto_resolved` flag
    - `needs_handoff` flag
- Simple daily aggregate query:
    - success rate
    - escalation rate
    - average response time