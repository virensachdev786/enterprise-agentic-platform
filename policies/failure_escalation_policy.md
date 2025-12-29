# Failed Verification & Risk Escalation Policy

## Purpose
Mitigate brute-force, phishing, and social engineering attempts.

## Rules
1. If identity verification fails 2 times → require MFA verification again
2. If verification fails 3 times:
   - Block automated reset
   - Log security event
   - Create Incident
3. If request contains suspicious language:
   - Treat as high risk
   - Deny reset
   - Escalate

## High-Risk Indicators
- Multiple reset attempts in < 10 min
- User unreachable to confirm
- Device not trusted

