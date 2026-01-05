from curses import raw
import traceback
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

# Intent Engine
from agent_backend.core.intent_engine import IntentEngine
from agent_backend.models.intent_schema import IntentRequest, IntentResponse

# Planner
from agent_backend.core.planner import Planner
from agent_backend.models.plan_schema import PlanRequest, PlanResponse, PlannerDebugRequest, PlannerDebugResponse

# Service: SNOW & Dispatcher
from services.servicenow.context_processor import prepare_ai_user_state
from services.servicenow.user_lookup import get_user_by_email
from agent_backend.core.dispatcher import ActionDispatcher

class EmailProcessRequest(BaseModel):
    email: str
    body: str

# Initialize Engines
router = APIRouter()
intent_engine = IntentEngine()
planner = Planner()
dispatcher = ActionDispatcher()



@router.post("/analyze_intent")
async def analyze_intent(payload: EmailProcessRequest):
    """Analyzes the raw email to extract intent, urgency, and system."""
    try:
        # intent_engine.process expected to return a dict
        result = intent_engine.analyze(payload.body)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Intent analysis failed: {str(e)}")

@router.post("/build_plan")
async def build_plan(data: PlanRequest):
    """Retrieves policies/procedures and generates the execution plan."""
    try:
        plan = planner.build_plan(
            intent=data.intent,
            system=data.system,
            urgency=data.urgency,
            confidence=data.confidence,
            user_state=data.user_state,
            body=data.body
        )
        return plan
    except Exception as e:
        print(f"PLANNER_ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Planning failed: {str(e)}")

@router.post("/dispatch_actions")
async def dispatch_actions(request: Request):
    """Executes the steps defined in the plan via the Dispatcher."""
    data = await request.json()
    
    try:
        execution_results = dispatcher.run(
            steps=data.get("steps", []),
            context={
                "user_state": data.get("user_state"),
                "body": data.get("body"),
                "intent": data.get("intent")
            }
        )
        return {"status": "success", "results": execution_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")

@router.get("/debug_plan")
async def debug_plan():
    """Returns the current configuration of the threshold and models."""
    return {
        "relevance_threshold": planner.RELEVANCE_THRESHOLD,
        "llm_model": planner.llm.model,
        "kbs_active": ["policy_kb", "procedures_kb"]
    }

# TO-DO: @router.get("/execute_plan")
# ActionDispatcher.execute_plan

# -----------------------------
# FULL PROCESS EMAIL ENDPOINT
# -----------------------------
@router.post("/process_email")
async def process_email(payload: EmailProcessRequest):
    try:
        # 1. Detect Intent
        intent_data = intent_engine.analyze(payload.body)
        print("Intent: ", intent_data)

        print("---------------------------------------------------------------------------------------------------------")
        print("---------------------------------------------------------------------------------------------------------")
        print()

        # 2. Get User State from ServiceNow
        raw_user = get_user_by_email(payload.email)
        print("raw_user | payload.email: ", raw_user)

        print("---------------------------------------------------------------------------------------------------------")
        print("---------------------------------------------------------------------------------------------------------")
        print()

        # 3. Transform to AI-Ready Context
        clean_user_state = prepare_ai_user_state(raw_user)
        print("User State for AI: ", clean_user_state)

        print("---------------------------------------------------------------------------------------------------------")
        print("---------------------------------------------------------------------------------------------------------")
        print()

        # 4. Build Plan (Retrieves relevant Policies/Procedures)
        plan = planner.build_plan(
            intent=intent_data.intent,
            system=intent_data.system,
            urgency=intent_data.urgency,
            confidence=intent_data.confidence,
            user_state=clean_user_state,
            body=payload.body
        )
        print("Plan Generated:", plan)

        print("---------------------------------------------------------------------------------------------------------")
        print("---------------------------------------------------------------------------------------------------------")
        print()

        # 5. Execute the Plan 
        execution_logs = []
        if plan.get("steps"):
            # We extract the policy/procedure name to use as 'knowledge' 
            # for the email body if a specific response isn't drafted yet.
            knowledge_context = knowledge_context = plan.get("procedure_used") or plan.get("policy_used") or "Standard Operating Procedure"
            
            execution_logs = await dispatcher.execute_plan(
                steps=plan["steps"],
                user_email=payload.email,
                intent=intent_data.intent,
                body=payload.body,
                knowledge=knowledge_context # Pass context to Dispatcher
            )

        return {
            "status": "success",
            "intent_summary": {
                "intent": intent_data.intent,
                "confidence": intent_data.confidence,
                "system": intent_data.system
            },
            "user_context": clean_user_state,
            "execution_plan": plan,
            "execution_results": execution_logs 
        }

    except Exception as e:
        print("--- EXECUTION ERROR ---")
        traceback.print_exc() 
        print("-----------------------")
        raise HTTPException(status_code=500, detail=f"Agent Orchestration Error: {str(e)}")