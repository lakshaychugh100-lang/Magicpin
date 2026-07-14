from fastapi import FastAPI
from app.api.context import router as context_router
from app.api.tick import router as tick_router
from app.api.reply import router as reply_router
from app.api.health import router as health_router
from app.api.metadata import router as metadata_router
from app.storage.sqlite_store import SQLiteStore
from app.engine.compose import ComposeEngine

app = FastAPI(title="Vera Message Engine")

store = SQLiteStore("local_data.db")
compose_engine = ComposeEngine()

app.include_router(context_router, prefix="/v1")
app.include_router(tick_router, prefix="/v1")
app.include_router(reply_router, prefix="/v1")
app.include_router(health_router, prefix="/v1")
app.include_router(metadata_router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
