# High-Level Architecture (HLA)

## Goal:

> “This is an Agentic AI Helpdesk Assistant that understands email requests, follows password-reset policy via a knowledge base, and safely executes or escalates actions through ServiceNow with full logging and confidence control.”
> 

## Main Components:

### 1. **Channels (User Interfaces)**:

- Email UIL
    - Users send emails to: `helpdesk-ai@demo.local`
    - A lightweight **Email Gateway** (IMAP poller or webhook) forwards messages to the backend `/inbound/email`.
- (Optional later) **CLI / Chat UI**
    - Simple terminal or web chat that hits `/chat`.

### 2. **Backend Service (FastAPI App):**

Core entrypoint for all channels.

Modules inside:

- **`Request Router`**:
    - Normalizes incoming requests into a common format:
    
    ```jsx
    {
      "user_id": "john.doe@company.com",
      "channel": "email",
      "text": "I'm locked out of my workstation...",
      "message_id": "abc123",
      "meta": {...}
    }
    ```
    
- **`Conversation Store`:**
    - Keeps basic history per user (SQLite/Postgres):
        - last N messages,
        - current “intent session” (e.g., a password-reset flow that is mid-MFA).
- **`Agent Orchestrator (UPRA Engine)`**:
    - Implements: **`Understand → Plan → Retrieve → Act (+Validate)**.`
    - Calls `LLM` and “`tools`” (`ServiceNow, KB, Policy Engine`).
    - Controls confidence thresholds and fallback.
- **`Tool Layer`:**
    - `ServiceNowClient` – REST calls:
        - lookup user
        - create incident
        - (optionally) trigger password reset script
    - `KBClient` – vector search over policies and reset procedures
    - `PolicyEngine` – deterministic checks: “Are we allowed to do automated reset for this user/system?”
    - `NotificationService` – send reply email; log output.
- **`Telemetry & Logging`:**
    - Structured logs per request:
        - intent
        - tools used
        - confidence score
        - outcome (success/fail/esc).

### 3. Data Store:

- **Conversation DB (SQLite/Postgres)**
    - Tables: `conversations`, `messages`, `actions_log`, `metrics_daily`.
- **Vector Store (Chroma / local)**
    - Stores:
        - password reset policies (remote vs on-prem, VPN, etc.)
        - MFA / identity verification rules
        - “When to escalate” rules

### 3. External Systems:

- **ServiceNow Sandbox**
    - `sys_user` (user lookup, phone/email)
    - `incident` or `sc_request` / `sc_task` (ticketing)
    - custom Scripted REST API for password reset.
- **Email Provider**
    - IMAP/POP to read new messages
    - SMTP/SendGrid/etc. to send responses