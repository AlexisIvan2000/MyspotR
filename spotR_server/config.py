from dotenv import load_dotenv
load_dotenv()

import os
class Config:
    SECRET_KEY = os.getenv("SPOTR_SECRET_KEY")

    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'spotr.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

