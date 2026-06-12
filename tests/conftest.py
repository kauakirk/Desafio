import pytest
from services.usuarios_service import UsuariosService
from utils.data_factory import novo_usuario
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://compassuol.serverest.dev")


@pytest.fixture(scope="session")
def service():
    """
    Cria uma única instância do UsuariosService para toda a sessão.
    Reutiliza a mesma Session HTTP em todos os testes.
    """
    svc = UsuariosService(BASE_URL)
    yield svc
    svc.fechar()


@pytest.fixture
def usuario_criado(service):
    """
    Cria um usuário antes do teste e deleta automaticamente depois.
    Use essa fixture em qualquer teste que precise de um usuário existente.
    """
    payload = novo_usuario()
    response = service.cadastrar_usuario(payload)
    assert response.status_code == 201, f"Falha no cadastro de fixture: {response.status_code} - {response.text}"
    usuario_id = response.json().get("_id")
    assert usuario_id, f"ID ausente no cadastro de fixture: {response.text}"

    yield {"id": usuario_id, "payload": payload}

    service.deletar_usuario(usuario_id)