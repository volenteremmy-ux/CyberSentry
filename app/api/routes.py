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
    
# ... inside routes.py ...
from app.models.schema import ScanRequest, ScanResponse, ReportRequest # Import new schema
import random # For fake heatmap data

# MOCK DATABASE (In-memory for demo)
REPORT_DB = []

@router.post("/report", summary="User reports a scam")
async def report_scam(request: ReportRequest):
    REPORT_DB.append(request)
    return {"status": "Reported", "message": "Thank you. The Ulinzi Network has been updated."}

@router.get("/stats", summary="Get Bank Dashboard Data")
async def get_dashboard_stats():
    # Simulate data for the dashboard if empty
    total_scans = 1420 + len(REPORT_DB)
    blocked_today = 89 + len(REPORT_DB)
    
    # Mocking coordinates for a Heatmap (Nairobi, Mombasa, Kisumu)
    # In a real app, this comes from IP/Tower data
    heatmap_data = [
        {"lat": -1.2921, "lon": 36.8219}, # Nairobi
        {"lat": -4.0435, "lon": 39.6682}, # Mombasa
        {"lat": -0.0917, "lon": 34.7680}, # Kisumu
        {"lat": -0.5143, "lon": 35.2698}, # Bomet (Mulot - Scam HQ)
    ]
    
    # Add some random jitter to make the map look alive
    for _ in range(10):
        heatmap_data.append({
            "lat": -1.2921 + random.uniform(-0.1, 0.1),
            "lon": 36.8219 + random.uniform(-0.1, 0.1)
        })

    return {
        "total_scans": total_scans,
        "threats_blocked": blocked_today,
        "active_campaigns": ["M-Pesa Blocked Script", "KRA Pin Reset", "Fake Reward"],
        "heatmap": heatmap_data,
        "recent_reports": REPORT_DB[-5:] # Last 5 reports
    }



# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.orm import Session
# from app.models.schema import ScanRequest, ScanResponse, ReportRequest, StatsResponse
# from app.core.database import Base, engine, get_db
# from app.models.sql_models import ScamReport

# # Create Tables automatically when app starts
# Base.metadata.create_all(bind=engine)

# router = APIRouter()
# engine_logic = FraudEngine()

# # --- EXISTING SCAN ENDPOINT ---
# @router.post("/scan", response_model=ScanResponse)
# async def scan_transaction(request: ScanRequest):
#     # ... (Keep your existing logic here) ...
#     # Copy paste your logic calling engine_logic.analyze(...)
#     # For brevity, I assume you kept the previous code
#     score, level, flags, action, time_ms = engine_logic.analyze(request.message, request.sender)
#     return ScanResponse(
#         risk_score=score, risk_level=level, flags=flags, 
#         action=action, analysis_time_ms=round(time_ms, 2)
#     )

# # --- NEW: REPORT ENDPOINT ---
# @router.post("/report", summary="Crowdsource a Scam")
# def report_scam(report: ReportRequest, db: Session = Depends(get_db)):
#     """
#     Save a confirmed scam to the database.
#     This builds the 'Waze' network effect.
#     """
#     new_report = ScamReport(
#         sender=report.sender,
#         message=report.message,
#         source=report.source,
#         risk_score=report.risk_score
#     )
#     db.add(new_report)
#     db.commit()
#     db.refresh(new_report)
#     return {"status": "Report Saved", "id": new_report.id}

# # --- NEW: DASHBOARD STATS ---
# @router.get("/stats", response_model=StatsResponse)
# def get_dashboard_stats(db: Session = Depends(get_db)):
#     count = db.query(ScamReport).count()
#     last_scam = db.query(ScamReport).order_by(ScamReport.timestamp.desc()).first()
    
#     return StatsResponse(
#         total_reports=count,
#         top_scam_sender=last_scam.sender if last_scam else "None",
#         recent_threat=last_scam.message[:30] + "..." if last_scam else "None"
#     )