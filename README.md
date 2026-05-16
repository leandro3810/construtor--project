# Estrutura do Projeto Flask

Este repositório usa a seguinte estrutura base para um projeto Flask:

```text
.
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       ├── about.html
│       ├── base.html
│       └── index.html
├── config.py
├── requirements.txt
├── run.py
└── Tests/
    └── test_route.py
```

## Versões do framework e runtime

- Python: `3.12.3` (validado neste projeto)
- Framework web: `Flask 3.1.3` (versão estável mais recente)
- Node.js/React: não aplicável neste repositório (projeto Python/Flask)

## Como rodar o projeto

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Exporte as variáveis de ambiente para desenvolvimento (o `.flaskenv` já define apenas `FLASK_APP`):
   ```bash
   export FLASK_APP=run.py
   export FLASK_DEBUG=1
   ```

3. Rode o servidor:
   ```bash
   flask run
   ```

4. Acesse o aplicativo em `http://127.0.0.1:5000`.

## Testes

```bash
pytest -q
```
