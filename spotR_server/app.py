from flask import Flask, session
from config import Config
from extensions import db   
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key= Config.SECRET_KEY
   
    app.config["SESSION_COOKIE_NAME"] = "session"
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    app.config["SESSION_COOKIE_SECURE"] = False     
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"    
    app.config["SESSION_COOKIE_DOMAIN"] = "127.0.0.1" 

    db.init_app(app)

    CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5173"]
    )

    with app.app_context():
        from models.user import User
        from models.tokens import Tokens
        db.create_all()

    from routes.auth_route import auth_bp
    from routes.client_auth import me_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(me_bp)

    @app.route("/test-cookie")
    def test_cookie():
        session["hello"] = "world"
        return "Cookie set!"


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
