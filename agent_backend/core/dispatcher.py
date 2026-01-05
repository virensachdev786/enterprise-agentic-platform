import logging
from services.servicenow.create_incident import create_incident, update_incident_state
from services.servicenow.user_lookup import get_user_by_email
from services.servicenow.password_reset import reset_password 
from services.email.outbound_service import send_external_email

logger = logging.getLogger(__name__)

class ActionDispatcher:
    def __init__(self):
        self.context_store = {} 

    async def execute_plan(self, steps: list, user_email: str, intent: str, body: str, knowledge: str = None):
        results = []
        self.context_store = {
            "email": user_email, 
            "intent": intent,
            "incident_number": None, 
            "incident_sys_id": None, 
            "user_sys_id": None,
            "knowledge_content": knowledge # Store RAG results for the email
        }

        user_data = get_user_by_email(user_email)
        if user_data:
            self.context_store["user_sys_id"] = user_data.get("sys_id")
            self.context_store["user_name"] = user_data.get("name", "User")
            logger.info(f"👤 Found User SysID: {self.context_store['user_sys_id']}")

        for item in steps:
            step_name = item["step"] if isinstance(item, dict) else item
            logger.info(f"⚙️ Dispatching Step: {step_name}")
            
            try:
                if step_name == "CREATE_INCIDENT":
                    res = self._step_create_incident(intent, body)
                elif step_name == "VERIFY_IDENTITY":
                    res = self._step_verify_identity()
                elif step_name == "RESET_PASSWORD":
                    res = self._step_reset_password()
                elif step_name == "CLOSE_INCIDENT":
                    res = self._step_close_incident()
                elif step_name == "GENERATE_KNOWLEDGE_RESPONSE":
                    res = self._step_generate_knowledge()
                elif step_name == "SEND_EMAIL_RESPONSE" or step_name == "NOTIFY_USER":
                    res = self._step_send_email()
                else:
                    res = f"Step {step_name} marked for manual review (No automation mapped)."
                
                results.append({"step": step_name, "status": "success", "details": res})
            except Exception as e:
                logger.error(f"❌ Step {step_name} failed: {str(e)}")
                results.append({"step": step_name, "status": "failed", "error": str(e)})
                break 

        return results

    # --- NEW / UPDATED STEPS ---

    def _step_generate_knowledge(self):
        """Prepares the RAG content for the email."""
        if not self.context_store.get("knowledge_content"):
            return "No specific KB articles found. Defaulting to general support message."
        return "Knowledge content successfully prepared for delivery."

    def _step_send_email(self):
        """Calls the actual outbound SMTP service."""
        recipient = self.context_store["email"]
        subject = f"Support Update: {self.context_store['intent'].replace('_', ' ').title()}"
        
        # Build the body based on what we have (Knowledge vs Password Reset)
        content = self.context_store.get("knowledge_content", "Your request is being processed.")
        inc_num = self.context_store.get("incident_number", "N/A")
        
        body = f"Hello {self.context_store.get('user_name', 'User')},\n\n"
        body += f"{content}\n\n"
        body += f"Reference Ticket: {inc_num}\n"
        body += "Best regards,\nYour IT AI Assistant"

        # Execute the SMTP call
        email_res = send_external_email(recipient, subject, body)
        
        if email_res["status"] == "success":
            return email_res["details"]
        raise Exception(f"Email delivery failed: {email_res.get('error')}")

    def _step_create_incident(self, intent, body):
        desc = f"Agentic AI processed request: {body}"
        inc_data = create_incident(
            short_description=f"{intent.upper()} Request", 
            description=desc,
            caller_id=self.context_store["user_sys_id"]
        )
        self.context_store["incident_number"] = inc_data["number"]
        self.context_store["incident_sys_id"] = inc_data["sys_id"]
        return f"Created Ticket: {inc_data['number']}"

    def _step_verify_identity(self):
        if self.context_store["user_sys_id"]:
            return f"Identity verified for user: {self.context_store['email']}"
        raise Exception("Identity verification failed: User not found in ServiceNow.")

    def _step_reset_password(self):
        email = self.context_store.get("email")
        temp_pw = reset_password(email)
        if not temp_pw:
            raise Exception("Password reset failed.")
        
        # We store the temp password so the email step can send it!
        self.context_store["knowledge_content"] = f"Your password has been reset. Your temporary password is: {temp_pw}"
        return f"SUCCESS: Temporary password [{temp_pw}] generated."

    def _step_close_incident(self):
        sys_id = self.context_store.get("incident_sys_id")
        if sys_id:
            success = update_incident_state(sys_id, state="6", close_notes="Resolved automatically.")
            if success:
                return f"Ticket {self.context_store['incident_number']} CLOSED."
        return "No active incident found to close."