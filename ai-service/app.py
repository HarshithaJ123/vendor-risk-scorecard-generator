from flask import Flask, jsonify
from flask_talisman import Talisman
from werkzeug.serving import WSGIRequestHandler

# IMPORT BLUEPRINTS
from routes.report_routes import report_bp
from routes.health_routes import health_bp
from routes.ai_routes import ai_routes

# IMPORT CHROMA INITIALIZER
from services.chroma_service import initialize_chroma

# Initialize ChromaDB
initialize_chroma()

# CUSTOM SERVER HEADER
class CustomRequestHandler(WSGIRequestHandler):

    def version_string(self):
        return "SecureServer/1.0"


# CREATE FLASK APP
app = Flask(__name__)

# BASIC SECURITY SETTINGS
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1MB
app.config['JSON_SORT_KEYS'] = False

# CONTENT SECURITY POLICY
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

# APPLY TALISMAN SECURITY
Talisman(
    app,
    content_security_policy=csp,
    force_https=False,
    frame_options='DENY'
)

# ADD SECURITY HEADERS
@app.after_request
def add_headers(response):

    # Remove default server header
    response.headers.pop('Server', None)

    # Add custom safe server header
    response.headers['Server'] = 'SecureServer/1.0'

    # Security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), camera=()'

    return response

# ROOT ROUTE
@app.route('/')
def home():

    return jsonify({
        "message": "AI Vendor Risk API running securely"
    }), 200

# REGISTER BLUEPRINTS
app.register_blueprint(report_bp, url_prefix='/ai')
app.register_blueprint(health_bp, url_prefix='/ai')
app.register_blueprint(ai_routes, url_prefix='/ai')

# RUN APPLICATION
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )