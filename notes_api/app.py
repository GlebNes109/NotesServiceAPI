from flask import Flask
from notes_api.extensions import db, jwt
from notes_api.config import config
from resources.auth import auth_bp
from resources.user import user_bp
from resources.note import note_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.secret_key
    app.config['JWT_SECRET_KEY'] = config.jwt_secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlalchemy_database_uri
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.sqlalchemy_track_modifications

    db.init_app(app)
    jwt.init_app(app)

    @app.before_request
    def init_db():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix='/api/user')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(note_bp, url_prefix='/api/note')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
