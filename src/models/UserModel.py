from api import db
from marshmallow import fields, Schema, validate


# Create a model for user entity with table name as users.
class UserModel(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    borrows = db.relationship('BorrowModel', backref='users', lazy='dynamic')

    def __init__(self, _id, name):
        self.user_id = _id
        self.user_name = name

    def add(self):
        if not self.check():
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    def check(self):
        return db.session.query(self.__class__).get(self.user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(Schema):
    user_id = fields.Int(required=True)
    user_name = fields.Str(required=True, validate=validate.Length(min=1))
