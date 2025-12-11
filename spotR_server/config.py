from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SPOTR_SECRET_KEY")

    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/spotr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

