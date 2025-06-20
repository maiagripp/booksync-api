from flask import Blueprint, request, jsonify
from database import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return {"message": "Dados incompletos"}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"message": "Usuário já existe"}, 409

    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return {"message": "Usuário criado com sucesso"}, 201
