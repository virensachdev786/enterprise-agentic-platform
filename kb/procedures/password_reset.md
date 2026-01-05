---
procedure_id: PASSWORD_RESET_STANDARD
intent: password_reset
system: ServiceNow
execution_mode: AUTOMATED
confidence_min: 0.6
---

# Password Reset – Standard Procedure

## Description
Used when a user requests a password reset and intent confidence is sufficiently high.

## Preconditions
- User identity must be verified
- No VIP or executive handling required
- Confidence score ≥ 0.6

## Steps
1. VERIFY_IDENTITY
2. CREATE_INCIDENT
3. RESET_PASSWORD
4. CLOSE_INCIDENT
5. NOTIFY_USER

## Failure Handling
- If identity verification fails → CREATE_INCIDENT
