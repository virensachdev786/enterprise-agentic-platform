from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from agent_backend.api.routes import router
from agent_backend.api.routes import router

app = FastAPI(
    title="Enterprise Agent Backend",
    version="0.1.0",
    description="Agent backend for password reset automation"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Agent Backend Running"}
