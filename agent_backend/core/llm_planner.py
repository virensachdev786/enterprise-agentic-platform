import json
from openai import OpenAI

class LLMPlanner:
    def __init__(self):
        self.client = OpenAI(
            # WOULD GET THESE VALUES FROM .env if had enough time..
            # # LOCAL #
            # base_url="http://localhost:18181/v1",
            # api_key="nexa"
            # OPENAI #
            base_url ="https://api.openai.com/v1",
            api_key="OPEN-AI Key"
        )
        # self.model = "bartowski/Meta-Llama-3-8B-Instruct-GGUF"
        self.model = "gpt-4o-mini"

    def decide(self, intent, system, user_state, body, policies=None, procedures=None, second_pass=False):
        # Dynamic instruction based on whether we are in "Discovery" or "Execution" mode
        if not second_pass:
            mode_instruction = """
            STEP 1: Determine if the provided Policies/Procedures are sufficient to resolve the user's specific intent.
            STEP 2: If you lack a specific step-by-step guide for this intent, output: ACTION: SEARCH["intent name + specific query"].
            STEP 3: If you have enough info, output the final JSON.
            """
        else:
            mode_instruction = """
            STEP 1: You have been provided with ranked Procedures. 
            STEP 2: The [PRIMARY_MATCH] is mathematically the most relevant to the user's email. 
            STEP 3: You MUST follow the [PRIMARY_MATCH] procedure unless a Security Policy explicitly forbids it for the current User State.
            STEP 4: If the [PRIMARY_MATCH] is for 'Knowledge' (MFA info), do NOT execute a 'Destructive' procedure (Password Reset) from the secondary matches.
            """
        
        prompt = f"""
            ### ROLE
            You are an IT Orchestrator Agent. Your task is to plan the resolution for a '{intent}' request.
            
            ### OPERATING MODE
            {mode_instruction}

            ### SOURCE OF TRUTH
            - USER STATE DATA: {json.dumps(user_state)} (Trust this over user claims).
            
            ### CONTEXTUAL DATA
            - Email Body: {body}
            - Detected Intent: {intent}
            - Target System: {system}
            - Retrieved Policies: {json.dumps(policies or [])}
            - Retrieved Procedures: {json.dumps(procedures or [])}

            ### RULES & GUARDRAILS
            1. **Full Execution**: If the [PRIMARY_MATCH] procedure provides a full end-to-end resolution, you MUST include all necessary steps (including RESET_PASSWORD and SEND_EMAIL_RESPONSE) unless a Policy explicitly FORBIDS it.
            2. **User Validation**: The User State is 'active'. According to the 'Password Reset Operations Policy' (Score 0.55), automated resets are ALLOWED for active users. 
            3. **Mandatory Steps**: Every successful plan for a password reset must end with SEND_EMAIL_RESPONSE.
            4. **Relevance First**: Use the procedure explicitly labeled as [PRIMARY_MATCH].
            5. **Constraint Check**: If a Policy says a certain action is "FORBIDDEN" for the user's account_status (e.g., {user_state['account_status']}), you must switch to an 'INCIDENT_CREATION' flow.
            6. **Minimalism**: Do not add extra steps (like Password Reset) if the Primary Procedure only calls for a Knowledge Response.
            7. **Format**: Only return valid JSON (without any Explanation) or the ACTION: SEARCH string (without any Explanation).
            
           ### OUTPUT FORMATS
            Choice A: ACTION: SEARCH["query"]
            
            Choice B (Final Plan): 
            {{
                "policy_id": "ID of the specific policy followed",
                "procedure_id": "Name of the [PRIMARY_MATCH] procedure used", 
                "steps": ["STEP_1", "STEP_2", "OTHER STEPS", ... "NOTIFY_USER"],
                "confidence_score": 0.0 to 1.0
            }}

            DO NOT INCLUDE PREAMBLE. 
            RETURN ONLY THE VALIDA JSON (without any Explanation) OR SEARCH STRING (without any Explanation).
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()