import json
import re
from groq import Groq
import os
import time
from services.health_service import record_response_time
from services.cache_service import get_cache, set_cache, generate_key
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

        # ✅ 1. Try direct JSON
        try:
            return json.loads(content)
        except:
            pass

        # ✅ 2. Clean markdown
        cleaned = re.sub(r"```json|```", "", content).strip()

        # ✅ 3. Try JSON again
        try:
            return json.loads(cleaned)
        except:
            pass

        # ✅ 4. Extract JSON OBJECT { ... }
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
            json_text = match.group()

            # Fix common issues
            json_text = json_text.replace("\n", " ").replace("\r", "")
            json_text = re.sub(r',\s*}', '}', json_text)
            json_text = re.sub(r',\s*]', ']', json_text)

            print("=== CLEAN OBJECT JSON ===")
            print(json_text)

            try:
                return json.loads(json_text)
            except:
                pass

        # ✅ 5. Extract JSON ARRAY [ ... ]
        match = re.search(r'\[.*\]', cleaned, re.DOTALL)
        if match:
            json_text = match.group()

            json_text = json_text.replace("\n", " ").replace("\r", "")
            json_text = re.sub(r',\s*}', '}', json_text)
            json_text = re.sub(r',\s*]', ']', json_text)

            print("=== CLEAN ARRAY JSON ===")
            print(json_text)

            try:
                return json.loads(json_text)
            except:
                pass

        # ❌ Final fallback
        return {
            "risk_level": "High",
            "reasons": ["AI parsing issue"],
            "recommendations": [
                {
                    "action_type": "Fix",
                    "description": "AI returned invalid JSON",
                    "priority": "Medium"
                }
            ]
        }

    except Exception as e:
        return {
            "error": "AI failure",
            "details": str(e)
        }

        
        # ✅ STEP 4: Extract JSON
        json_match = re.search(r'(\{.*\}|\[.*\])', content, re.DOTALL)
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

        # ✅ Fallback response
        return [
            {
                "action_type": "Review",
                "description": "AI response invalid, fallback triggered",
                "priority": "Medium"
            }
        ]
        # ✅ FIXED fallback (DICT not LIST)
        return fallback_response(vendor)
