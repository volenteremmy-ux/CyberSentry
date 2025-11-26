from fuzzywuzzy import fuzz
import re
import time
from app.core.patterns import SCAM_PATTERNS, WEIGHTS, WHITELIST
from app.core.config import settings
from app.services.ai_handler import AIHandler

class FraudEngine:
    def __init__(self):
        self.ai = AIHandler()

    def analyze(self, text: str, sender: str):
        start_time = time.time()
        score = 0
        flags = []
        
        text_lower = text.lower()
        sender_upper = sender.upper()
        
        # DEBUG PRINT
        print(f"🔍 ANALYZING: {text} from {sender}")

        # --- LAYER 0: WHITELIST ---
        if sender_upper in WHITELIST:
            print("   ✅ Whitelisted Sender")
            return 0, "SAFE", ["Verified Trusted Sender"], "ALLOW", 0.0

        # --- LAYER 1: REGEX CHECKS ---
        
        # A. Technical (USSD/Links)
        for pattern in SCAM_PATTERNS["technical_attack"]:
            if re.search(pattern, text_lower):
                print(f"   ⚠️ Match Technical: {pattern}")
                score += WEIGHTS["technical_attack"]
                flags.append("⚠️ Technical Threat Detected")
                break 

        # B. Threats & Extortion (NEW: Catches "kill her")
        # We check this BEFORE social engineering because it's more dangerous
        if "threats" in SCAM_PATTERNS:
            for pattern in SCAM_PATTERNS["threats"]:
                if re.search(pattern, text_lower):
                    print(f"   ⚠️ Match Threat: {pattern}")
                    score += WEIGHTS["threats"]
                    flags.append("⛔ EXTORTION/THREAT DETECTED")
                    break

        # C. Social Engineering (Keywords)
        for pattern in SCAM_PATTERNS["social_engineering"]:
             if re.search(pattern, text_lower):
                print(f"   ⚠️ Match Social: {pattern}")
                score += WEIGHTS["social_engineering"]
                flags.append(f"⚠️ Suspicious Keyword Match")
                break
        
        # D. Urgency
        for pattern in SCAM_PATTERNS["urgency"]:
             if re.search(pattern, text_lower):
                print(f"   ⚠️ Match Urgency: {pattern}")
                score += WEIGHTS["urgency"]
                flags.append(f"⏳ Urgency Detected")
                break

        print(f"   📊 Score before AI: {score}")

        # --- LAYER 2: AI ---
        # Only call AI if score is < CRITICAL to save time/money
        if score < settings.CRITICAL_SCORE:
            try:
                ai_score, ai_label = self.ai.predict_intent(text)
                print(f"   🤖 AI Result: {ai_label} ({ai_score})")
                
                if ai_label != "AI_OFFLINE":
                    # Trust the highest score
                    score = max(score, ai_score)
                    if ai_score > 40:
                        flags.append(f"🤖 AI Analysis: {ai_label}")
            except Exception as e:
                print(f"   ❌ AI Failed: {e}")

        # --- SCORING ---
        score = min(score, 100)
        
        if score >= settings.CRITICAL_SCORE:
            level = "CRITICAL"
            action = "BLOCK"
        elif score >= settings.WARNING_SCORE:
            level = "WARNING"
            action = "WARN"
        else:
            level = "SAFE"
            action = "ALLOW"

        if score == 0:
            flags.append("✅ Clean Scan")

        process_time = (time.time() - start_time) * 1000 
        return score, level, flags, action, process_time