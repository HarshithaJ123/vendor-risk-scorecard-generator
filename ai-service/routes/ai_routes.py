from flask import Blueprint, request, jsonify
from services.prompt_loader import load_prompt
from services.groq_service import get_ai_response as call_groq
from datetime import datetime
import json

ai_routes = Blueprint("ai_routes", __name__)


# ✅ Safe JSON extractor (FINAL)
def extract_json(text):
    import json
    import ast
    import re

    if not text:
        return {}

    text = str(text)

    # Remove markdown ```json ```
    text = re.sub(r"```json|```", "", text).strip()

    # ✅ Try normal JSON
    try:
        return json.loads(text)
    except:
        pass

    # ✅ Try Python dict (single quotes)
    try:
        return ast.literal_eval(text)
    except:
        pass

    # ✅ Try extracting JSON inside text
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group()
            try:
                return json.loads(json_str)
            except:
                return ast.literal_eval(json_str)
    except:
        pass

    return {}

       


@ai_routes.route("/analyze", methods=["POST"])
def analyze_vendor():
    try:
        data = request.json

        # ✅ 1. Validate input
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        vendor = data.get("vendor")
        risk_score = data.get("risk_score")

        if not vendor:
            return jsonify({"error": "vendor is required"}), 400

        # ✅ 2. Load prompts
        describe_prompt = load_prompt("vendor_prompt.txt")
        recommend_prompt = load_prompt("recommend_prompt.txt")

        # ✅ 3. Format prompts
        describe_final = describe_prompt.format(
            vendor=vendor,
            risk_score=risk_score
        )

        recommend_final = recommend_prompt.format(
            vendor=vendor,
            risk_score=risk_score
        )

        # ✅ 4. Call AI (force string)
        describe_res = (call_groq(describe_final))
        recommend_res = (call_groq(recommend_final))

        print("RAW DESCRIBE:", repr(describe_res))
        print("RAW RECOMMEND:", repr(recommend_res))
        print("PARSED:", describe_json)

        # ✅ 5. Extract JSON safely
        describe_json = extract_json(describe_res)
        recommend_json = extract_json(recommend_res)

        # ✅ 6. Final response (mentor format)
        return jsonify({
            "risk_level": describe_json.get("risk_level", "High"),
            "reasons": describe_json.get("reasons", ["AI response issue"]),
            "recommendations": recommend_json.get("recommendations", [
                {
                    "action_type": "Fix",
                    "description": "AI returned invalid JSON",
                    "priority": "Medium"
                }
            ]),
            "generated_at": datetime.utcnow().isoformat()
        })

    except Exception as e:
        print("ERROR OCCURRED:", str(e))
        return jsonify({"error": str(e)}), 500