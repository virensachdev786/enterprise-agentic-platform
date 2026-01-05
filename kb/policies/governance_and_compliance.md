# IT Automation Governance & Compliance Policy

## Purpose
To ensure all automated AI actions are auditable, traceable, and compliant with corporate IT standards.

## Mandated Orchestration
1. **No Shadow Actions**: Every automated execution must be logged.
2. **Incident Linking**: The `CREATE_INCIDENT` step is MANDATORY for any request involving account changes or password resets.
3. **Closure Requirement**: If an automated action is completed successfully, the `CLOSE_INCIDENT` step must be executed to resolve the ticket in ServiceNow.

## Audit Logging
- The agent must record the `incident_number` in the final execution summary.
- The `user_sys_id` must be linked as the 'Caller' for all tickets.