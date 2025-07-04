from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.book_schemas import ReviewInput, StatusInput
from database import db
from models.book import Book
from models.user_book import UserBook
from services.google_books import get_book_by_id, search_google_books
import requests

book_bp = Blueprint("books", __name__, url_prefix="/api/user/books")


@book_bp.route("", methods=["GET"])
@jwt_required()
def get_user_books():
    """
    Retorna todos os livros avaliados pelo usuário autenticado.
    ---
    tags:
      - Livros
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de livros avaliados pelo usuário
        content:
          application/json:
            schema:
              type: object
              properties:
                books:
                  type: array
                  items:
                    type: object
                    properties:
                      google_id:
                        type: string
                        example: "aog0vgAACAAJ"
                      title:
                        type: string
                        example: "A Amiga Genial"
                      author:
                        type: string
                        example: "Elena Ferrante"
                      image:
                        type: string
                        example: "https://books.google.com/thumbnail?id=abc123"
                      rating:
                        type: integer
                        example: 5
                      comment:
                        type: string
                        example: "Um livro maravilhoso!"
                      status:
                        type: string
                        example: "lido"
    """
    user_id = int(get_jwt_identity())
    user_books = (
        db.session.query(UserBook, Book)
        .join(Book, UserBook.book_id == Book.id)
        .filter(UserBook.user_id == user_id)
        .all()
    )

    result = []
    for user_book, book in user_books:
        result.append({
            "google_id": book.google_id,
            "title": book.title,
            "author": book.author,
            "image": book.image,
            "rating": user_book.rating,
            "comment": user_book.comment,
            "status": user_book.status
        })

    return jsonify({"books": result}), 200


@book_bp.route("/search", methods=["GET"])
def search_books():
    """
    Busca livros pela query na Google Books API.
    ---
    tags:
      - Livros
    parameters:
      - name: query
        in: query
        schema:
          type: string
        required: true
        description: Termo para busca de livros
    responses:
      200:
        description: Lista de livros encontrados
        content:
          application/json:
            schema:
              type: object
              properties:
                items:
                  type: array
                  items:
                    type: object
    """
    query = request.args.get("query")
    if not query:
        return {"message": "Parâmetro 'query' é obrigatório"}, 400
    books = search_google_books(query)
    return jsonify(books)


@book_bp.route("/<string:google_id>", methods=["POST"])
@jwt_required()
def create_user_book_review(google_id):
    """
    Cria uma avaliação de livro para o usuário.
    ---
    tags:
      - Livros
    security:
      - Bearer: []
    parameters:
      - name: google_id
        in: path
        schema:
          type: string
        required: true
        description: ID do livro no Google Books
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - rating
            - comment
            - status
          properties:
            rating:
              type: integer
              example: 4
            comment:
              type: string
              example: "Na releitura, gostei ainda mais"
            status:
              type: string
              enum: [lido, lendo]
              example: lendo
    responses:
      201:
        description: Avaliação criada com sucesso
      400:
        description: Erro de validação
      404:
        description: Livro não encontrado
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    rating = data.get("rating")
    comment = data.get("comment")
    status = data.get("status")

    if not all([rating, comment, status]):
        return {"message": "Campos rating, comment e status são obrigatórios."}, 400

    google_data = requests.get(f"https://www.googleapis.com/books/v1/volumes/{google_id}").json()
    volume_info = google_data.get("volumeInfo", {})
    title = volume_info.get("title", "Título desconhecido")
    authors = volume_info.get("authors", [])
    image_links = volume_info.get("imageLinks", {})
    thumbnail = image_links.get("thumbnail")

    book = Book.query.filter_by(google_id=google_id).first()
    if not book:
        book = Book(
            google_id=google_id,
            title=title,
            author=", ".join(authors) if authors else "Autor desconhecido",
            image=thumbnail
        )
        db.session.add(book)
        db.session.commit()

    existing_review = UserBook.query.filter_by(user_id=user_id, book_id=book.id).first()
    if existing_review:
        return {"message": "Avaliação já existe. Use PUT para atualizar."}, 400

    user_book = UserBook(
        user_id=user_id,
        book_id=book.id,
        rating=rating,
        comment=comment,
        status=status
    )

    db.session.add(user_book)
    db.session.commit()

    return {"message": "Avaliação criada com sucesso"}, 201


@book_bp.route("/<string:google_id>", methods=["PUT"])
@jwt_required()
def update_user_book_review(google_id):
    """
    Atualiza uma avaliação existente de livro para o usuário.
    ---
    tags:
      - Livros
    security:
      - Bearer: []
    parameters:
      - name: google_id
        in: path
        schema:
          type: string
        required: true
        description: ID do livro no Google Books
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - rating
            - comment
            - status
          properties:
            rating:
              type: integer
              example: 4
            comment:
              type: string
              example: "Na releitura, gostei ainda mais"
            status:
              type: string
              enum: [lido, lendo]
              example: lendo
    responses:
      201:
        description: Avaliação criada com sucesso
      400:
        description: Erro de validação
      404:
        description: Livro não encontrado
    """
    user_id = int(get_jwt_identity())
    body = request.get_json()
    try:
        data = ReviewInput(**body)
    except Exception as e:
        return {"message": f"Erro de validação: {str(e)}"}, 400

    user_book = UserBook.query.join(Book).filter(Book.google_id == google_id, UserBook.user_id == user_id).first()

    if not user_book:
        return {"message": "Avaliação não encontrada"}, 404

    user_book.rating = data.rating
    user_book.comment = data.comment
    user_book.status = data.status
    db.session.commit()
    return {"message": "Avaliação atualizada com sucesso"}, 200


@book_bp.route("/<string:google_id>", methods=["DELETE"])
@jwt_required()
def delete_user_book_review(google_id):
    """
    Remove a avaliação do usuário para um livro.
    ---
    tags:
      - Livros
    security:
      - Bearer: []
    parameters:
      - name: google_id
        in: path
        schema:
          type: string
        required: true
        description: ID do livro no Google Books
    responses:
      200:
        description: Avaliação removida com sucesso
      404:
        description: Avaliação não encontrada
    """
    user_id = int(get_jwt_identity())
    user_book = UserBook.query.join(Book).filter(Book.google_id == google_id, UserBook.user_id == user_id).first()
    if not user_book:
        return {"message": "Avaliação não encontrada"}, 404
    db.session.delete(user_book)
    db.session.commit()
    return {"message": "Avaliação removida com sucesso"}, 200


@book_bp.route("/<string:google_id>/status", methods=["PATCH"])
@jwt_required()
def update_book_status(google_id):
    """
    Atualiza somente o status da avaliação do livro.
    ---
    tags:
      - Livros
    security:
      - Bearer: []
    parameters:
      - name: google_id
        in: path
        type: string
        required: true
        description: ID do livro no Google Books
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - status
          properties:
            status:
              type: string
              enum:
                - lido
                - lendo
              example: lido
    responses:
      200:
        description: Status atualizado com sucesso
      400:
        description: Status inválido
      404:
        description: Avaliação não encontrada
    """
    user_id = int(get_jwt_identity())
    body = request.get_json()
    try:
        data = StatusInput(**body)
    except Exception as e:
        return {"message": f"Erro de validação: {str(e)}"}, 400

    if data.status not in ["lido", "lendo"]:
        return {"message": "Status inválido"}, 400

    user_book = UserBook.query.join(Book).filter(Book.google_id == google_id, UserBook.user_id == user_id).first()
    if not user_book:
        return {"message": "Review não encontrada"}, 404

    user_book.status = data.status
    db.session.commit()
    return {"message": f"Status atualizado para {data.status}"}, 200