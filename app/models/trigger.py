from typing import Dict, Any, Optional
from pydantic import BaseModel

class Trigger(BaseModel):
    id: str
    scope: str
    kind: str
    source: str
    merchant_id: str
    customer_id: Optional[str] = None
    payload: Dict[str, Any] = {}
    urgency: int
    suppression_key: str
    expires_at: str
