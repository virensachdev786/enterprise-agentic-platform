# Incident Handling and Resolution States

## Purpose
Defines how the agent interacts with ServiceNow ticket states.

## Ticket Creation
- All automated incidents should be created with the category "IT Support".
- Default State: "2 - In Progress".

## Resolution Logic
- **Successful Reset**: Use the `CLOSE_INCIDENT` step. Set state to "6 - Resolved". 
- **Resolution Code**: "Solution Provided".
- **Resolution Notes**: "Issue resolved automatically by AI Agent Platform."

## Escalation Logic
- If any automation step fails, the ticket must remain "Open" for human review.