from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from database import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registra novo usuário.
    ---
    tags:
      - Autenticação
    security: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
            - username
          properties:
            email:
              type: string
              example: teste@example.com
            password:
              type: string
              example: 123456
            username:
              type: string
              example: joaosilva
    responses:
      201:
        description: Usuário registrado com sucesso
      400:
        description: Email ou username já registrado ou dados inválidos
    """
    data = request.get_json()
    email = data.get("email")
    password = str(data.get("password"))
    username = data.get("username")

    if not email or not password or not username:
        return {"message": "Email, senha e nome de usuário são obrigatórios"}, 400

    if User.query.filter_by(email=email).first():
        return {"message": "Email já registrado"}, 400

    if User.query.filter_by(username=username).first():
        return {"message": "Nome de usuário já registrado"}, 400

    user = User(email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return {"message": "Usuário registrado com sucesso"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Realiza login e retorna token JWT.
    ---
    tags:
      - Autenticação
    security: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: teste@example.com
            password:
              type: string
              example: 123456
    responses:
      200:
        description: Login bem-sucedido com token JWT
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    email = data.get("email")
    password = str(data.get("password"))

    if not email or not password:
        return {"message": "Email e senha são obrigatórios"}, 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"message": "Email ou senha inválidos"}, 401

    access_token = create_access_token(identity=str(user.id))
    return {
        "access_token": access_token,
        "username": user.username
    }, 200
