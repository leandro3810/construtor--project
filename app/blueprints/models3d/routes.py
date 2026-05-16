from flask import render_template, abort
from app.extensions import db
from app.models import Model3D
from . import models3d


@models3d.route('/')
def index():
    modelos = Model3D.query.order_by(Model3D.created_at.desc()).all()
    return render_template('models3d/index.html', modelos=modelos)


@models3d.route('/<int:model_id>')
def viewer(model_id):
    modelo = db.session.get(Model3D, model_id)
    if modelo is None:
        abort(404)
    return render_template('models3d/viewer.html', modelo=modelo)
