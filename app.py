from flask import Flask, jsonify
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from database import db
from routes.book_routes import book_bp
from routes.auth_routes import auth_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    JWTManager(app)
    Swagger(app, template=app.config['SWAGGER_TEMPLATE'], config=app.config['SWAGGER_CONFIG'])
    with app.app_context():
        db.create_all()  

    app.register_blueprint(book_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return jsonify({"message": "BookSync API está rodando!"})

    return app

app = create_app()
