import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app('development', {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    with app.app_context():
        from app.extensions import db
        db.create_all()
        from app import _seed_data
        _seed_data()
    with app.test_client() as client:
        yield client


# ── Main ──────────────────────────────────────────────────────────────
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Construtor Project'.encode() in response.data


def test_about(client):
    response = client.get('/sobre')
    assert response.status_code == 200
    assert 'Flask'.encode() in response.data


# ── Catalog ───────────────────────────────────────────────────────────
def test_catalog_index(client):
    response = client.get('/projetos/')
    assert response.status_code == 200
    assert 'Residência Moderna'.encode() in response.data


def test_catalog_index_filter_category(client):
    response = client.get('/projetos/?category=Residencial')
    assert response.status_code == 200
    assert 'Residência Moderna'.encode() in response.data


def test_catalog_index_filter_status(client):
    response = client.get('/projetos/?status=Concluído')
    assert response.status_code == 200


def test_catalog_index_search(client):
    response = client.get('/projetos/?q=Moderna')
    assert response.status_code == 200
    assert 'Residência Moderna'.encode() in response.data


def test_catalog_detail(client):
    response = client.get('/projetos/1')
    assert response.status_code == 200


def test_catalog_detail_not_found(client):
    response = client.get('/projetos/9999')
    assert response.status_code == 404


def test_catalog_edit_form(client):
    response = client.get('/projetos/1/editar')
    assert response.status_code == 200
    assert 'Residência Moderna'.encode() in response.data


def test_catalog_edit_not_found(client):
    response = client.get('/projetos/9999/editar')
    assert response.status_code == 404


def test_project_create_form(client):
    response = client.get('/projetos/novo')
    assert response.status_code == 200


def test_project_create(client):
    response = client.post('/projetos/novo', data={
        'code': 'CP-RES-2026-999',
        'name': 'Condomínio Horizonte',
        'description': 'Projeto residencial vertical com 3 torres e área de lazer integrada.',
        'client_name': 'Horizonte Incorporadora',
        'location': 'Fortaleza/CE',
        'responsible_engineer': 'Eng. Júlia Dias',
        'category': 'Residencial',
        'status': 'Planejamento',
        'area_m2': '9500',
        'budget_brl': '35000000',
        'start_date': '2026-04-01',
        'expected_end_date': '2028-10-31',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'CP-RES-2026-999'.encode() in response.data


def test_project_create_invalid(client):
    response = client.post('/projetos/novo', data={
        'code': '',
        'name': '',
        'description': '',
        'client_name': '',
        'location': '',
        'responsible_engineer': '',
        'category': 'Residencial',
        'status': 'Planejamento',
        'area_m2': '100',
        'budget_brl': '50000',
    })
    assert response.status_code == 400


def test_project_create_duplicate_code(client):
    response = client.post('/projetos/novo', data={
        'code': 'CP-RES-2026-001',
        'name': 'Outro Projeto',
        'description': 'Descrição.',
        'client_name': 'Cliente',
        'location': 'SP',
        'responsible_engineer': 'Eng. Teste',
        'category': 'Residencial',
        'status': 'Planejamento',
        'area_m2': '100',
        'budget_brl': '50000',
    })
    assert response.status_code == 400


def test_project_edit(client):
    response = client.post('/projetos/1/editar', data={
        'code': 'CP-RES-2026-001',
        'name': 'Residência Moderna Atualizada',
        'description': 'Descrição revisada do projeto residencial.',
        'client_name': 'Família Nogueira',
        'location': 'Campinas/SP',
        'responsible_engineer': 'Eng. Mariana Lopes',
        'category': 'Residencial',
        'status': 'Concluído',
        'area_m2': '430',
        'budget_brl': '1900000',
        'start_date': '2024-02-05',
        'expected_end_date': '2025-01-22',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Residência Moderna Atualizada'.encode() in response.data


def test_project_delete(client):
    response = client.post('/projetos/1/excluir', follow_redirects=True)
    assert response.status_code == 200
    assert 'excluído com sucesso'.encode() in response.data
    # Projeto deve ter sido removido
    detail = client.get('/projetos/1')
    assert detail.status_code == 404


def test_project_delete_not_found(client):
    response = client.post('/projetos/9999/excluir')
    assert response.status_code == 404


# ── Models 3D ─────────────────────────────────────────────────────────
def test_models3d_index(client):
    response = client.get('/modelos-3d/')
    assert response.status_code == 200


def test_models3d_viewer(client):
    response = client.get('/modelos-3d/1')
    assert response.status_code == 200


def test_models3d_viewer_not_found(client):
    response = client.get('/modelos-3d/9999')
    assert response.status_code == 404


def test_models3d_edit_form(client):
    response = client.get('/modelos-3d/1/editar')
    assert response.status_code == 200


def test_models3d_edit_not_found(client):
    response = client.get('/modelos-3d/9999/editar')
    assert response.status_code == 404


def test_model_create_form(client):
    response = client.get('/modelos-3d/novo')
    assert response.status_code == 200


def test_model_create(client):
    response = client.post('/modelos-3d/novo', data={
        'name': 'Modelo Estrutural Torre Norte',
        'description': 'Modelo estrutural completo da torre norte.',
        'category': 'Estrutural',
        'discipline': 'Estruturas',
        'version': 'v1.0',
        'format': 'ifc',
        'author_name': 'Equipe BIM Norte',
        'validation_status': 'Em revisão',
        'file_size_mb': '142.5',
        'file_name': 'torre-norte.ifc',
        'project_id': '1',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Modelo Estrutural Torre Norte'.encode() in response.data


def test_model_create_invalid(client):
    response = client.post('/modelos-3d/novo', data={
        'name': '',
        'description': 'incompleto',
        'category': 'Estrutural',
        'discipline': 'Estruturas',
        'version': 'v1.0',
        'format': 'ifc',
        'author_name': 'Equipe BIM',
        'validation_status': 'Em revisão',
        'file_size_mb': '100',
        'project_id': '1',
    })
    assert response.status_code == 400


def test_model_delete(client):
    response = client.post('/modelos-3d/1/excluir', follow_redirects=True)
    assert response.status_code == 200
    assert 'excluído com sucesso'.encode() in response.data
    detail = client.get('/modelos-3d/1')
    assert detail.status_code == 404


def test_model_delete_not_found(client):
    response = client.post('/modelos-3d/9999/excluir')
    assert response.status_code == 404

