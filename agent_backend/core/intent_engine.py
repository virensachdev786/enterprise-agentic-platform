from agent_backend.models.intent_schema import IntentResponse
from .llm_classifier import LLMClassifier


class IntentEngine:
    def __init__(self):
        self.llm = LLMClassifier()

    # ------------------------------
    #  RULE ENGINE (Deterministic)
    # ------------------------------
    def rule_based_detection(self, text: str):
        text_lower = text.lower()

        # PASSWORD RESET / ACCOUNT UNLOCK
        if ("password reset" in text_lower or "reset my password" in text_lower or
            "forgot password" in text_lower or "locked out" in text_lower or
            "unlock my account" in text_lower or "account locked" in text_lower):

            urgency = "high" if "urgent" in text_lower or "asap" in text_lower else "medium"

            return {
                "intent": "password_reset",
                "urgency": urgency,
                "system": "AD" if "ad" in text_lower or "active directory" in text_lower else "unknown",
                "confidence": 0.85
            }

        # MFA / VPN / TOKEN ISSUES
        if ("mfa" in text_lower or "otp" in text_lower or "token" in text_lower or
            "2fa" in text_lower or "authenticator" in text_lower):

            urgency = "high" if "urgent" in text_lower else "medium"

            return {
                "intent": "mfa_issue",
                "urgency": urgency,
                "system": "VPN" if "vpn" in text_lower else "unknown",
                "confidence": 0.80
            }

        # ACCESS / PERMISSION REQUESTS (not supported yet → force unknown)
        if (
            "access" in text_lower or
            "permission" in text_lower or
            "license" in text_lower or
            "add me" in text_lower or
            "request access" in text_lower or
            "provision" in text_lower or
            "enable" in text_lower
        ):
            return {
                "intent": "unknown",
                "urgency": "medium",
                "system": "unknown",
                "confidence": 0.60
            }

        # UNKNOWN
        return {
            "intent": "unknown",
            "urgency": "medium",
            "system": "unknown",
            "confidence": 0.40
        }

    # ------------------------------
    #  HYBRID ENGINE
    # ------------------------------
    def analyze(self, text: str) -> IntentResponse:
        # 1️⃣ RULE ENGINE FIRST
        rule_result = self.rule_based_detection(text)

        # If high confidence → Stop. No need to call LLM.
        if rule_result["confidence"] >= 0.80:
            return IntentResponse(**rule_result)

        # 2️⃣ FALLBACK TO LLM
        llm_result = self.llm.classify(text)

        # Safety net defaults
        llm_intent = llm_result.get("intent", "unknown")
        llm_urgency = llm_result.get("urgency", "medium")
        llm_system = llm_result.get("system", "unknown")
        llm_conf = float(llm_result.get("confidence", 0.5))

        # 3️⃣ PICK BEST ANSWER
        # If LLM stronger → trust LLM
        if llm_conf > rule_result["confidence"] and llm_intent != "unknown" and llm_conf >= 0.85:
            return IntentResponse(
                intent=llm_intent,
                urgency=llm_urgency,
                system=llm_system,
                confidence=llm_conf
            )

        # Otherwise stick to rules
        return IntentResponse(**rule_result)
