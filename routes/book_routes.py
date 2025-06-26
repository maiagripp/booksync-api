from flask_openapi3 import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from services.google_books import get_book_by_id, search_google_books
from models.book import Book
from models.user_book import UserBook
from schemas.book_schemas import PathGoogleID, ReviewInput, StatusInput, SearchQuery

book_bp = APIBlueprint("books", __name__, url_prefix="/api/user/books")

@book_bp.get("/search")
def search_books(query: SearchQuery):
    """Busca livros na API do Google Books."""
    books = search_google_books(query.query)
    return books, 200

# --- CORREÇÃO AQUI: Adicionada a barra "/" no início ---
@book_bp.post("/{google_id}")
@jwt_required()
def add_user_book(path: PathGoogleID, body: ReviewInput):
    """Adiciona um novo livro e review para o usuário."""
    google_id = path.google_id
    user_id = int(get_jwt_identity())

    if body.status not in ["lendo", "lido"]:
        return {"message": "Status inválido"}, 400

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

    existing_user_book = UserBook.query.filter_by(user_id=user_id, book_id=book.id).first()
    if existing_user_book:
        return {"message": "Você já adicionou este livro. Use a rota PUT para atualizá-lo."}, 409
    
    user_book = UserBook(user_id=user_id, book_id=book.id, rating=body.rating, comment=body.comment, status=body.status)
    db.session.add(user_book)
    db.session.commit()

    return {"message": "Livro avaliado com sucesso"}, 201

# --- CORREÇÃO AQUI: Adicionada a barra "/" no início ---
@book_bp.put("/{google_id}")
@jwt_required()
def update_or_create_user_book(path: PathGoogleID, body: ReviewInput):
    google_id = path.google_id
    user_id = int(get_jwt_identity())
    user_book = UserBook.query.join(Book).filter(Book.google_id == google_id, UserBook.user_id == user_id).first()
    if not user_book:
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
        user_book = UserBook(user_id=user_id, book_id=book.id, rating=body.rating, comment=body.comment, status=body.status)
        db.session.add(user_book)
        db.session.commit()
        return {"message": "Review criada com sucesso"}, 201
    user_book.rating = body.rating
    user_book.comment = body.comment
    user_book.status = body.status
    db.session.commit()
    return {"message": "Review atualizada com sucesso"}, 200

# --- CORREÇÃO AQUI: Adicionada a barra "/" no início ---
@book_bp.delete("/{google_id}")
@jwt_required()
def delete_user_book(path: PathGoogleID):
    """Deleta a review de um livro para o usuário."""
    google_id = path.google_id
    user_id = int(get_jwt_identity())
    user_book = UserBook.query.join(Book).filter(Book.google_id == google_id, UserBook.user_id == user_id).first()
    if not user_book:
        return {"message": "Review não encontrada"}, 404
    db.session.delete(user_book)
    db.session.commit()
    return {"message": "Review removida com sucesso"}, 200

# --- CORREÇÃO AQUI: Adicionada a barra "/" no início ---
@book_bp.patch("/{google_id}/status")
@jwt_required()
def update_book_status(path: PathGoogleID, body: StatusInput):
    """Atualiza apenas o status de um livro (lido/lendo)."""
    google_id = path.google_id
    if body.status not in ["lido", "lendo"]:
        return {"message": "Status inválido"}, 400
    user_id = int(get_jwt_identity())
    user_book = UserBook.query.join(Book).filter(Book.google_id == google_id, UserBook.user_id == user_id).first()
    if not user_book:
        return {"message": "Review não encontrada"}, 404
    user_book.status = body.status
    db.session.commit()
    return {"message": f"Status atualizado para {body.status}"}, 200
