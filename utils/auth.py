from services.usuarios_service import UsuariosService
from utils.payloads import new_user_payload

_admin_token_cache = None
_user_token_cache = None


def admin_token():
    """Retorna um token de admin, criando e cacheando na primeira chamada da sessão."""
    global _admin_token_cache
    if _admin_token_cache is None:
        payload = new_user_payload(administrador="true")
        create_response = UsuariosService.create(payload)
        assert create_response.status_code == 201

        login_response = UsuariosService.login({"email": payload["email"], "password": payload["password"]})
        assert login_response.status_code == 200
        _admin_token_cache = login_response.json()["authorization"]

    return _admin_token_cache


def user_token():
    """Retorna um token de usuário comum, criando e cacheando na primeira chamada da sessão."""
    global _user_token_cache
    if _user_token_cache is None:
        payload = new_user_payload(administrador="false")
        create_response = UsuariosService.create(payload)
        assert create_response.status_code == 201

        login_response = UsuariosService.login({"email": payload["email"], "password": payload["password"]})
        assert login_response.status_code == 200
        _user_token_cache = login_response.json()["authorization"]

    return _user_token_cache


def reset_token_cache():
    """Limpa o cache de tokens — útil para forçar renovação em testes específicos."""
    global _admin_token_cache, _user_token_cache
    _admin_token_cache = None
    _user_token_cache = None
