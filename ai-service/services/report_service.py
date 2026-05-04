from services.groq_service import get_ai_response
from services.prompt_loader import load_prompt
from services.cache_service import generate_key, get_cache, set_cache
from datetime import datetime

def generate_report(vendor, risk_score):
    # Generate a cache key
    key = generate_key(vendor, risk_score)

    # Try to get the report from cache
    cached_report = get_cache(key)
    if cached_report:
        return cached_report

    try:
        prompt = load_prompt("report_prompt.txt") \
            .replace("{vendor}", vendor) \
            .replace("{risk_score}", risk_score)

        result = get_ai_response(prompt, vendor, risk_score)

        if not isinstance(result, dict):
            result = {}

        # Normalize fields (ensure lists/dicts)
        key_items = result.get("key_items", [])
        if not isinstance(key_items, list):
            key_items = []

        recs = result.get("recommendations", [])
        if not isinstance(recs, list):
            recs = []

        # 🔥 FINAL NORMALIZED RESPONSE (ORDER FIXED)
        response = {
            "title": result.get("title", "Vendor Risk Report"),
            "summary": result.get("summary", ""),
            "overview": result.get("overview", ""),
            "key_items": result.get("key_items", []),
            "recommendations": result.get("recommendations", []),
            "generated_at": datetime.now().isoformat()
        }

        # save to cache
        set_cache(key, response)
        return response

    except Exception as e:
        return {
            "error": "Report generation failed",
            "details": str(e),
            "title": "",
            "summary": "",
            "overview": "",
            "key_items": [],
            "recommendations": [],
            "generated_at": datetime.now().isoformat()
        }