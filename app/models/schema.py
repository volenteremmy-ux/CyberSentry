from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ScanRequest(BaseModel):
    sender: str = Field(..., description="The Sender ID (e.g. +2547... or Safaricom)")
    message: str = Field(..., description="The SMS or Clipboard content")
    source: str = Field(..., description="Origin: SMS, WhatsApp, Web")

    # Validator: Clean the phone number automatically
    @validator('sender')
    def clean_sender(cls, v):
        return v.strip()

class ScanResponse(BaseModel):
    risk_score: int
    risk_level: str  # SAFE, WARNING, CRITICAL
    analysis_time_ms: float
    flags: List[str] # Detailed reasons
    action: str      # ALLOW, WARN, BLOCK

class ReportRequest(BaseModel):
    sender: str
    message: str
    category: str # e.g. "Phishing", "Extortion"