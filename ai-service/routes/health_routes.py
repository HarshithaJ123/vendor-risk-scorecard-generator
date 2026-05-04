from flask import Blueprint, jsonify
from services.health_service import get_health_status

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health():
    return jsonify(get_health_status())