import os
from flask import Flask
from config import config_by_name
from .extensions import db


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Init extensions
    db.init_app(app)

    # Register blueprints
    from .blueprints.main import main
    from .blueprints.catalog import catalog
    from .blueprints.models3d import models3d

    app.register_blueprint(main)
    app.register_blueprint(catalog)
    app.register_blueprint(models3d)

    # Create tables and seed data
    with app.app_context():
        db.create_all()
        _seed_data()

    return app


def _seed_data() -> None:
    from .models import Project, Model3D

    if Project.query.first() is not None:
        return

    projects = [
        Project(
            name='Residência Moderna',
            description='Projeto residencial de alto padrão com fachada contemporânea, pé-direito duplo e integração total entre ambientes internos e externos.',
            category='Residencial',
            status='Concluído',
        ),
        Project(
            name='Complexo Comercial Alfa',
            description='Torre comercial de 12 andares com estrutura de concreto armado, vidro temperado e sistema de automação predial.',
            category='Comercial',
            status='Em andamento',
        ),
        Project(
            name='Pavilhão Industrial Beta',
            description='Galpão industrial com estrutura metálica pré-fabricada, cobertura termoacústica e plataformas de carga e descarga.',
            category='Industrial',
            status='Planejamento',
        ),
        Project(
            name='Escola Municipal Verde',
            description='Projeto de escola pública com conceito sustentável, painéis solares, captação de água da chuva e jardins pedagógicos.',
            category='Institucional',
            status='Em andamento',
        ),
    ]

    for p in projects:
        db.session.add(p)
    db.session.flush()

    modelos = [
        Model3D(
            name='Estrutura Residencial — Planta Isométrica',
            description='Visualização tridimensional da estrutura de concreto e alvenaria do projeto residencial.',
            category='Estrutural',
            project_id=projects[0].id,
        ),
        Model3D(
            name='Fachada Torre Alfa',
            description='Modelo 3D da fachada principal com detalhamento de esquadrias e cobogós decorativos.',
            category='Arquitetônico',
            project_id=projects[1].id,
        ),
        Model3D(
            name='Galpão Metálico — Vista Explodida',
            description='Estrutura metálica do pavilhão industrial detalhando pilares, vigas e terças.',
            category='Estrutural',
            project_id=projects[2].id,
        ),
        Model3D(
            name='Layout Escola — Bloco Principal',
            description='Disposição volumétrica dos blocos pedagógicos com pátio central e coberta.',
            category='Arquitetônico',
            project_id=projects[3].id,
        ),
    ]

    for m in modelos:
        db.session.add(m)

    db.session.commit()

