# Construtor Project

Plataforma web para gestão de projetos de construção civil com visualização 3D interativa.

> Desenvolvido com Python/Flask · Design profissional dark theme · Three.js · SQLite

## Funcionalidades

- **Catálogo de projetos** com busca por nome/código/cliente e filtros por categoria e status
- **Detalhe de projeto** com barra de progresso estimada por prazo e dados formatados
- **Módulo de modelos 3D** com visualização interativa (orbit, zoom, pan) via Three.js
- **CRUD completo** — criar, editar e excluir projetos e modelos com validação de dados
- **Flash messages** de sucesso e erro em todas as operações
- **Design responsivo** dark theme com glassmorphism, gradientes e tipografia Inter
- **Menu hambúrguer** para mobile

## Estrutura

```
app/
├── blueprints/
│   ├── main/        ← home, sobre
│   ├── catalog/     ← catálogo de projetos (/projetos)
│   └── models3d/    ← visualizador 3D (/modelos-3d)
├── models/
│   ├── project.py   ← modelo Project
│   └── model3d.py   ← modelo Model3D
├── static/
│   ├── style.css    ← design system completo
│   └── js/
│       ├── hero3d.js
│       ├── previews3d.js
│       └── viewer3d.js
├── templates/
├── extensions.py
└── __init__.py      ← factory + seed de dados
config.py
run.py
Tests/
└── test_route.py    ← 27 testes
```

## Requisitos

- Python 3.12+
- pip

## Como rodar

```bash
pip install -r requirements.txt
flask run
```

Acesse: `http://127.0.0.1:5000`

O banco SQLite (`construtor.db`) é criado automaticamente com dados de exemplo.

## Rotas

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/` | Home com stats |
| GET | `/sobre` | Sobre o projeto |
| GET | `/projetos/` | Catálogo (busca + filtros) |
| GET | `/projetos/<id>` | Detalhe do projeto |
| GET/POST | `/projetos/novo` | Criar projeto |
| GET/POST | `/projetos/<id>/editar` | Editar projeto |
| POST | `/projetos/<id>/excluir` | Excluir projeto |
| GET | `/modelos-3d/` | Lista de modelos |
| GET | `/modelos-3d/<id>` | Visualizador 3D |
| GET/POST | `/modelos-3d/novo` | Criar modelo |
| GET/POST | `/modelos-3d/<id>/editar` | Editar modelo |
| POST | `/modelos-3d/<id>/excluir` | Excluir modelo |

## Configuração por ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `FLASK_ENV` | `development` | `development` ou `production` |
| `SECRET_KEY` | gerada aleatória | Chave secreta da sessão |
| `DATABASE_URL` | `sqlite:///construtor.db` | URI do banco de dados |

## Testes

```bash
pip install pytest
python -m pytest -q
```

Suite: **27 testes** cobrindo todas as rotas (CRUD, filtros, exclusão, 404, validações).

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12 · Flask 3.1 |
| ORM | Flask-SQLAlchemy · SQLite |
| Frontend | HTML/CSS (Inter · glassmorphism) |
| 3D | Three.js 0.163 |
| Testes | pytest |
