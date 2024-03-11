from database import db

class User(db.Model):
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_mail=db.Column(db.String(60),unique=True, nullable=False)
    password=db.Column(db.String(100), nullable=False)