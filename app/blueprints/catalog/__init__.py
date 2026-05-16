from flask import Blueprint

catalog = Blueprint('catalog', __name__, url_prefix='/projetos')

from . import routes  # noqa: E402, F401
