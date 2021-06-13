
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, autoincrement=True)
    username = db.Column(db.String(20), primary_key = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hash_pwd = bcrypt.generate_password_hash(password)
        hashed_password_storeable = hash_pwd.decode("utf-8")

        new_user = User(username=username, password = hashed_password_storeable, email = email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)

        return new_user

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    
class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable = False)
    




