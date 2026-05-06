from flask import Blueprint, jsonify
from services.health_service import get_health_status
from datetime import datetime

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health():

    status = get_health_status()

    return jsonify({
        "status": status,
        "service": "AI Vendor Risk API",
        "timestamp": datetime.utcnow().isoformat()
    }), 200