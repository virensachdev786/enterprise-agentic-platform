---
procedure_id: UNKNOWN_ESCALATION
intent: unknown
system: unknown
execution_mode: ESCALATION
confidence_min: 0.0
---

# Unknown Request – Escalation Procedure

## Description
Used when intent cannot be confidently determined.

## Preconditions
- Intent is unknown OR confidence is low

## Steps
1. CREATE_INCIDENT
2. ASSIGN_TO_SUPPORT_QUEUE
3. NOTIFY_USER_OF_ESCALATION

## Notes
- No automation beyond ticket creation
