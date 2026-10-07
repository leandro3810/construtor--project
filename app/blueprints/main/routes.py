from datetime import date
from flask import render_template
from app.extensions import db
from . import main


@main.route('/')
def home():
    from app.models import Project, Model3D
    projects = Project.query.all()
    total_projects = len(projects)
    active_projects = sum(project.status == 'Em andamento' for project in projects)
    overdue_projects = [
        project for project in projects
        if project.status != 'Concluído'
        and project.expected_end_date
        and project.expected_end_date < date.today()
    ]
    total_budget = sum(project.budget_brl for project in projects)
    total_models = db.session.query(Model3D).count()
    return render_template(
        'index.html',
        total_projects=total_projects,
        active_projects=active_projects,
        overdue_projects=overdue_projects,
        total_budget=total_budget,
        total_models=total_models,
    )


@main.route('/sobre')
def about():
    return render_template('about.html')
