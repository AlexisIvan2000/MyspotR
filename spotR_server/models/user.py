from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(120), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    country = db.Column(db.String(10), nullable=True)
    profile_image_url = db.Column(db.String(250), nullable=True)

    tokens= relationship("Tokens", backref="user", uselist=False)