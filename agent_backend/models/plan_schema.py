# agent_backend/models/plan_schema.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PlanRequest(BaseModel):
    intent: str = Field(..., description="High-level user intent, e.g. password_reset")
    system: str = Field(..., description="Target system, e.g. AD")
    urgency: str = Field(..., description="low | normal | high")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Intent confidence")
    # Added user_state field here
    user_state: Dict[str, Any] = Field(
        default={"vip": False, "account_status": "active"}, 
        description="JSON object containing user details like VIP status, etc."
    )
    body: str

class PlanResponse(BaseModel):
    policy_used: str
    procedure_used: str
    steps: list[str]
    agent_was_curious: bool
    confidence: float = 1.0  # Add a default value so it stops crashing


class PlannerDebugRequest(BaseModel):
    intent: str
    system: str
    urgency: str = "normal"
    confidence: float = 0.5
    top_k: int = Field(5, ge=1, le=20)


class RankedPolicy(BaseModel):
    policy_id: str
    score: float
    distance: float
    semantic_confidence: float
    risk_level: Optional[str] = None
    policy_name: Optional[str] = None
    section_name: Optional[str] = None
    source: Optional[str] = None
    content_preview: str
    metadata: Dict[str, Any] = {}


class PlannerDebugResponse(BaseModel):
    query: str
    selected_policy_id: str
    selected_policy_score: float
    ranked_policies: List[RankedPolicy]
