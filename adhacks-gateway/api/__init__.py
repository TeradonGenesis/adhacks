from flask import Blueprint, Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

default = Blueprint('default', __name__, url_prefix='/public/api/v1')

@default.route('/', methods=["GET"])
def index():
    return "AdHacks is online"

app.register_blueprint(default)

