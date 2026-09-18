from fastapi import FastAPI
from sqlalchemy import text

from app.api.users import router as users_router
from app.core.database import engine

app = FastAPI(
    title="Chess Platform API",
    version="1.0.0",
)

app.include_router(users_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }

@app.get("/db-health")
def database_health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}