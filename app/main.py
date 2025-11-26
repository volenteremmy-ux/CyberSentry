from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise-Grade Fraud Detection SDK for Kenyan Fintech."
)

app.include_router(router, prefix=settings.API_PREFIX, tags=["Detection"])

@app.get("/")
def health_check():
    return {"status": "operational", "version": settings.VERSION}