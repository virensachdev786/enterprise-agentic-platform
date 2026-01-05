# Identity Verification Policy

## Purpose
To prevent unauthorized account access via social engineering.

## Verification Requirements
1. **Primary Method**: The step `VERIFY_IDENTITY` must compare the sender's email address against the ServiceNow `sys_user` table.
2. **Status Check**: If `get_user_by_email` returns no result, the identity is "Unverified".
3. **Blocking Rule**: If identity is "Unverified", the agent MUST NOT proceed with `RESET_PASSWORD`. 

## Failure Handling
- If verification fails, the agent must log a security note in the incident and end the execution.