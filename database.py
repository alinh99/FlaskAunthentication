from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)

class ForgotPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship("User")
    otp = db.Column(db.Integer)
    is_confirmed_otp = db.Column(db.Boolean)
    expired_in = db.Column(db.DateTime)