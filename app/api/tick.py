from fastapi import APIRouter, HTTPException
from app.models.trigger import Trigger
from app.engine.normalizer import Normalizer
from typing import Dict, Any

router = APIRouter()

@router.post("/tick")
async def tick(trigger_payload: Dict[str, Any]):
    from app.main import store, compose_engine
    
    trigger = Normalizer.normalize_trigger(trigger_payload)
    
    merchant_data = store.get_merchant_context(trigger.merchant_id)
    if not merchant_data:
        raise HTTPException(status_code=404, detail="Merchant context not found")
    
    merchant = Normalizer.normalize_merchant(merchant_data)
    
    customer = None
    if trigger.customer_id:
        customer_data = store.get_customer_context(trigger.customer_id)
        if customer_data:
            customer = Normalizer.normalize_customer(customer_data)
            
    response = compose_engine.process(merchant, trigger, customer)
    
    # Do not expose decision_trace in production response (could add logic here based on env)
    return response.model_dump(exclude={"decision_trace"})
