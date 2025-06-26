from database import db

class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    rating = db.Column(db.Integer)  # de 1 a 5
    comment = db.Column(db.Text)
    status = db.Column(db.String(10), default="lendo" )  # "reading", "completed", "dropped", etc.
