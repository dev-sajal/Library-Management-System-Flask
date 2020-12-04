from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# app initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librarymanagement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db initialization
db = SQLAlchemy(app)
db.init_app(app)


@app.before_first_request
def create_db():
    db.create_all()


# Flask migrate app and db
migrate = Migrate(app=app, db=db)

# Register your views as blueprints here and the use the following prefixes.
from src.views.UserView import user_blueprint
from src.views.BookView import book_blueprint
from src.views.BorrowView import borrow_blueprint
from src.views.BillingView import bill_blueprint
# user_blueprint   ----> /users
app.register_blueprint(user_blueprint)
# book_blueprint   ----> /books
app.register_blueprint(book_blueprint)
# borrow_blueprint ----> /borrows
app.register_blueprint(borrow_blueprint)
# bill_blueprint   ----> /books
app.register_blueprint(bill_blueprint)
