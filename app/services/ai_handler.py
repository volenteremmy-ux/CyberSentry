import requests
import google.generativeai as genai
import json
from app.core.config import settings

class AIHandler:
    def __init__(self):
        # Setup Hugging Face
        self.hf_headers = {"Authorization": f"Bearer {settings.HF_API_KEY}"}
        
        # Setup Google Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def predict_intent(self, text: str):
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
            # We use a strict prompt to get a JSON response
            prompt = f"""
            Analyze this SMS for fraud. 
            Text: "{text}"
            Return ONLY a JSON object: {{"risk_score": 0-100, "label": "reason"}}
            """
            
            # We assume Gemini is fast, but we wrap in a general try block
            # Note: The Python SDK handles timeouts differently, but 'flash' is usually < 1s
            response = self.gemini_model.generate_content(prompt)
            
            # Clean the response text to find JSON
            result_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(result_text)
            
            return data.get("risk_score", 0), f"GEMINI_{data.get('label', 'Analyzed').upper()}"

        except Exception as e:
            print(f"   ⚠️ Gemini Fail: {e}. Falling back to Regex.")

        
        # --- ATTEMPT 3: FALLBACK (Hardcoded) ---
        # If we reach here, both AIs failed. Return 0 so the Regex engine takes over.
        return 0, "AI_OFFLINE"