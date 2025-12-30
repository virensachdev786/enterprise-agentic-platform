# Identity Verification Policy

## Purpose
To ensure password resets are performed securely and only for verified users.

## Rules
1. The system must verify the requesting user’s identity before a password reset is initiated.
2. Acceptable verification types:
   - ServiceNow user record validation
   - Security question verification (if enabled)

## Special Notes
- If identity cannot be verified → Reset MUST NOT proceed.
- If verification fails 3 times → Escalate to human support.

