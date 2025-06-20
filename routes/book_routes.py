from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.google_books import get_book_by_id, search_google_books
from database import db
from models.book import Book
from models.user_book import UserBook

book_bp = Blueprint("books", __name__)

@book_bp.route("/api/user/books/<google_id>", methods=["POST"])
@jwt_required()
def add_user_book(google_id):
    data = request.get_json()
    rating = data.get("rating")
    comment = data.get("comment")

    if not rating or not comment:
        return {"message": "Campos obrigatórios ausentes"}, 400

    user_id = get_jwt_identity()

    book = Book.query.filter_by(google_id=google_id).first()

    if not book:
        book_data = get_book_by_id(google_id)
        if not book_data:
            return {"message": "Livro não encontrado na Google Books API"}, 404

        title = book_data["volumeInfo"].get("title", "Título desconhecido")
        authors = book_data["volumeInfo"].get("authors", ["Autor desconhecido"])
        author = ", ".join(authors)

        book = Book(google_id=google_id, title=title, author=author)
        db.session.add(book)
        db.session.commit()


    user_book = UserBook(user_id=user_id, book_id=book.id, rating=rating, comment=comment)
    db.session.add(user_book)
    db.session.commit()

    return {"message": "Livro avaliado com sucesso"}, 201

@book_bp.route("/api/search", methods=["GET"])
def search_books():
    query = request.args.get("q")
    if not query:
        return {"message": "Parâmetro 'q' obrigatório"}, 400

    books = search_google_books(query)
    return jsonify(books), 200