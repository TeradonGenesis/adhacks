from flask import Blueprint

ads_blueprint = Blueprint("ads", __name__, url_prefix="/public/api/v1/ads")

from . import views