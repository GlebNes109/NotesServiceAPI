from flask import Flask, send_from_directory
from flask_wtf import CSRFProtect
from cachetools import LRUCache

from app.src.blueprints.authorize import auth_bp
from app.src.settings import settings

app = Flask(__name__, template_folder='app/src/templates') # путь только к базовым шаблонам (навбару и тд)
app.config['SECRET_KEY'] = settings.secret_key
app.config['WTF_CSRF_ENABLED'] = True
csrf = CSRFProtect(app)
cache = LRUCache(maxsize=100)

app.register_blueprint(auth_bp)

def user_data(filename):
    return send_from_directory('static/user_data', filename)


if __name__ == '__main__':
    app.run(port=settings.server_port, host=settings.server_host)