# backend.py
from fastapi import FastAPI
from pydantic import BaseModel
from fuzzywuzzy import fuzz

app = FastAPI(title="Ulinzi Trust SDK API")

# 1. THE DATA MODEL
class TransactionContext(BaseModel):
    message_text: str       # The SMS or Clipboard text
    sender_id: str          # Who sent it? (e.g., +2547..., Safaricom)
    app_source: str         # e.g., "WhatsApp", "SMS"

# 2. THE KENYAN LOGIC ENGINE (The Brain)
def calculate_risk(text: str, sender: str):
    text_lower = text.lower()
    sender_lower = sender.lower()
    score = 0
    flags = []

    # A. SHENG/SWAHILI TRIGGERS (Intent Detection)
    danger_words = {
        "imefungwa": 30, "blocked": 30, "suspended": 30, 
        "tuma": 20, "dial": 20, "reverse": 20, 
        "pin": 20, "unlock": 20, "reward": 15, "zawadi": 15
    }
    
    urgency_words = ["haraka", "urgent", "immediately", "leo", "today", "now", "within"]

    # Check Keywords
    for word, weight in danger_words.items():
        if word in text_lower:
            score += weight
            flags.append(f"Threat Keyword: '{word}'")

    # Check Urgency
    for word in urgency_words:
        if word in text_lower:
            score += 20
            flags.append(f"Urgency Marker: '{word}'")

    # B. BRAND IMPERSONATION (Fuzzy Logic)
    # If sender looks like 'Safaricom' but isn't exact
    if "safaricom" in sender_lower and sender_lower != "safaricom":
        ratio = fuzz.ratio(sender_lower, "safaricom")
        if ratio > 60:
            score += 50
            flags.append("Fake Safaricom ID Detected")

    # C. COMBINATION LOGIC (The "Context")
    # Tuma + Number = High Risk
    if "tuma" in text_lower and any(char.isdigit() for char in text_lower):
        score += 25
        flags.append("Soliciting Money via Text")

    # Cap Score at 100
    if score > 100: score = 100
    
    # Decision
    status = "SAFE"
    if score > 75: status = "CRITICAL_BLOCK"
    elif score > 40: status = "WARNING"

    return {"score": score, "status": status, "reasons": flags}

# 3. THE API ENDPOINT
@app.post("/assess-risk")
def assess_risk(data: TransactionContext):
    result = calculate_risk(data.message_text, data.sender_id)
    return result

# Run with: uvicorn backend:app --reload