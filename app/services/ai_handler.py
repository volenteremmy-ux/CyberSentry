import requests
import google.generativeai as genai
import json
from app.core.config import settings

class AIHandler:
    def __init__(self):
        # Setup Hugging Face
        self.hf_headers = {"Authorization": f"Bearer {settings.HF_API_KEY}"}
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def predict_intent(self, text: str, sender: str):
        """
        Tries HuggingFace -> Fails? -> Tries Gemini -> Fails? -> Returns 0 (Hardcoded Fallback)
        """
        
        # --- ATTEMPT 1: HUGGING FACE (Zero-Shot) ---
        print("   🔹 Attempting Hugging Face...")
        try:
            payload = {
                "inputs": text,
                "parameters": {"candidate_labels": ["urgent scam", "money request", "safe"]}
            }
            response = requests.post(
                settings.HF_MODEL_URL, 
                headers=self.hf_headers, 
                json=payload, 
                timeout=settings.HF_TIMEOUT # 2 Seconds Max
            )
            
            if response.status_code == 200:
                data = response.json()
                top_label = data['labels'][0]
                confidence = data['scores'][0]
                
                # Normalize Score
                if top_label == "urgent scam": return int(confidence * 100), "HF_SCAM"
                if top_label == "money request": return int(confidence * 60), "HF_SUSPICIOUS"
                return 0, "HF_SAFE"
            
            else:
                print(f"   ⚠️ HF Error {response.status_code}. Switching to Gemini...")

        except Exception as e:
            print(f"   ⚠️ HF Timeout/Fail: {e}. Switching to Gemini...")


        # --- ATTEMPT 2: GOOGLE GEMINI (Generative) ---
        print("   🔸 Attempting Gemini Flash...")
        try:
            # IMPROVED PROMPT
            prompt = f"""
            Act as a bank fraud security expert. Analyze this message context.
            
            Sender: "{sender}"
            Message: "{text}"
            
            Rules:
            1. If this is a standard transaction receipt, low balance alert, or decline notification, return risk_score: 0.
            2. Legitimate banks DO ask users to call a toll-free number for support. This is SAFE.
            3. ONLY flag as fraud if it asks for a PIN, demands an immediate transfer to a random number, or threatens the user.
            
            Return ONLY JSON: {{"risk_score": 0-100, "label": "reason"}}
            """
            
            response = self.gemini_model.generate_content(prompt)
            result_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(result_text)
            
            return data.get("risk_score", 0), f"GEMINI_{data.get('label', 'Analyzed').upper()}"

        except Exception as e:
            print(f"   ⚠️ Gemini Fail: {e}")
            return 0, "AI_OFFLINE"

        return 0, "AI_OFFLINE"
    





import requests
import google.generativeai as genai
from app.core.config import settings

class AIHandler:
    def __init__(self):
        # We simulate the internet status
        self.is_online = True  # Change to False to test offline mode

    def predict_intent(self, text: str):
        # 1. CHECK CONNECTIVITY
        if not self.is_online:
            print("   📶 DEVICE OFFLINE. Skipping Cloud AI.")
            return 0, "OFFLINE_MODE"

        # 2. PROCEED TO CLOUD (Hugging Face / Gemini)
        # ... (Rest of your existing cloud code) ... 