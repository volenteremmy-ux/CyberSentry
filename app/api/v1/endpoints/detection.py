from fastapi import APIRouter, HTTPException
from app.schemas.schema import ScanRequest, ScanResponse
from app.services.engine import FraudEngine
import time

router = APIRouter()
engine = FraudEngine()

@router.post("/scan", response_model=ScanResponse)
def detect_fraud(request: ScanRequest):
    start_time = time.time()
    
    # Run the Engine
    score, level, flags, action = engine.analyze(request.message_body, request.sender)
    
    process_time = (time.time() - start_time) * 1000
    
    return ScanResponse(
        risk_score=score,
        risk_level=level,
        detection_flags=flags,
        recommended_action=action,
        processing_time_ms=round(process_time, 2)
    )