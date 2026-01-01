from fastapi import APIRouter
from agent_backend.core.intent_engine import IntentEngine
from agent_backend.models.intent_schema import IntentRequest, IntentResponse

router = APIRouter()
intent_engine = IntentEngine()

@router.post("/intent/analyze", response_model=IntentResponse)
async def analyze_intent(payload: IntentRequest):
    result = intent_engine.analyze(payload.text)
    return result
