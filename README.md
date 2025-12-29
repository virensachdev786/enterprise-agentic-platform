# Agentic AI Password Reset System

This project is a hands-on implementation of an **Agentic AI platform** designed to automate enterprise password reset workflows using **Email as the initial user interface channel**, the **UPRA (Understand → Plan → Retrieve → Act)** reasoning framework, and seamless integration with **ServiceNow ITSM**.

---

## 🎯 Goal

Build a production-ready, practical Agentic AI system that:
- Understands real-world employee requests (messy, human language)
- Dynamically plans actions instead of following rigid scripts
- Uses **policy-driven logic + RAG** to stay compliant and secure
- Executes real password resets via **ServiceNow APIs**
- Provides confirmations and auditability
- Extensible to IT, HR, Finance, CRM workflows in the future

---

## 🧠 Core Architecture

The system is designed around four key intelligent phases:

### 1️⃣ Understand  
Natural language intent detection + entity extraction from user request (via email initially).

### 2️⃣ Plan  
The AI **generates a task plan** dynamically:
- Verifies identity
- Fetches security policies
- Checks user account state
- Determines automation eligibility
- Decides reset vs. create ticket

### 3️⃣ Retrieve  
Policy + Knowledge retrieval using vectors to ensure:
- MFA rules compliance  
- Security guardrails  
- Organizational requirements

### 4️⃣ Act  
Executes securely:
- Calls ServiceNow APIs
- Logs actions
- Sends confirmation to user
- Closes request lifecycle

---

## 🔗 Integrations

| Component | Purpose |
|----------|--------|
Email UI | Initial conversational channel for users  
Vector DB | Policy + Knowledge retrieval  
ServiceNow | Account lookup + password reset + logging  
LLM | Reasoning, orchestration, and adaptive planning  

---

## 🚧 Roadmap

- [x] Architecture & Design Docs
- [ ] ServiceNow Sandbox & API Wiring
- [ ] Knowledge Base + Vector Store Setup
- [ ] Agentic Orchestration Engine
- [ ] Email Interaction Workflow
- [ ] Demo + Deployment Readiness

---

## 📂 Repository Structure

- docs/
- ├─ architecture-documents/
- ├─ diagrams/
- └─ handdrawn-diagrams/

---

## 🤝 Philosophy

This is not a chatbot.  
This is a **policy-aware, action-orchestrating AI agent** built for real enterprise environments.

