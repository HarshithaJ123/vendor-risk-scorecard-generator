from flask import Blueprint, request, jsonify
from services.report_service import generate_report

report_bp = Blueprint('report', __name__)

@report_bp.route('/generate-report', methods=['POST'])
def report():
    try:
        data = request.json

        if not data or 'vendor' not in data:
            return jsonify({"error": "Vendor required"}), 400

        vendor = data['vendor']
        risk_score = data.get('risk_score', 'Medium')

        result = generate_report(vendor, risk_score)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500