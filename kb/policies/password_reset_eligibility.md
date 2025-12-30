# Password Reset Eligibility Policy

## Purpose
Define when automated password reset is allowed.

## Allowed Reset Conditions
1. Account in "Locked" state
2. Account in "Active but password expired"
3. User identity successfully verified

## Not Allowed Conditions
1. User marked as VIP / Executive
2. Account disabled or terminated
3. Security risk flagged on account
4. Policy retrieval fails

## System Behavior
If NOT eligible:
- Do not reset
- Open ServiceNow incident
- Notify security team if high risk

