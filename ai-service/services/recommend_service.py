from services.groq_service import get_ai_response
from services.prompt_loader import load_prompt
from datetime import datetime
import json

def safe_parse(text):
    try:
        text = str(text)

        # Extract JSON part
        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end != -1:
            return json.loads(text[start:end])

    except Exception as e:
        print("PARSE ERROR:", str(e))

    return {}

def generate_full_analysis(vendor, risk_score):
    try:
        # ✅ Step 1: Risk Analysis
        risk_prompt = load_prompt("vendor_prompt.txt")\
                        .replace("{vendor}", vendor)\
                        .replace("{risk_score}", risk_score)

        risk_res = get_ai_response(risk_prompt)
        print("RISK RAW:", risk_res)

        risk_json = safe_parse(risk_res)

        # ✅ Step 2: Recommendations
        rec_prompt = load_prompt("recommend_prompt.txt")\
                        .replace("{vendor}", vendor)\
                        .replace("{risk_score}", risk_score)

        rec_res = get_ai_response(rec_prompt)
        print("REC RAW:", rec_res)

        rec_json = safe_parse(rec_res)

        # ✅ FINAL RESPONSE
        return {
            "risk_level": risk_json.get("risk_level", "High"),
            "reasons": risk_json.get("reasons", ["AI parsing issue"]),
            "recommendations": rec_json.get("recommendations", [
                {
                    "action_type": "Fix",
                    "description": "AI returned invalid JSON",
                    "priority": "Medium"
                }
            ]),

def generate_full_analysis(vendor, risk_score):

    # ✅ Initialize variables (IMPORTANT FIX)
    risk_result = {}
    rec_result = []

    try:
        # -------------------------
        # Step 1: Risk Analysis (Day 3)
        # -------------------------
        risk_prompt = load_prompt("vendor_prompt.txt") \
            .replace("{vendor}", vendor) \
            .replace("{risk_score}", risk_score)

        risk_result = get_ai_response(risk_prompt)

        print("=== RISK RESULT ===", risk_result)

        # -------------------------
        # Step 2: Recommendations (Day 4)
        # -------------------------
        rec_prompt = load_prompt("recommend_prompt.txt") \
            .replace("{vendor}", vendor) \
            .replace("{risk_score}", risk_score)

        rec_result = get_ai_response(rec_prompt)

        print("=== REC RESULT ===", rec_result)

        # -------------------------
        # Step 3: Combine (Day 5)
        # -------------------------
        return {
            "risk_level": risk_result.get("risk_level", "Unknown"),
            "reasons": risk_result.get("reasons", []),
            "recommendations": rec_result if isinstance(rec_result, list) else [],
            "generated_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "error": "AI failure",
            "details": str(e)
        return {
            "error": "AI failure",
            "details": str(e),
            "risk_level": "Unknown",
            "reasons": [],
            "recommendations": []
        }