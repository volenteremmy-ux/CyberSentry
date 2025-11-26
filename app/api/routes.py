# File: app/api/routes.py
from fastapi import APIRouter, HTTPException
from app.models.schema import ScanRequest, ScanResponse
from app.services.engine import FraudEngine

router = APIRouter()
engine = FraudEngine()

@router.post("/scan", response_model=ScanResponse, summary="Analyze Transaction Context")
async def scan_transaction(request: ScanRequest):
    try:
        score, level, flags, action, time_ms = engine.analyze(request.message, request.sender)
        
        return ScanResponse(
            risk_score=score,
            risk_level=level,
            flags=flags,
            action=action,
            analysis_time_ms=round(time_ms, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))