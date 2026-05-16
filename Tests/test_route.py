import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app('development')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        from app.extensions import db
        db.create_all()
        from app import _seed_data
        _seed_data()
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_about(client):
    response = client.get('/sobre')
    assert response.status_code == 200


def test_catalog_index(client):
    response = client.get('/projetos/')
    assert response.status_code == 200
    assert 'Residência Moderna'.encode() in response.data


def test_catalog_detail(client):
    response = client.get('/projetos/1')
    assert response.status_code == 200


def test_catalog_detail_not_found(client):
    response = client.get('/projetos/9999')
    assert response.status_code == 404


def test_models3d_index(client):
    response = client.get('/modelos-3d/')
    assert response.status_code == 200


def test_models3d_viewer(client):
    response = client.get('/modelos-3d/1')
    assert response.status_code == 200


def test_models3d_viewer_not_found(client):
    response = client.get('/modelos-3d/9999')
    assert response.status_code == 404
