from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class ContextPayload(BaseModel):
    scope: str
    context_id: str
    version: int
    payload: Dict[str, Any]
    delivered_at: str

@router.post("/context")
async def receive_context(data: ContextPayload):
    from app.main import store
    
    # Generic save for any scope (merchant, customer, category, trigger, etc)
    accepted = store.save_context(data.scope, data.context_id, data.payload, data.version, data.delivered_at)
        
    return {
        "accepted": accepted,
        "ack_id": f"ack_{data.context_id}_{data.version}",
        "stored_at": data.delivered_at
    }
