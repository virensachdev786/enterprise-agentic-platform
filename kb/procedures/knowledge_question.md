---
procedure_id: KNOWLEDGE_RESPONSE_ONLY
intent: knowledge_question
system: unknown
execution_mode: KNOWLEDGE_ONLY
confidence_min: 0.4
---

# Knowledge-Only Response Procedure

## Description
Used when the user asks how to do something (e.g., MFA setup, general IT questions, Policy).

## Preconditions
- No identity verification required

## Steps
1. CREATE_INCIDENT
2. GENERATE_KNOWLEDGE_RESPONSE
3. SEND_EMAIL_RESPONSE
4. CLOSE_INCIDENT
