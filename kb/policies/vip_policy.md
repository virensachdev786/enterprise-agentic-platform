# VIP & Executive Protection Policy
ID: POLICY_VIP_BLOCK

## RULE
IF user_state.vip_status == True:
    - ACTION: RESET_PASSWORD is STRICTLY FORBIDDEN.
    - ACTION: MUST CREATE_INCIDENT with priority 1.
    - ACTION: MUST ESCALATE_TO_HUMAN.
    - REASON: High-value targets require physical identity verification.