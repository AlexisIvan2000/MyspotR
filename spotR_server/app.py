from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from config import Config
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        db.init_app(app)
        from models.user import User  
        db.create_all()



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)