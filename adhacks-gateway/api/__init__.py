from flask import Blueprint, Flask
from flask_cors import CORS
from api.ads import ads_blueprint

app = Flask(__name__)
CORS(app)

default = Blueprint('default', __name__, url_prefix='/public/api/v1')

@default.route('/', methods=["GET"])
def index():
    return "AdHacks is online"

app.register_blueprint(default)
app.register_blueprint(ads_blueprint)

if __name__ == "__main__":
    
    app.run(debug=True)