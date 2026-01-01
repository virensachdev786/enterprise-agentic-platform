from pydantic import BaseModel

class IntentRequest(BaseModel):
    text: str


class IntentResponse(BaseModel):
    intent: str
    urgency: str
    system: str
    confidence: float
