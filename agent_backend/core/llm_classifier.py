import json
import re
from openai import OpenAI

class LLMClassifier:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:18181/v1",
            api_key="nexa"
        )
        self.model_name = "bartowski/Meta-Llama-3-8B-Instruct-GGUF"

    def classify(self, text: str):
        system_prompt = ("""
            You are an IT incident intent classifier. 
            You MUST ONLY output JSON. No prose. No explanations.
            Return a single JSON object with the exact schema:

            {
            "intent": "password_reset" | "unlock_account" | "mfa_issue" | "unknown",
            "urgency": "low" | "medium" | "high",
            "system": "AD" | "VPN" | "Salesforce" | "unknown",
            "confidence": float between 0 and 1
            }

            STRICT RULES:
            - DO NOT guess.
            - If the request is about tool access, permissions, licenses, approvals, onboarding, analytics tools, Tableau, Slack, Jira, or anything not explicitly password/MFA related → intent MUST be "unknown".
            - If the text does not clearly match a supported intent → intent MUST be "unknown".
            - If system is not clearly mentioned (AD, VPN, Salesforce) → system MUST be "unknown".
            - NEVER invent a system or intent that is not explicitly mentioned.
            - If unsure, set intent = "unknown", system = "unknown", urgency = "medium", confidence <= 0.5.

            Output ONLY valid JSON. No markdown. No text""")

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