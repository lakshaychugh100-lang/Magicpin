import json
import asyncio
from app.api.context import receive_context, ContextPayload
from app.api.tick import tick

async def run():
    # Load sample merchant
    with open("expanded/merchants/m_001_drmeera_dentist_delhi.json", "r") as f:
        merchant_data = json.load(f)
        
    context_payload = ContextPayload(
        scope="merchant",
        context_id=merchant_data["merchant_id"],
        version=1,
        payload=merchant_data,
        delivered_at="2026-07-14T10:00:00Z"
    )
    
    # Push Context
    res = await receive_context(context_payload)
    print("Context Response:", res)
    
    # Load trigger
    with open("expanded/triggers/trg_001_research_digest_dentists.json", "r") as f:
        trigger_data = json.load(f)
        
    # Run Tick
    try:
        response = await tick(trigger_data)
        print("Tick Response:", json.dumps(response, indent=2))
    except Exception as e:
        print("Tick Error:", e)

if __name__ == "__main__":
    asyncio.run(run())
