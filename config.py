import os
import secrets
from pathlib import Path


def _load_secret_key() -> str:
    env_secret = os.environ.get('SECRET_KEY')
    if env_secret:
        return env_secret

    secret_file = Path(os.environ.get('SECRET_KEY_FILE', '.flask_secret_key'))
    if secret_file.exists():
        return secret_file.read_text(encoding='utf-8').strip()

    generated_secret = secrets.token_hex(32)
    try:
        secret_file.write_text(generated_secret, encoding='utf-8')
        secret_file.chmod(0o600)
    except OSError:
        pass

    return generated_secret


class Config:
    SECRET_KEY = _load_secret_key()
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
