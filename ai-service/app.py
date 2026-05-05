from flask import Flask, jsonify
from flask_talisman import Talisman

# Import blueprints
from routes.ai_routes import ai_routes
from routes.recommend_routes import recommend_bp   # ✅ ADD THIS
from routes.recommend_routes import recommend_bp
# 🔽 Import your route blueprints
from routes.report_routes import report_bp
from routes.health_routes import health_bp

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
# ✅ Register blueprints with prefix
app.register_blueprint(ai_routes, url_prefix="/ai")
app.register_blueprint(recommend_bp, url_prefix="/ai")

app.register_blueprint(report_bp, url_prefix="/ai")
app.register_blueprint(health_bp, url_prefix="/ai")
app.register_blueprint(recommend_bp, url_prefix="/ai")

# ✅ Health check route
@app.route("/")

# ✅ Limit request size (ZAP fix)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1MB
app.config['JSON_SORT_KEYS'] = False  # keep response order stable

# ✅ Content Security Policy
csp = {
    'default-src': "'self'"
}

# ✅ Apply security headers via Talisman
Talisman(app, content_security_policy=csp, force_https=False,frame_options='DENY')

# ✅ Additional Security Headers (only extra ones)
@app.after_request
def add_headers(response):
    response.headers.setdefault('X-Content-Type-Options', 'nosniff')
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers.setdefault('X-XSS-Protection', '1; mode=block')
    response.headers.setdefault('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
    
    # Hide server info (ZAP fix)
    response.headers.pop('Server', None)

    return response

# ✅ Root route
@app.route('/')
def home():
    return jsonify({"message": "API running securely"}), 200

# ✅ Register Blueprints
app.register_blueprint(report_bp, url_prefix='/ai')
app.register_blueprint(health_bp, url_prefix='/ai')

# ✅ Run server
if __name__ == "__main__":
    app.run(debug=True)