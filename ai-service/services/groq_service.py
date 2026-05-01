import json
import re
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

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

        
