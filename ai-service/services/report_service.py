from services.groq_service import get_ai_response
from services.prompt_loader import load_prompt
from services.cache_service import generate_key, get_cache, set_cache
from datetime import datetime
import time


def fallback_response(vendor, risk_score):
    return {
        "title": "Vendor Risk Report",
        "summary": "Fallback response due to AI error",
        "overview": f"Unable to fetch AI response for {vendor}. Using fallback.",
        "key_items": [],
        "recommendations": ["Please retry later"],
        "generated_at": datetime.now().isoformat(),
        "is_fallback": True
    }


def generate_report(vendor, risk_score):
    start_time = time.time()

    # 🔑 Generate cache key
    key = generate_key(vendor, risk_score)

    # ✅ Check cache
    cached_report = get_cache(key)
    if cached_report:
        cached_report["response_time"] = round(time.time() - start_time, 3)
        return cached_report

    try:
        # ✅ Load prompt
        prompt = load_prompt("report_prompt.txt") \
            .replace("{vendor}", vendor) \
            .replace("{risk_score}", risk_score)

        # ✅ Call AI (Groq)
        result = get_ai_response(prompt, vendor, risk_score)

        # ⚠️ Validate AI response
        if not isinstance(result, dict):
            result = {}

        # ✅ LIMIT TO 1 ITEM
        key_items = result.get("key_items", [])
        if isinstance(key_items, list):
         key_items = key_items[:1]

        recommendations = result.get("recommendations", [])
        if isinstance(recommendations, list):
         recommendations = recommendations[:1]

        response = {
       "title": result.get("title", "Vendor Risk Report"),
       "summary": result.get("summary", ""),
       "overview": result.get("overview", ""),
       "key_items": key_items,                 # ✅ fixed
       "recommendations": recommendations,     # ✅ fixed
       "generated_at": datetime.now().isoformat(),
       "is_fallback": False
}

    except Exception:
        # ✅ Day 9 fallback
        response = fallback_response(vendor, risk_score)

    # ✅ Save cache (even fallback allowed)
    set_cache(key, response)

    # ⏱ Add performance time
    response["response_time"] = round(time.time() - start_time, 2)

    return response