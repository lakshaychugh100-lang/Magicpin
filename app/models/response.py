from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class DecisionTrace(BaseModel):
    features: Dict[str, Any]
    scores: Dict[str, float]
    winner: str
    template: str
    confidence: float

class EngineResponse(BaseModel):
    body: str
    cta: str
    send_as: str
    suppression_key: str
    rationale: str
    # The trace is optionally returned but generally stripped at the edge if needed
    decision_trace: Optional[DecisionTrace] = None
