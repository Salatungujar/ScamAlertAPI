from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from routes.auth import auth_bp
from routes.blog import blog_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(blog_bp, url_prefix="/api")

@app.route('/')
def index():
    return {"status": "Scam Awareness API is running."}
