import json
import re
import os
import time
from groq import Groq
from dotenv import load_dotenv
from services.health_service import record_response_time
from services.cache_service import get_cache, set_cache, generate_key
from services.model_service import get_model

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# FALLBACK RESPONSE
def fallback_response():

    return {
        "risk_level": "Medium",
        "reasons": [
            "AI service temporarily unavailable",
            "Fallback response generated"
        ],
        "recommendations": [
            {
                "action_type": "Security",
                "description": "Retry AI request later",
                "priority": "Medium"
            }
        ],
        "is_fallback": True
    }

# MAIN AI FUNCTION
def get_ai_response(prompt):

    try:

        # Load embedding model
        model = get_model()

        # Generate embedding
        model.encode(prompt)

        # Generate cache key
        cache_key = generate_key(prompt)

        # Check cache
        cached = get_cache(cache_key)

        if cached:
            print("CACHE HIT")
            return cached

        print("CALLING GROQ AI")

        # Track response time
        start = time.time()

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        end = time.time()

        # Record response time
        record_response_time(end - start)

        # Extract response content
        content = response.choices[0].message.content

        print("\n=== RAW AI RESPONSE ===\n")
        print(content)

        # EXTRACT JSON OBJECT OR ARRAY
        json_match = re.search(
            r'(\{.*\})',
            content,
            re.DOTALL
        )

        # Try JSON array if object not found
        if not json_match:

            json_match = re.search(
                r'(\[.*\])',
                content,
                re.DOTALL
            )

        if not json_match:
            raise ValueError("No JSON found")

        json_text = json_match.group()

        # CLEAN JSON
        json_text = json_text.replace("\n", " ")

        json_text = re.sub(
            r',\s*}',
            '}',
            json_text
        )

        json_text = re.sub(
            r',\s*]',
            ']',
            json_text
        )

        print("\n=== CLEAN JSON ===\n")
        print(json_text)

        # SAFE JSON PARSING

        try:

            parsed = json.loads(json_text)

        except Exception:

            try:
                # Fix single quotes
                fixed_json = json_text.replace("'", '"')

                parsed = json.loads(fixed_json)

            except Exception:

                # Final fallback structure
                parsed = {
                    "risk_level": "Medium",
                    "reasons": [
                        "AI formatting issue",
                        "Fallback response used"
                    ],
                    "recommendations": [
                        {
                            "action_type": "Security",
                            "description": "Retry AI request later",
                            "priority": "Medium"
                        }
                    ]
                }

    
        # SAVE CACHE
        set_cache(cache_key, parsed)

        return parsed

    except Exception as e:

        print("\n=== GROQ ERROR ===\n")
        print(str(e))

        return fallback_response()