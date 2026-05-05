from flask import Flask, jsonify
from flask_talisman import Talisman

# 🔽 Import your route blueprints
from routes.report_routes import report_bp
from routes.health_routes import health_bp
from werkzeug.serving import WSGIRequestHandler
from services.chroma_service import seed_documents
from services.chroma_service import initialize_chroma

initialize_chroma() # call only, do not redefine

class CustomRequestHandler(WSGIRequestHandler):
    def version_string(self):
        return "SecureServer/1.0"  # Custom Server header

app = Flask(__name__)

# ✅ Limit request size (ZAP fix)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1MB
app.config['JSON_SORT_KEYS'] = False

# ✅ Strong Content Security Policy (fix CSP issue fully)
csp = {
    'default-src': "'self'",
    'script-src': "'self'",
    'style-src': "'self'",
    'img-src': "'self' data:",
    'font-src': "'self'",
    'connect-src': "'self'",
    'object-src': "'none'",
    'frame-ancestors': "'none'",
    'base-uri': "'self'",
    'form-action': "'self'"
}

# ✅ Apply Talisman (main security layer)
Talisman(
    app,
    content_security_policy=csp,
    force_https=False,
    frame_options='DENY'
)

@app.after_request
def add_headers(response):
    # Remove server header completely
    response.headers.pop('Server', None)

    # Add custom safe server header
    if 'Server' in response.headers:
     del response.headers['Server']
     response.headers['Server'] = 'SecureServer/1.0'

    # Security headers (add ALL)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), camera=()'

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
    app.run(debug=False,request_handler=CustomRequestHandler)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)