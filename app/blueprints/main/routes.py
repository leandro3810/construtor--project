from flask import render_template
from app.extensions import db
from . import main


@main.route('/')
def home():
    from app.models import Project, Model3D
    total_projects = db.session.query(Project).count()
    total_models = db.session.query(Model3D).count()
    return render_template('index.html', total_projects=total_projects, total_models=total_models)


@main.route('/sobre')
def about():
    return render_template('about.html')
