import re
import json
from agent_backend.core.llm_planner import LLMPlanner
from agent_backend.core.retriever import KnowledgeRetriever

class Planner:
    def __init__(self):
        self.policy_kb = KnowledgeRetriever("policy_kb")
        self.procedure_kb = KnowledgeRetriever("procedures_kb")
        self.llm = LLMPlanner()
        
        # Lowered threshold: 0.85 means we only accept high-quality matches.
        # This will likely filter out the 0.98 password reset match entirely.
        self.RELEVANCE_THRESHOLD = 0.90

    def build_plan(self, intent, system, urgency, confidence, user_state, body):
        # STAGE 1: Global Security context based on SNOW status
        security_policies = self.policy_kb.query(f"Policy for {user_state['account_status']}", top_k=1)
        
        # 1. FIRST PASS: Ask LLM if it can plan or if it needs to search
        raw_decision = self.llm.decide(
            intent=intent, 
            system=system, 
            user_state=user_state, 
            body=body, 
            policies=security_policies
        )

        # 2. TOOL CALL LOGIC: Check if LLM requested a search
        if "ACTION: SEARCH" in raw_decision:
            match = re.search(r'\["(.*?)"\]', raw_decision)
            search_query = match.group(1) if match else intent
            
            print(f"DEBUG: Agent requested search for: {search_query}")

            # Retrieve intent-specific data
            raw_policies = self.policy_kb.query(f"Policy for {search_query}", top_k=2)
            raw_procedures = self.procedure_kb.query(f"Procedure for {search_query}", top_k=2)

            # --- DYNAMIC FILTERING & RANKING ---
            # We filter out anything above the threshold to prevent "hallucinated" procedures
            filtered_procedures = [p for p in raw_procedures if p['score'] <= self.RELEVANCE_THRESHOLD]
            
            # Sort remaining procedures by score (lowest distance = first)
            final_procedures = sorted(filtered_procedures, key=lambda x: x['score'])

            if not final_procedures:
                print(f"⚠️ No highly relevant procedures found (Best score > {self.RELEVANCE_THRESHOLD}). Overriding with Fallback.")
                return {
                    "policy_used": "GENERAL_SECURITY_POLICY",
                    "procedure_used": "UNKNOWN_INTENT_PROCEDURE",
                    "steps": ["CREATE_INCIDENT", "GENERATE_KNOWLEDGE_RESPONSE", "SEND_EMAIL_RESPONSE"],
                    "agent_was_curious": True,
                    "confidence": confidence
                }

            # Prepare procedures with "Rank" info for the LLM to respect the distance score
            ranked_procedures = []
            for i, proc in enumerate(final_procedures):
                rank_label = "PRIMARY_MATCH" if i == 0 else "SECONDARY_MATCH"
                ranked_content = f"[{rank_label}] (Match Score: {proc['score']})\n{proc['content']}"
                
                # We update the dictionary content to include this ranking label
                proc_copy = proc.copy()
                proc_copy['content'] = ranked_content
                ranked_procedures.append(proc_copy)

            # 3. SECOND PASS: Final Decision
            # We pass only filtered, ranked procedures to ensure the LLM doesn't pick a fuzzy match
            raw_decision = self.llm.decide(
                intent=intent, 
                system=system, 
                user_state=user_state, 
                body=body, 
                policies=raw_policies + security_policies, 
                procedures=ranked_procedures,
                second_pass=True
            )

        # 4. FINAL PARSE
        decision = self.parse_json_safely(raw_decision)

        print(f"DEBUG: Raw LLM Decision String: {raw_decision}") # ADD THIS LINE
        decision = self.parse_json_safely(raw_decision)
        
        return {
            "policy_used": decision.get("policy_id", "UNKNOWN"),
            "procedure_used": decision.get("procedure_id", "UNKNOWN"),
            "steps": decision.get("steps", []),
            "agent_was_curious": "ACTION: SEARCH" in raw_decision
        }

    def parse_json_safely(self, text):
        try:
            clean = re.sub(r"```json|```", "", text).strip()
            match = re.search(r"(\{.*\})", clean, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return {}
        except Exception as e:
            print(f"ERROR Parsing LLM Plan: {e}")
            return {}