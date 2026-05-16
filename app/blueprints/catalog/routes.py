from flask import render_template, abort
from app.extensions import db
from app.models import Project
from . import catalog


@catalog.route('/')
def index():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('catalog/index.html', projects=projects)


@catalog.route('/<int:project_id>')
def detail(project_id):
    project = db.session.get(Project, project_id)
    if project is None:
        abort(404)
    return render_template('catalog/detail.html', project=project)
