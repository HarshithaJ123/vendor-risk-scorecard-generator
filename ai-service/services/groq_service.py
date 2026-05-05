import json
import re
from groq import Groq
import os
import time
from services.health_service import record_response_time
from services.cache_service import get_cache, set_cache, generate_key
from services.model_service import get_model
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def fallback_response(vendor):
    return {
        "title": "Vendor Risk Report",
        "summary": "Fallback response due to AI failure",
        "overview": f"AI failed for {vendor}, fallback used.",
        "key_items": [],
        "recommendations": ["Retry later"],
        "is_fallback": True
    }


def get_ai_response(prompt, vendor, risk_score):
    try:
        # 🔥 STEP 0: Load model (ADD HERE)
        model = get_model()
        embedding = model.encode(prompt)

        # 🔑 Cache key
        cache_key = generate_key(vendor, risk_score)

        # ⚡ Cache check
        cached = get_cache(cache_key)
        if cached:
            return cached

        print("🚀 CALLING AI")

        # ⏱ Track time
        start = time.time()

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        end = time.time()
        record_response_time(end - start)

        content = response.choices[0].message.content

        print("\n=== RAW AI RESPONSE ===\n", content)

        # ✅ Extract JSON
        json_match = re.search(r'(\{.*\})', content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found")

        json_text = json_match.group()

        # ✅ Clean JSON
        json_text = json_text.replace("\n", " ")
        json_text = re.sub(r',\s*}', '}', json_text)

        print("\n=== CLEAN JSON ===\n", json_text)

        parsed = json.loads(json_text)

        # ✅ Validate
        if not isinstance(parsed, dict):
            raise ValueError("Invalid format")

        parsed["is_fallback"] = False

        # 🔥 Save cache
        set_cache(cache_key, parsed)

        return parsed

    except Exception as e:
        print("\n=== ERROR ===\n", str(e))

        # ✅ FIXED fallback (DICT not LIST)
        return fallback_response(vendor)