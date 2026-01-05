import logging

class ActionDispatcher:
    def __init__(self):
        self.logger = logging.getLogger("dispatcher")

    async def execute(self, steps, context):
        """
        Takes the list of steps and executes them one by one.
        """
        results = []
        for step in steps:
            self.logger.info(f"🚀 Executing Step: {step}")
            
            # Map the string from the Planner to a function
            if step == "CREATE_INCIDENT":
                outcome = await self._create_snow_incident(context)
            elif step == "GENERATE_KNOWLEDGE_RESPONSE":
                outcome = await self._generate_email_draft(context)
            elif step == "CLOSE_INCIDENT":
                outcome = "Successfully closed ticket in ServiceNow."
            else:
                outcome = f"Manual intervention required for: {step}"
            
            results.append({"step": step, "outcome": outcome})
        
        return results

    async def _create_snow_incident(self, ctx):
        # This is where we will eventually put the ServiceNow API call
        return f"CREATED: Incident #INC-202405 for {ctx['email']} (Intent: {ctx['intent']})"

    async def _generate_email_draft(self, ctx):
        # Here we could use the LLM again to write the actual email body
        return "DRAFTED: 'Hello, we have received your request...'"