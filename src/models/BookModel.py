from api import db
from marshmallow import fields, Schema, validate


# Create a model for books entity with table name as books
class BookModel(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), nullable=False)
    book_author = db.Column(db.String(255), nullable=False)
    book_available = db.Column(db.Boolean, default=True)
    borrowed = db.relationship('BorrowModel', backref='books', lazy='dynamic')

    def __init__(self, _id, name, author_name, available=True):
        self.book_id = _id
        self.book_name = name
        self.book_author = author_name
        self.book_available = available

    def add(self):
        if not self.check():
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    def check(self):
        return db.session.query(self.__class__).get(self.book_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BookSchema(Schema):
    book_id = fields.Int(required=True)
    book_name = fields.Str(required=True, validate=validate.Length(min=1))
    book_author = fields.Str(required=True, validate=validate.Length(min=1))
    book_available = fields.Bool(required=False)
