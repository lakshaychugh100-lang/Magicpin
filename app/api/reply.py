from fastapi import APIRouter
from typing import Dict, Any
from app.engine.intent_engine import IntentEngine

router = APIRouter()
intent_engine = IntentEngine()

@router.post("/reply")
async def reply(payload: Dict[str, Any]):
    message = payload.get("message", "")
    from_role = payload.get("from_role", "merchant")
    
    # Process the message through our config-driven intent engine
    response = intent_engine.evaluate(message, from_role)
    
    return response
