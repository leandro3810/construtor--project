from flask import render_template, abort, request, redirect, url_for, flash
from app.extensions import db
from app.models import Model3D, Project
from . import models3d

MODEL_CATEGORIES = ['Arquitetônico', 'Estrutural', 'Instalações', 'Interiores']
VALIDATION_STATUS = ['Pendente', 'Em revisão', 'Aprovado']


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


@models3d.route('/novo', methods=['GET', 'POST'])
def create():
    projects = Project.query.order_by(Project.name.asc()).all()
    if request.method == 'POST':
        form_data, error = _validate_model_form(request.form, projects)
        if error:
            return render_template(
                'models3d/form.html',
                modelo=None,
                form_data=request.form,
                categories=MODEL_CATEGORIES,
                validation_statuses=VALIDATION_STATUS,
                projects=projects,
                error=error,
            ), 400

        model = Model3D(**form_data)
        db.session.add(model)
        db.session.commit()
        flash(f'Modelo "{model.name}" criado com sucesso.', 'success')
        return redirect(url_for('models3d.viewer', model_id=model.id))

    return render_template(
        'models3d/form.html',
        modelo=None,
        form_data={},
        categories=MODEL_CATEGORIES,
        validation_statuses=VALIDATION_STATUS,
        projects=projects,
        error=None,
    )


@models3d.route('/<int:model_id>/editar', methods=['GET', 'POST'])
def edit(model_id):
    modelo = db.session.get(Model3D, model_id)
    if modelo is None:
        abort(404)
    projects = Project.query.order_by(Project.name.asc()).all()

    if request.method == 'POST':
        form_data, error = _validate_model_form(request.form, projects)
        if error:
            return render_template(
                'models3d/form.html',
                modelo=modelo,
                form_data=request.form,
                categories=MODEL_CATEGORIES,
                validation_statuses=VALIDATION_STATUS,
                projects=projects,
                error=error,
            ), 400

        for field, value in form_data.items():
            setattr(modelo, field, value)
        db.session.commit()
        flash(f'Modelo "{modelo.name}" atualizado com sucesso.', 'success')
        return redirect(url_for('models3d.viewer', model_id=modelo.id))

    return render_template(
        'models3d/form.html',
        modelo=modelo,
        form_data=_model_to_form(modelo),
        categories=MODEL_CATEGORIES,
        validation_statuses=VALIDATION_STATUS,
        projects=projects,
        error=None,
    )


@models3d.route('/<int:model_id>/excluir', methods=['POST'])
def delete(model_id):
    modelo = db.session.get(Model3D, model_id)
    if modelo is None:
        abort(404)
    name = modelo.name
    db.session.delete(modelo)
    db.session.commit()
    flash(f'Modelo "{name}" excluído com sucesso.', 'success')
    return redirect(url_for('models3d.index'))


def _model_to_form(modelo: Model3D) -> dict:
    return {
        'name': modelo.name,
        'description': modelo.description,
        'category': modelo.category,
        'discipline': modelo.discipline,
        'version': modelo.version,
        'format': modelo.format,
        'author_name': modelo.author_name,
        'validation_status': modelo.validation_status,
        'file_size_mb': f'{modelo.file_size_mb:.2f}',
        'file_name': modelo.file_name or '',
        'project_id': str(modelo.project_id),
    }


def _validate_model_form(form: dict, projects: list[Project]) -> tuple[dict | None, str | None]:
    name = (form.get('name') or '').strip()
    description = (form.get('description') or '').strip()
    category = (form.get('category') or '').strip()
    discipline = (form.get('discipline') or '').strip()
    version = (form.get('version') or '').strip()
    format_value = (form.get('format') or '').strip()
    author_name = (form.get('author_name') or '').strip()
    validation_status = (form.get('validation_status') or '').strip()
    file_size_mb_raw = (form.get('file_size_mb') or '').strip()
    file_name = (form.get('file_name') or '').strip() or None
    project_id_raw = (form.get('project_id') or '').strip()

    required_fields = [name, description, category, discipline, version, format_value, author_name, validation_status, file_size_mb_raw, project_id_raw]
    if any(not value for value in required_fields):
        return None, 'Preencha todos os campos obrigatórios do modelo 3D.'
    if category not in MODEL_CATEGORIES:
        return None, 'Categoria inválida para modelo 3D.'
    if validation_status not in VALIDATION_STATUS:
        return None, 'Status de validação inválido para modelo 3D.'

    valid_project_ids = {project.id for project in projects}
    try:
        project_id = int(project_id_raw)
    except ValueError:
        return None, 'Projeto inválido para o modelo 3D.'
    if project_id not in valid_project_ids:
        return None, 'Projeto inválido para o modelo 3D.'

    try:
        file_size_mb = float(file_size_mb_raw.replace(',', '.'))
    except ValueError:
        return None, 'Tamanho do arquivo deve ser numérico.'
    if file_size_mb <= 0:
        return None, 'Tamanho do arquivo deve ser maior que zero.'

    return {
        'name': name,
        'description': description,
        'category': category,
        'discipline': discipline,
        'version': version,
        'format': format_value.upper(),
        'author_name': author_name,
        'validation_status': validation_status,
        'file_size_mb': file_size_mb,
        'file_name': file_name,
        'project_id': project_id,
    }, None
