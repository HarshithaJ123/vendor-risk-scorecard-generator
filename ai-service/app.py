from flask import Flask

# Import blueprints
from routes.ai_routes import ai_routes
from routes.recommend_routes import recommend_bp   # ✅ ADD THIS
from routes.recommend_routes import recommend_bp
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
def home():
    return {"message": "AI Service is running 🚀"}

# ✅ Run server
if __name__ == "__main__":
    app.run(debug=True)