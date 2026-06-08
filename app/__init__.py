import os
from datetime import date, datetime, timezone
from flask import Flask
from sqlalchemy import inspect, text
from config import config_by_name
from .extensions import db


def create_app(config_name: str | None = None, config_overrides: dict | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    if config_overrides:
        app.config.update(config_overrides)

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

    # Inject current datetime into all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.now(timezone.utc)}

    # Jinja filter: Brazilian currency format  (e.g. 1850000.0 → "1.850.000,00")
    @app.template_filter('brl')
    def format_brl(value: float) -> str:
        try:
            integer, decimal = f'{float(value):.2f}'.split('.')
            groups = []
            while len(integer) > 3:
                groups.append(integer[-3:])
                integer = integer[:-3]
            groups.append(integer)
            return ','.join(['.'.join(reversed(groups)), decimal])
        except (TypeError, ValueError):
            return str(value)

    # Create tables and seed data
    with app.app_context():
        db.create_all()
        _ensure_schema_updates()
        _seed_data()

    return app


def _seed_data() -> None:
    from .models import Project, Model3D

    if Project.query.first() is not None:
        return

    projects = [
        Project(
            code='CP-RES-2026-001',
            name='Residência Moderna',
            description='Projeto residencial de alto padrão com fachada contemporânea, pé-direito duplo e integração total entre ambientes internos e externos.',
            client_name='Família Nogueira',
            location='Campinas/SP',
            responsible_engineer='Eng. Mariana Lopes',
            category='Residencial',
            status='Concluído',
            area_m2=420.0,
            budget_brl=1850000.0,
            start_date=date(2024, 2, 5),
            expected_end_date=date(2025, 1, 22),
        ),
        Project(
            code='CP-COM-2026-002',
            name='Complexo Comercial Alfa',
            description='Torre comercial de 12 andares com estrutura de concreto armado, vidro temperado e sistema de automação predial.',
            client_name='Alfa Empreendimentos S.A.',
            location='Belo Horizonte/MG',
            responsible_engineer='Eng. Rafael Sousa',
            category='Comercial',
            status='Em andamento',
            area_m2=11800.0,
            budget_brl=42600000.0,
            start_date=date(2025, 3, 10),
            expected_end_date=date(2027, 8, 30),
        ),
        Project(
            code='CP-IND-2026-003',
            name='Pavilhão Industrial Beta',
            description='Galpão industrial com estrutura metálica pré-fabricada, cobertura termoacústica e plataformas de carga e descarga.',
            client_name='Beta Logística Integrada',
            location='Contagem/MG',
            responsible_engineer='Eng. Carlos Menezes',
            category='Industrial',
            status='Planejamento',
            area_m2=15800.0,
            budget_brl=31200000.0,
            start_date=date(2026, 7, 1),
            expected_end_date=date(2027, 12, 15),
        ),
        Project(
            code='CP-INS-2026-004',
            name='Escola Municipal Verde',
            description='Projeto de escola pública com conceito sustentável, painéis solares, captação de água da chuva e jardins pedagógicos.',
            client_name='Prefeitura Municipal de Curitiba',
            location='Curitiba/PR',
            responsible_engineer='Eng. Bianca Teixeira',
            category='Institucional',
            status='Em andamento',
            area_m2=6400.0,
            budget_brl=18900000.0,
            start_date=date(2025, 6, 2),
            expected_end_date=date(2026, 11, 28),
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
            discipline='Estruturas',
            version='v1.4',
            format='GLB',
            author_name='Equipe BIM Residencial',
            validation_status='Aprovado',
            file_size_mb=52.3,
            project_id=projects[0].id,
        ),
        Model3D(
            name='Fachada Torre Alfa',
            description='Modelo 3D da fachada principal com detalhamento de esquadrias e cobogós decorativos.',
            category='Arquitetônico',
            discipline='Arquitetura',
            version='v2.1',
            format='GLTF',
            author_name='Núcleo Arquitetura Alfa',
            validation_status='Em revisão',
            file_size_mb=126.8,
            project_id=projects[1].id,
        ),
        Model3D(
            name='Galpão Metálico — Vista Explodida',
            description='Estrutura metálica do pavilhão industrial detalhando pilares, vigas e terças.',
            category='Estrutural',
            discipline='Estruturas Metálicas',
            version='v0.9',
            format='IFC',
            author_name='Coordenação Industrial Beta',
            validation_status='Pendente',
            file_size_mb=204.5,
            project_id=projects[2].id,
        ),
        Model3D(
            name='Layout Escola — Bloco Principal',
            description='Disposição volumétrica dos blocos pedagógicos com pátio central e coberta.',
            category='Arquitetônico',
            discipline='Arquitetura',
            version='v1.2',
            format='GLB',
            author_name='Equipe Sustentabilidade Pública',
            validation_status='Aprovado',
            file_size_mb=88.1,
            project_id=projects[3].id,
        ),
    ]

    for m in modelos:
        db.session.add(m)

    db.session.commit()


def _ensure_schema_updates() -> None:
    inspector = inspect(db.engine)
    table_names = set(inspector.get_table_names())

    if 'projects' in table_names:
        _sync_projects_table({col['name'] for col in inspector.get_columns('projects')})
    if 'models3d' in table_names:
        _sync_models_table({col['name'] for col in inspector.get_columns('models3d')})


def _sync_projects_table(existing_columns: set[str]) -> None:
    statements: list[str] = []
    if 'code' not in existing_columns:
        statements.append('ALTER TABLE projects ADD COLUMN code VARCHAR(30)')
    if 'client_name' not in existing_columns:
        statements.append('ALTER TABLE projects ADD COLUMN client_name VARCHAR(120)')
    if 'location' not in existing_columns:
        statements.append('ALTER TABLE projects ADD COLUMN location VARCHAR(120)')
    if 'responsible_engineer' not in existing_columns:
        statements.append('ALTER TABLE projects ADD COLUMN responsible_engineer VARCHAR(120)')
    if 'area_m2' not in existing_columns:
        statements.append('ALTER TABLE projects ADD COLUMN area_m2 FLOAT')
    if 'budget_brl' not in existing_columns:
        statements.append('ALTER TABLE projects ADD COLUMN budget_brl FLOAT')
    if 'start_date' not in existing_columns:
        statements.append('ALTER TABLE projects ADD COLUMN start_date DATE')
    if 'expected_end_date' not in existing_columns:
        statements.append('ALTER TABLE projects ADD COLUMN expected_end_date DATE')

    for statement in statements:
        db.session.execute(text(statement))

    if statements:
        project_ids_without_code = db.session.execute(
            text("SELECT id FROM projects WHERE code IS NULL OR trim(code) = ''")
        ).scalars().all()
        for project_id in project_ids_without_code:
            db.session.execute(
                text('UPDATE projects SET code = :code WHERE id = :id'),
                {'code': f'CP-LEG-{project_id:04d}', 'id': project_id},
            )
        db.session.execute(text("UPDATE projects SET client_name = 'Cliente não informado' WHERE client_name IS NULL OR trim(client_name) = ''"))
        db.session.execute(text("UPDATE projects SET location = 'Local não informado' WHERE location IS NULL OR trim(location) = ''"))
        db.session.execute(text("UPDATE projects SET responsible_engineer = 'Responsável não informado' WHERE responsible_engineer IS NULL OR trim(responsible_engineer) = ''"))
        db.session.execute(text('UPDATE projects SET area_m2 = 0 WHERE area_m2 IS NULL'))
        db.session.execute(text('UPDATE projects SET budget_brl = 0 WHERE budget_brl IS NULL'))
        db.session.commit()


def _sync_models_table(existing_columns: set[str]) -> None:
    statements: list[str] = []
    if 'discipline' not in existing_columns:
        statements.append('ALTER TABLE models3d ADD COLUMN discipline VARCHAR(60)')
    if 'version' not in existing_columns:
        statements.append('ALTER TABLE models3d ADD COLUMN version VARCHAR(20)')
    if 'format' not in existing_columns:
        statements.append('ALTER TABLE models3d ADD COLUMN format VARCHAR(20)')
    if 'author_name' not in existing_columns:
        statements.append('ALTER TABLE models3d ADD COLUMN author_name VARCHAR(120)')
    if 'validation_status' not in existing_columns:
        statements.append('ALTER TABLE models3d ADD COLUMN validation_status VARCHAR(30)')
    if 'file_size_mb' not in existing_columns:
        statements.append('ALTER TABLE models3d ADD COLUMN file_size_mb FLOAT')

    for statement in statements:
        db.session.execute(text(statement))

    if statements:
        db.session.execute(text("UPDATE models3d SET discipline = 'Arquitetura' WHERE discipline IS NULL OR trim(discipline) = ''"))
        db.session.execute(text("UPDATE models3d SET version = 'v1.0' WHERE version IS NULL OR trim(version) = ''"))
        db.session.execute(text("UPDATE models3d SET format = 'GLB' WHERE format IS NULL OR trim(format) = ''"))
        db.session.execute(text("UPDATE models3d SET author_name = 'Equipe Técnica' WHERE author_name IS NULL OR trim(author_name) = ''"))
        db.session.execute(text("UPDATE models3d SET validation_status = 'Em revisão' WHERE validation_status IS NULL OR trim(validation_status) = ''"))
        db.session.execute(text('UPDATE models3d SET file_size_mb = 0 WHERE file_size_mb IS NULL'))
        db.session.commit()
