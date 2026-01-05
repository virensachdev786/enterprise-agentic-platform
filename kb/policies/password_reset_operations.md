# Password Reset Operations Policy

## Eligibility Criteria
- **Allowed**: Automated reset is permitted if `account_status` is "active" or "locked".
- **Forbidden**: Reset is NOT permitted if `account_status` is "terminated" or "disabled".

## VIP Protection (Critical)
- **VIP Definition**: Any user where `vip_status` is "true".
- **Restriction**: The `RESET_PASSWORD` step is FORBIDDEN for VIP users.
- **Escalation**: For VIPs, the agent must:
    1. Skip the `RESET_PASSWORD` step.
    2. Set Incident Impact/Urgency to "1 - High".
    3. Inform the user that a human technician will contact them shortly.

## Security Standards
- Temporary passwords must be 10 characters minimum.
- Passwords must be sent via the `NOTIFY_USER` step only.