# from sqlalchemy import Column, Integer, String, Boolean, DateTime
# from sqlalchemy.sql import func
# from app.core.database import Base

# class ScamReport(Base):
#     __tablename__ = "scam_reports"

#     id = Column(Integer, primary_key=True, index=True)
#     sender = Column(String, index=True)      # e.g. "0722..."
#     message = Column(String)                 # e.g. "Tuma pesa..."
#     source = Column(String)                  # e.g. "WhatsApp"
#     risk_score = Column(Integer)             # e.g. 90
#     timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
#     # Is this confirmed as a scam? (For future admin panel)
#     verified = Column(Boolean, default=False)