# Enterprise Autonomous Agent with Multi-Pass Re-Act Orchestration
https://www.notion.so/Enterprise-Autonomous-Agent-with-Multi-Pass-Re-Act-Orchestration-2dfbffd79b4680d29302f7cf966a7e52?source=copy_link

- [Enterprise Autonomous Agent with Multi-Pass Re-Act Orchestration](#enterprise-autonomous-agent-with-multi-pass-re-act-orchestration)
- [🚀 VeeBee: Autonomous Enterprise Service Agent](#-veebee-autonomous-enterprise-service-agent)
  - [**🛠️ Tech Stack**](#️-tech-stack)
  - [🧠 Key Engineering Highlights:](#-key-engineering-highlights)
    - [1. The Autonomous "Second Pass" (Re-Act)](#1-the-autonomous-second-pass-re-act)
    - [2. Deterministic Guardrails via ServiceNow](#2-deterministic-guardrails-via-servicenow)
    - [3. Modular "`Document-as-Code`" Scaling](#3-modular-document-as-code-scaling)
- [**🎬 DEMO: HAPPY PATH**](#demo-happy-path)
  - [**`0:00 - 2:00` | SNOW PDI Env. \& Intent Engine**](#000---200--snow-pdi-env--intent-engine)
  - [**`2:00 - 2:29` | The Re-Act Loop (The Star):**](#200---229--the-re-act-loop-the-star)
  - [**`2:30 - 2:45` | Planner Agent *choosing* Policy + Procedure based of Results:**](#230---245--planner-agent-choosing-policy--procedure-based-of-results)
  - [**`2:45 - 3:45` | Automated Dispatch \& Closing the Loop:**](#245---345--automated-dispatch--closing-the-loop)
- [**🎬 DEMO: Lack of Document in KB —\> Knowledge Response**](#demo-lack-of-document-in-kb--knowledge-response)
  - [**`0:00 - 1:00`** | **Natural Language Request + Await IMAP Trigger:**](#000---100--natural-language-request--await-imap-trigger)
  - [**`1:50 - 2:50`**: **`Email Response` from Bot + `Incident Creation` in SNOW**:](#150---250-email-response-from-bot--incident-creation-in-snow)
- [🏗️ CURRENT ARCHITECTURE](#️current-architecture)
    - [**TO BE DOCUMENTED …**](#to-be-documented-)
- [🎯 FUTURE ARCHITECTURE + Improvements](#future-architecture--improvements)
    - [**TO BE DOCUMENTED …**](#to-be-documented--1)
- [🧱 Building Journey:](#building-journey)
  - [**TO BE DOCUMENTED …**](#to-be-documented--2)
    - [**GITHUB URL: { COMMIT HISTORY}**](#github-url--commit-history)
    - [`Day 1 (Sunday **Dec 28, 2025**)`: Planning / Architecture, etc …](#day-1-sunday-dec-28-2025-planning--architecture-etc-)
    - [`Day 2:(Monday **Dec 29, 2025)`:\*\* SNOW PDI Setup + Curls…](#day-2monday-dec-29-2025-snow-pdi-setup--curls)
    - [`Day 3: (Tuesday **Dec 30, 2025)`:\*\* Vector DB Local Install + Chunking Strategy.](#day-3-tuesday-dec-30-2025-vector-db-local-install--chunking-strategy)
    - [`Day 4: (Wednesday **Dec 31, 2025)`:\*\* Agentic Backend Foundation.](#day-4-wednesday-dec-31-2025-agentic-backend-foundation)
    - [`Day 5: (Thursday Jan 1, 2026)`: Agentic Backend Foundation + Initial Intent Engine](#day-5-thursday-jan-1-2026-agentic-backend-foundation--initial-intent-engine)
    - [`Day 6-8: (Fri, Jan 2 - Sun, Jan 4, 2026)`: Improve Intent Engine + Initial RAG → Evolve to ReAct + Dispatcher ( SNOW API Action + Email Inbound \& Outbound)](#day-6-8-fri-jan-2---sun-jan-4-2026-improve-intent-engine--initial-rag--evolve-to-react--dispatcher--snow-api-action--email-inbound--outbound)


---

# 🚀 VeeBee: Autonomous Enterprise Service Agent

**An Intelligent Orchestrator bridging Natural Language and IT Service Management (ServiceNow).**

VeeBee is an autonomous AI agent designed to automate enterprise workflows (like password resets and policy inquiries) while maintaining 100% adherence to corporate security protocols. Unlike standard "black-box" chatbots, VeeBee utilizes a **multi-pass Re-Act (Reasoning and Acting) loop** to validate user identity via ServiceNow and cross-reference requests against a local Knowledge Base before taking action.

It transforms static Standard Operating Procedures (SOPs) into executable logic, providing a scalable, "Document-as-Code" approach to IT automation.

## **🛠️ Tech Stack**

- **Orchestration:** `Python` / `FastAPI`.
- **Reasoning:** `OpenAI` / `Llama-3` (via local ) using a custom **Re-Act** (Reasoning + Acting) loop.
- **Vector Engine:** `ChromaDB` (Local) storing Markdown-based SOPs.
- **Enterprise Integration:** `ServiceNow API (REST).`
- **Messaging:** `IMAP` (Gmail Listener) & `SMTP` (Secure Dispatcher).

## 🧠 Key Engineering Highlights:

### 1. The Autonomous "Second Pass" (Re-Act)

Instead of a simple "top-k" RAG lookup, I implemented a **`Reasoning Loop`**. If the first retrieval doesn't meet a specific confidence threshold, The **`LLM generates a refined search query.`** This "Second Pass" ensures the agent actually finds the *Procedure* before it attempts an *Action*.

### 2. Deterministic Guardrails via ServiceNow

The agent doesn't just "act"; it validates. By pulling the **User State** from ServiceNow in real-time, the agent cross-references the user's `account_status` and `vip_status` against corporate **Policies**.

### 3. Modular "`Document-as-Code`" Scaling

The system is built for modularity. To expand the agent's skills, you don't rewrite code; you simply add a new `.md` procedure file to ChromaDB. 

The agent discovers the new capability via  search and executes it using the existing dispatcher.

---

# **🎬 DEMO: HAPPY PATH**

[view?usp=sharing](https://drive.google.com/file/d/1NlTznpIYZ_tZ9A9CjM1anGQad-3I3NCp/view?usp=sharing)

## **`0:00 - 2:00` | SNOW PDI Env. & Intent Engine**

- **PDI + Email Compose**: ServiceNow PDI Environmental working & Successful Login + Composed email to Agent.
- **Input & Intent:** Show the email hitting the listener.
    - Highlight the:
        - **Intent Engine** extracting "Password Reset” request.
        - Call to ServiceNow API for user validation + Prepped User State for AI.
        

## **`2:00 - 2:29` | The Re-Act Loop (The Star):**

- Initial Rag Query based of user state & email- (”`*Policy for active user*`”)
- Retrieved Results not very relevant due to score.(”`*Score: 1.1893*`”)
- High RAG Score, makes LLM realize that it needs more info and triggers the **Second Pass RAG - with a better query**. “`*Policy / Procedure for password_reset specific query*`”
- Receive relevant results with better score.
    
    ```jsx
    -> Score: 0.5544 | Type: policy | Snippet: # Password Reset Operations Policy...
    -> Score: 0.8766 | Type: policy | Snippet: - **Allowed**: Automated reset is permitted if `ac...
    -------------------------------
    
    --- RETRIEVAL DEBUG: Procedure for password_reset specific query ---
    -> Score: 0.7075 | Type: None | Snippet: # Password Reset – Standard Procedure
    ```
    

## **`2:30 - 2:45` | Planner Agent *choosing* Policy + Procedure based of Results:**

- Result passed to `Planner (LLM Powered)`, which based of Retrieval uses the Policy & Procedure.

```jsx
DEBUG: Raw LLM Decision String: {
    "policy_id": "Password Reset Operations Policy",
    "procedure_id": "PASSWORD_RESET_STANDARD",
    "steps": ["VERIFY_IDENTITY", "CREATE_INCIDENT", "RESET_PASSWORD", "CLOSE_INCIDENT", "NOTIFY_USER"],
    "confidence_score": 0.70748836
}
Plan Generated: {'policy_used': 'Password Reset Operations Policy', 'procedure_used': 'PASSWORD_RESET_STANDARD', 'steps': ['VERIFY_IDENTITY', 'CREATE_INCIDENT', 'RESET_PASSWORD', 'CLOSE_INCIDENT', 'NOTIFY_USER'], 'agent_was_curious': False}
```

## **`2:45 - 3:45` | Automated Dispatch & Closing the Loop:**

- The "`Password Reset`" email arriving back in the inbox with the `temporary password` and `ticket number`.
- SNOW Login Failed, because of Password being Reset.
- Reset Password throw PDI Dashboard & Login.
- Show the Incident creation in ServiceNow.

---

# **🎬 DEMO: Lack of Document in KB —> Knowledge Response**

[view?usp=sharing](https://drive.google.com/file/d/1unzQSzbmjt8SIJ0t6eZAzpJjeuYQmfKS/view?usp=sharing)

## **`0:00 - 1:00`** | **Natural Language Request + Await IMAP Trigger:**

- **The Trigger:** A natural language email is sent to the agent's listener, and awate the email reader to fetch the email.
- Show routes Agent Backend Offers.
- **1:00 - 1:50** | **Trigger → Intent → Retrieval | ReAct, choosing Policy & Procedure.**
    - Once email is caught, Intent Engine is able to make out its a knowledge Question.
    
    ```jsx
    {
        "intent": "knowledge_question",
        "urgency": "low",
        "system": "AD",
        "confidence": 0.9
    }
    ```
    
    - Based of Intent , initial Query to Vector DB which returned low relevance because of high distance “`*Score: 1.1893*`” .
    - Which is signal for Second Pass to Vector DB with a **`AI Generated Query`** for Vector DB, however retrieved procedure was not good enough, hence went to fallback.

```jsx
DEBUG: Agent requested search for: password strength company policy

--- RETRIEVAL DEBUG: Policy for password strength company policy ---
-> Score: 0.6523 | Type: policy | Snippet: # Password Reset Operations Policy...
-> Score: 1.1374 | Type: policy | Snippet: IF user_state.vip_status == True:
    - ACTION: RE...
-------------------------------

--- RETRIEVAL DEBUG: Procedure for password strength company policy ---
-> Score: 0.9328 | Type: None | Snippet: # Password Reset – Standard Procedure

## Descript...
-> Score: 1.3552 | Type: None | Snippet: # Knowledge-Only Response Procedure

## Descriptio...
-------------------------------

⚠️ No highly relevant procedures found (Best score > 0.9). Overriding with Fallback.
```

- Based on the Fallback plan, choose the Plan to be executed + Observed `ServiceNow API call` + `Email Outbound Call` executed by the Dispatcher.

```jsx
Plan Generated: {'policy_used': 'GENERAL_SECURITY_POLICY', 'procedure_used': 'UNKNOWN_INTENT_PROCEDURE', 'steps': ['CREATE_INCIDENT', 'GENERATE_KNOWLEDGE_RESPONSE', 'SEND_EMAIL_RESPONSE'], 'agent_was_curious': True, 'confidence': 0.9}

DEBUG: (SNOW API Call) Client Initialized for https://dev249455.service-now.com with user admin
DEBUG: (SNOW API Call) Client Initialized for https://dev249455.service-now.com with user admin
```

## **`1:50 - 2:50`**: **`Email Response` from Bot + `Incident Creation` in SNOW**:

- Navigated to email, and saw an email response from Bot.
- Navigated to SNOW Incident and saw the freshly created incident.

---

# 🏗️ CURRENT ARCHITECTURE + Challanges

### **TO BE DOCUMENTED …**

HAD TO PIVIT FROM **INITIAL PLAN (URL of initial Plans: [docs](https://github.com/virensachdev786/enterprise-agentic-platform/tree/master/docs))** TO MAINTAIN MOVEMENTUM.

LOTS OF CHALLANGES: **TO BE DOCUMENTED**

---

# 🎯 FUTURE ARCHITECTURE + Improvements

### **TO BE DOCUMENTED …**

High Level Idea without looking at notes: 

- `Logging` via SQL Database for traceability.
- `Better Prompts` for better System reliability + Fallback in Prompts.
- Better Knowledge with Tags (This will cover Feedback Loop)
- Send Temp pass on Phone instead of Email + MFA in flow.
- `API idempotency`
- Making the Agent `Conversational`.
- Make all Variables configurable through `config,py` + `.env`
- `Dockerize` + write a `requirements.txt` for needed libraries
- Improve the `core` & put the code into sub folders of `Understand` (`Intent`) + `Plan` + `Retrieve` (`Re-Act`) + `Act` (`Dispatcher`)
- ETC. ……

---

# 🧱 Building Journey:

## **TO BE DOCUMENTED …**

### **GITHUB URL: { [COMMIT HISTORY](https://github.com/virensachdev786/enterprise-agentic-platform/commits?author=virensachdev786&since=2025-12-27&until=2026-01-04)}**

### `Day 1 (Sunday **Dec 28, 2025**)`: Planning / Architecture, etc …

### `Day 2:(Monday **Dec 29, 2025)`:** SNOW PDI Setup + Curls…

### `Day 3: (Tuesday **Dec 30, 2025)`:** Vector DB Local Install + Chunking Strategy.

### `Day 4: (Wednesday **Dec 31, 2025)`:** Agentic Backend Foundation.

### `Day 5: (Thursday Jan 1, 2026)`: Agentic Backend Foundation + Initial Intent Engine

### `Day 6-8: (Fri, Jan 2 - Sun, Jan 4, 2026)`: Improve Intent Engine + Initial RAG → Evolve to ReAct + Dispatcher ( SNOW API Action + Email Inbound & Outbound)