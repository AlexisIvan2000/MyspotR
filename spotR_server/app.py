from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = getattr(Config, 'SECRET_KEY', 'default')  
    db.init_app(app)

    with app.app_context():
        from models.user import User
        from models.tokens import Tokens
        db.create_all()

    from routes.auth_route import auth_bp
    app.register_blueprint(auth_bp)    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
