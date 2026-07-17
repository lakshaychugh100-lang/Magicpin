from fastapi import APIRouter, HTTPException
from app.models.trigger import Trigger
from app.engine.normalizer import Normalizer
from typing import Dict, Any

from pydantic import BaseModel
from typing import Dict, Any, List

class TickPayload(BaseModel):
    now: str
    available_triggers: List[str]

router = APIRouter()

@router.post("/tick")
async def tick(payload: TickPayload):
    from app.main import store, compose_engine
    
    actions = []
    
    for trigger_id in payload.available_triggers:
        trigger_data = store.get_context("trigger", trigger_id)
        if not trigger_data:
            continue
            
        trigger = Normalizer.normalize_trigger(trigger_data)
        
        merchant_data = store.get_merchant_context(trigger.merchant_id)
        if not merchant_data:
            continue
            
        merchant = Normalizer.normalize_merchant(merchant_data)
        
        customer = None
        if trigger.customer_id:
            customer_data = store.get_customer_context(trigger.customer_id)
            if customer_data:
                customer = Normalizer.normalize_customer(customer_data)
                
        response = compose_engine.process(merchant, trigger, customer)
        
        # Build the action dict exactly as the judge expects
        action = {
            "action": "send",
            "body": response.body,
            "cta": response.cta,
            "send_as": response.send_as,
            "suppression_key": response.suppression_key,
            "rationale": response.rationale
        }
        actions.append(action)
        
    return {"actions": actions}
