from flask import Blueprint, request, jsonify
from services.groq_service import get_ai_response
from services.prompt_loader import load_prompt
from services.recommend_service import generate_full_analysis

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json

        if not data or 'vendor' not in data:
            return jsonify({"error": "Vendor input required"}), 400

        vendor = data['vendor']
        risk_score = data.get('risk_score', 'Medium')

        # ✅ Day 5 logic
        result = generate_full_analysis(vendor, risk_score)

        #DAY 5 logic
        result = generate_full_analysis(vendor,risk_score)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500