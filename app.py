from flask import Flask
from config import Config
from database import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import models

from routes.auth_routes import auth_bp
from routes.book_routes import book_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
JWTManager(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)

@app.route("/")
def index():
    return {"message": "API BookSync no ar"}

if __name__ == "__main__":
    app.run(debug=True)
