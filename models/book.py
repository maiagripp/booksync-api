from database import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(120))
