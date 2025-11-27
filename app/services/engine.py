from fuzzywuzzy import fuzz
import re
import time
# IMPORTANT: Added SAFE_PATTERNS to the import
from app.core.patterns import SCAM_PATTERNS, SAFE_PATTERNS, WEIGHTS, WHITELIST
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
        print(f"🔍 ANALYZING: {text[:50]}... from {sender}")

        # --- LAYER 0: WHITELIST (Trust) ---
        if sender_upper in WHITELIST:
            print("   ✅ Whitelisted Sender")
            return 0, "SAFE", ["Verified Trusted Sender"], "ALLOW", 0.0

        # --- LAYER 0.5: SAFE PATTERN CHECK (Context Awareness) ---
        # We check this first. If it looks like a receipt, we flag it as 'Transactional'.
        is_transactional = False
        for pattern in SAFE_PATTERNS:
            if re.search(pattern, text_lower):
                print(f"   ✅ Match Safe Pattern: {pattern}")
                is_transactional = True
                break

        # --- LAYER 1: REGEX CHECKS ---
        
        # A. Technical (USSD/Links)
        for pattern in SCAM_PATTERNS["technical_attack"]:
            if re.search(pattern, text_lower):
                print(f"   ⚠️ Match Technical: {pattern}")
                score += WEIGHTS["technical_attack"]
                flags.append("⚠️ Technical Threat Detected")
                break 

        # B. Threats & Extortion (High Danger)
        # We track if a threat exists, because threats are NEVER safe (even in receipts).
        has_threat = False
        if "threats" in SCAM_PATTERNS:
            for pattern in SCAM_PATTERNS["threats"]:
                if re.search(pattern, text_lower):
                    print(f"   ⚠️ Match Threat: {pattern}")
                    score += WEIGHTS["threats"]
                    flags.append("⛔ EXTORTION/THREAT DETECTED")
                    has_threat = True
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

        # --- LOGIC CORRECTION: FALSE POSITIVE SUPPRESSION ---
        # If the message matches a SAFE PATTERN (like a receipt) AND contains no violent threats:
        # We assume the "Urgency" or "Social" flags are just standard banking language.
        if is_transactional and not has_threat:
            print("   📉 Transactional Context Detected: Suppressing False Positives.")
            score = 0
            flags = [] # Clear the flags

        print(f"   📊 Score before AI: {score}")

        # --- LAYER 2: AI ---
        # Only call AI if we haven't already blocked it, and logic isn't already 0 (Safe)
        if score < settings.CRITICAL_SCORE:
            try:
                # IMPORTANT: We pass 'sender' to the AI now for better context
                ai_score, ai_label = self.ai.predict_intent(text, sender)
                print(f"   🤖 AI Result: {ai_label} ({ai_score})")
                
                if ai_label != "AI_OFFLINE":
                    # If we already determined it's transactional/safe, 
                    # we ignore the AI unless it is EXTREMELY confident (95%+) it's a scam.
                    if is_transactional:
                        if ai_score > 95:
                            score = max(score, ai_score)
                            flags.append(f"🤖 AI Override: {ai_label}")
                    else:
                        # Normal behavior: Trust the highest score
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
    




def analyze(self, text: str, sender: str):
        # ... (Regex Layers run first) ...
        # Regex finds "imefungiwa" -> Score = 30.
        
        # ... (AI Layer) ...
        ai_score, ai_label = self.ai.predict_intent(text)
        
        if ai_label == "OFFLINE_MODE":
            # If offline, we multiply the Regex score to be more aggressive (Safety First)
            # If we suspect a scam but can't ask the AI, we assume it IS a scam.
            if score > 0:
                print("   ⚠️ Offline: Boosting Regex Confidence")
                score = min(score * 1.5, 100) # Boost score by 50%
        
        # ... (Rest of logic) ...