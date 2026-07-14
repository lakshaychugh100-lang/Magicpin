from fastapi import APIRouter

router = APIRouter()

@router.get("/metadata")
async def metadata():
    return {
        "bot_id": "vera_bot_1",
        "version": "1.0.0",
        "capabilities": ["reply", "tick", "context"]
    }
