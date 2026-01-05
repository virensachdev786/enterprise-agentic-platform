import json
import re
from openai import OpenAI

class LLMClassifier:
    def __init__(self):
        # WOULD GET THESE VALUES FROM .env if had enough time..
        self.client = OpenAI(
            # # LOCAL #
            # base_url="http://localhost:18181/v1",
            # api_key="nexa"
            # OPENAI #
            base_url ="https://api.openai.com/v1",
            api_key="OPENAI-KEY"
        )
        # self.model_name = "bartowski/Meta-Llama-3-8B-Instruct-GGUF"
        self.model_name = "gpt-4o-mini"
    

    def classify(self, text: str):
        system_prompt = ("""
            ### ROLE
            You are a Lead IT Triage Engineer. Your job is to extract intent from IT support emails.
            You MUST ONLY output JSON. No prose. No explanations.
            Return a single JSON object with the exact schema

            ### ENTITY MAPPING LOGIC
            Map the user's mentioned system to these Internal Categories:
            1. **AD**: Windows, Main Computer, Laptop Login, SSO, SAML, Portal, Directory, or general "system."
            2. **Salesforce**: CRM, Salesforce, or Lead Management.
            3. **VPN**: GlobalProtect, Remote Access, AnyConnect, or "Home Connection."
            4. **ServiceNow**: Ticketing, SNOW, Support Portal, or KB.

            ### INTENT DEFINITIONS
            - **password_reset**: Credentials rejected, expired, forgotten, or "not accepted."
            - **unlock_account**: Account "locked," "frozen," "too many attempts," or "greyed out."
            - **mfa_issue**: Tokens, 2FA, codes, Duo, Okta pushes, or "new phone setup."
            - **knowledge_question**: Use for "How-to" questions, policy inquiries, or requests for information that do not require a technical fix/reset (e.g., "Where is the holiday schedule?" or "How do I set up MFA?").

            ### DECISION LOGIC
            1. **PRIMARY BLOCKER**: If a user reports a broken monitor but CANNOT login to report it, prioritize the login issue (password_reset/unlock_account).
            2. **HARDWARE/OFFICE**: If the email is purely about hardware (broken mouse, monitor), licenses, or office furniture → intent="unknown".

            ### OUTPUT FORMAT
            Output ONLY valid JSON, 
            DO NOT SAY ANYTHING LIKE "Here is the output", ONLY RETURN VALID JSON OBJECT
            NOTHING ELSE - no reasoning or Analysis
            {
                "intent": "password_reset" | "unlock_account" | "mfa_issue" | "knowledge_question" | "unknown",
                "urgency": "low" | "medium" | "high",
                "system": "AD" | "VPN" | "Salesforce" | "ServiceNow" | "unknown",
                "confidence": float
            }
            
            
        """)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.0
            )

            raw = response.choices[0].message.content.strip()

            # Remove Markdown JSON fences if present
            raw = re.sub(r"```json|```", "", raw).strip()
            print(raw)

            data = json.loads(raw)

            # --- Safety Guards ---
            data.setdefault("intent", "unknown")
            data.setdefault("urgency", "medium")
            data.setdefault("system", "unknown")
            data.setdefault("confidence", 0.5)

            return data

        except Exception as e:
            print(f"[LLM Classifier Error] {e}")
            return {
                "intent": "unknown",
                "urgency": "medium",
                "system": "unknown",
                "confidence": 0.2
            }