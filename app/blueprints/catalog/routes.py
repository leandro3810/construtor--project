from datetime import datetime
from flask import render_template, abort, request, redirect, url_for
from app.extensions import db
from app.models import Project
from . import catalog

PROJECT_CATEGORIES = ['Residencial', 'Comercial', 'Industrial', 'Institucional']
PROJECT_STATUS = ['Planejamento', 'Em andamento', 'Concluído']


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


@catalog.route('/novo', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form_data, error = _validate_project_form(request.form)
        if error:
            return render_template(
                'catalog/form.html',
                project=None,
                form_data=request.form,
                categories=PROJECT_CATEGORIES,
                statuses=PROJECT_STATUS,
                error=error,
            ), 400

        existing = Project.query.filter_by(code=form_data['code']).first()
        if existing:
            return render_template(
                'catalog/form.html',
                project=None,
                form_data=request.form,
                categories=PROJECT_CATEGORIES,
                statuses=PROJECT_STATUS,
                error='Já existe um projeto com este código.',
            ), 400

        project = Project(**form_data)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('catalog.detail', project_id=project.id))

    return render_template(
        'catalog/form.html',
        project=None,
        form_data={},
        categories=PROJECT_CATEGORIES,
        statuses=PROJECT_STATUS,
        error=None,
    )


@catalog.route('/<int:project_id>/editar', methods=['GET', 'POST'])
def edit(project_id):
    project = db.session.get(Project, project_id)
    if project is None:
        abort(404)

    if request.method == 'POST':
        form_data, error = _validate_project_form(request.form)
        if error:
            return render_template(
                'catalog/form.html',
                project=project,
                form_data=request.form,
                categories=PROJECT_CATEGORIES,
                statuses=PROJECT_STATUS,
                error=error,
            ), 400

        existing = Project.query.filter(Project.code == form_data['code'], Project.id != project.id).first()
        if existing:
            return render_template(
                'catalog/form.html',
                project=project,
                form_data=request.form,
                categories=PROJECT_CATEGORIES,
                statuses=PROJECT_STATUS,
                error='Já existe um projeto com este código.',
            ), 400

        for field, value in form_data.items():
            setattr(project, field, value)
        db.session.commit()
        return redirect(url_for('catalog.detail', project_id=project.id))

    return render_template(
        'catalog/form.html',
        project=project,
        form_data=_project_to_form(project),
        categories=PROJECT_CATEGORIES,
        statuses=PROJECT_STATUS,
        error=None,
    )


def _project_to_form(project: Project) -> dict:
    return {
        'code': project.code,
        'name': project.name,
        'description': project.description,
        'client_name': project.client_name,
        'location': project.location,
        'responsible_engineer': project.responsible_engineer,
        'category': project.category,
        'status': project.status,
        'area_m2': f'{project.area_m2:.2f}',
        'budget_brl': f'{project.budget_brl:.2f}',
        'start_date': project.start_date.isoformat() if project.start_date else '',
        'expected_end_date': project.expected_end_date.isoformat() if project.expected_end_date else '',
    }


def _validate_project_form(form: dict) -> tuple[dict | None, str | None]:
    code = (form.get('code') or '').strip()
    name = (form.get('name') or '').strip()
    description = (form.get('description') or '').strip()
    client_name = (form.get('client_name') or '').strip()
    location = (form.get('location') or '').strip()
    responsible_engineer = (form.get('responsible_engineer') or '').strip()
    category = (form.get('category') or '').strip()
    status = (form.get('status') or '').strip()
    area_m2_raw = (form.get('area_m2') or '').strip()
    budget_brl_raw = (form.get('budget_brl') or '').strip()
    start_date_raw = (form.get('start_date') or '').strip()
    expected_end_date_raw = (form.get('expected_end_date') or '').strip()

    required_fields = [code, name, description, client_name, location, responsible_engineer, category, status, area_m2_raw, budget_brl_raw]
    if any(not value for value in required_fields):
        return None, 'Preencha todos os campos obrigatórios do projeto.'
    if category not in PROJECT_CATEGORIES:
        return None, 'Categoria inválida para projeto.'
    if status not in PROJECT_STATUS:
        return None, 'Status inválido para projeto.'

    try:
        area_m2 = float(area_m2_raw.replace(',', '.'))
        budget_brl = float(budget_brl_raw.replace(',', '.'))
    except ValueError:
        return None, 'Área e orçamento devem ser numéricos.'

    if area_m2 <= 0 or budget_brl <= 0:
        return None, 'Área e orçamento devem ser maiores que zero.'

    start_date = _parse_iso_date(start_date_raw)
    expected_end_date = _parse_iso_date(expected_end_date_raw)
    if start_date_raw and start_date is None:
        return None, 'Data de início inválida.'
    if expected_end_date_raw and expected_end_date is None:
        return None, 'Data prevista de término inválida.'
    if start_date and expected_end_date and expected_end_date <= start_date:
        return None, 'A data prevista de término deve ser posterior à data de início.'

    return {
        'code': code.upper(),
        'name': name,
        'description': description,
        'client_name': client_name,
        'location': location,
        'responsible_engineer': responsible_engineer,
        'category': category,
        'status': status,
        'area_m2': area_m2,
        'budget_brl': budget_brl,
        'start_date': start_date,
        'expected_end_date': expected_end_date,
    }, None


def _parse_iso_date(value: str):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None
