import pytest
from utils.auth import admin_token as _get_admin_token, user_token as _get_user_token, reset_token_cache


def pytest_configure(config):
    """Limpa o cache de tokens antes de qualquer sessão de testes."""
    reset_token_cache()


@pytest.fixture(scope="session")
def admin_tok():
    """Token de administrador compartilhado por toda a sessão de testes."""
    return _get_admin_token()


@pytest.fixture(scope="session")
def user_tok():
    """Token de usuário comum compartilhado por toda a sessão de testes."""
    return _get_user_token()
