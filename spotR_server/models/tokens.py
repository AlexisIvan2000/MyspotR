from app import db

from sqlalchemy.orm import relationship

class Tokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(250), nullable=False)
    refresh_token = db.Column(db.String(250))
    expires_in = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    