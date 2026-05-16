from flask import Blueprint

models3d = Blueprint('models3d', __name__, url_prefix='/modelos-3d')

from . import routes  # noqa: E402, F401
