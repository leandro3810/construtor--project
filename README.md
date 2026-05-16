# Construtor Project

Plataforma web para gestão de projetos de construção civil com visualização 3D interativa.

## Estrutura

```
app/
├── blueprints/
│   ├── main/        ← home, sobre
│   ├── catalog/     ← catálogo de projetos
│   └── models3d/    ← visualizador 3D
├── models/
│   ├── project.py   ← modelo Project
│   └── model3d.py   ← modelo Model3D
├── static/
│   ├── style.css
│   └── js/
│       ├── hero3d.js      ← animação da home
│       ├── previews3d.js  ← mini-renders nos cards
│       └── viewer3d.js    ← visualizador completo
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── catalog/
│   └── models3d/
├── extensions.py    ← instância do SQLAlchemy
└── __init__.py      ← factory + seed de dados
config.py            ← configuração por ambiente
run.py
requirements.txt
Tests/
└── test_route.py
```

## Requisitos

- Python 3.12+
- pip

## Como rodar

```bash
pip install -r requirements.txt
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

Acesse: `http://127.0.0.1:5000`

O banco SQLite (`construtor.db`) é criado automaticamente na primeira execução com dados de exemplo.

## Configuração por ambiente

| Variável         | Padrão              | Descrição                     |
|------------------|---------------------|-------------------------------|
| `FLASK_ENV`      | `development`       | `development` ou `production` |
| `SECRET_KEY`     | gerada aleatória    | Chave secreta da sessão       |
| `DATABASE_URL`   | `sqlite:///construtor.db` | URI do banco de dados   |

## Testes

```bash
python -m pytest -q
```

## Tecnologias

- **Flask 3.1** — framework web
- **Flask-SQLAlchemy** — ORM com SQLite
- **Three.js** — renderização 3D no navegador
- **python-dotenv** — variáveis de ambiente
