from flask import Blueprint, request, jsonify
from services.report_service import generate_report
from services.chroma_service import query_knowledge
import re

report_bp = Blueprint('report', __name__)

# 🔐 Input sanitization
def sanitize_input(value):
    if not value:
        return ""
    return re.sub(r'[^a-zA-Z0-9\s]', '', value)

@report_bp.route('/generate-report', methods=['POST'])
def report():
    try:
        # ✅ Safe JSON parsing
        data = request.get_json(silent=True)

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        vendor = sanitize_input(data.get('vendor'))
        risk_score = sanitize_input(data.get('risk_score', 'Medium'))

        # ✅ Required field check
        if not vendor:
            return jsonify({"error": "Vendor required"}), 400

        #new chromadb knowledge base query
        knowledge = query_knowledge(risk_score)
        result = {
            "vendor": vendor,
            "risk": risk_score,
            "insights": knowledge
        }

        # ✅ Ensure valid response
        if not result:
            return jsonify({"error": "No response from AI"}), 500

        return jsonify(result), 200

    except Exception as e:
        print("🔥 ERROR in /generate-report:", str(e))  # important debug
        return jsonify({"error": "Internal Server Error"}), 500