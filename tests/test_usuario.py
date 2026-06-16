import pytest
from services.usuarios_service import UsuariosService
from utils.payloads import new_user_payload, invalid_user_payload, login_payload
from utils.validator import validate_user_create, validate_user_login, validate_user_response, validate_login_response
from services.api_client import get


@pytest.mark.usuarios
def test_can_call_endpoint():
    response = get("")
    assert response.status_code == 200


@pytest.mark.usuarios
@pytest.mark.listagem
def test_can_get_users():
    response = UsuariosService.list_all()
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "usuarios" in body
    assert isinstance(body["usuarios"], list)


@pytest.mark.usuarios
@pytest.mark.cadastro
def test_can_create_user():
    user_payload = new_user_payload()
    validate_user_create(user_payload)

    response = UsuariosService.create(user_payload)
    body = response.json()

    assert response.status_code == 201
    validate_user_response(body)
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body
    
    UsuariosService.delete(body["_id"])


@pytest.mark.usuarios
@pytest.mark.cadastro
@pytest.mark.negativo
def test_cannot_create_user_without_email():
    payload = invalid_user_payload()

    response = UsuariosService.create(payload)
    body = response.json()

    assert response.status_code == 400
    assert "email" in body


@pytest.mark.usuarios
@pytest.mark.cadastro
def test_can_create_user_and_login():
    user_payload = new_user_payload()

    create_response = UsuariosService.create(user_payload)
    assert create_response.status_code == 201

    login_payload_body = login_payload(user_payload["email"], user_payload["password"])
    validate_user_login(login_payload_body)

    login_response = UsuariosService.login(login_payload_body)
    body = login_response.json()

    assert login_response.status_code == 200
    validate_login_response(body)
    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body
    
    UsuariosService.delete(create_response.json()["_id"])


@pytest.mark.usuarios
@pytest.mark.exclusao
def test_can_create_and_delete_user():
    user_payload = new_user_payload()

    create_response = UsuariosService.create(user_payload)
    assert create_response.status_code == 201

    user_id = create_response.json()["_id"]
    delete_response = UsuariosService.delete(user_id)

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Registro excluído com sucesso"


@pytest.mark.usuarios
@pytest.mark.exclusao
@pytest.mark.negativo
def test_can_delete_nonexistent_user():
    delete_response = UsuariosService.delete("nonexistent_user_id")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Nenhum registro excluído"


@pytest.mark.usuarios
@pytest.mark.atualizacao
def test_can_create_user_and_edit():
    user_payload = new_user_payload()

    create_response = UsuariosService.create(user_payload)
    assert create_response.status_code == 201

    user_id = create_response.json()["_id"]

    edited_payload = {
        "nome": "Usuario Editado",
        "email": user_payload["email"],
        "password": user_payload["password"],
        "administrador": "true",
    }

    edit_response = UsuariosService.update(user_id, edited_payload)

    assert edit_response.status_code == 200
    assert edit_response.json()["message"] == "Registro alterado com sucesso"
    
    UsuariosService.delete(user_id)


@pytest.mark.usuarios
@pytest.mark.atualizacao
def test_can_edit_nonexistent_user_and_create_new_one():
    payload = new_user_payload()

    response = UsuariosService.update("usuario_inexistente", payload)

    body = response.json()

    assert response.status_code == 201
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body
    
    UsuariosService.delete(body["_id"])


@pytest.mark.usuarios
@pytest.mark.atualizacao
@pytest.mark.negativo
def test_cannot_edit_user_to_existing_email():
    first_user = new_user_payload()
    second_user = new_user_payload()

    first_response = UsuariosService.create(first_user)
    second_response = UsuariosService.create(second_user)

    second_user_id = second_response.json()["_id"]

    edited_payload = {
        "nome": second_user["nome"],
        "email": first_user["email"],
        "password": second_user["password"],
        "administrador": second_user["administrador"],
    }

    response = UsuariosService.update(second_user_id, edited_payload)

    body = response.json()

    assert response.status_code == 400
    assert body["message"] == "Este email já está sendo usado"
    
    UsuariosService.delete(first_response.json()["_id"])
    UsuariosService.delete(second_user_id)


@pytest.mark.usuarios
@pytest.mark.cadastro
@pytest.mark.negativo
def test_cannot_create_user_with_existing_email():
    user_payload = new_user_payload()

    first_response = UsuariosService.create(user_payload)
    assert first_response.status_code == 201

    second_response = UsuariosService.create(user_payload)
    body = second_response.json()

    assert second_response.status_code == 400
    assert body["message"] == "Este email já está sendo usado"
    
    UsuariosService.delete(first_response.json()["_id"])


@pytest.mark.usuarios
@pytest.mark.busca
def test_can_get_user_by_id():
    payload = new_user_payload()

    create_response = UsuariosService.create(payload)
    user_id = create_response.json()["_id"]

    response = UsuariosService.get_by_id(user_id)
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == user_id
    assert body["nome"] == payload["nome"]
    assert body["email"] == payload["email"]
    assert body["administrador"] == payload["administrador"]
    
    UsuariosService.delete(user_id)


@pytest.mark.usuarios
@pytest.mark.busca
@pytest.mark.negativo
def test_cannot_get_user_with_invalid_id():
    response = UsuariosService.get_by_id("id_inexistente_404")
    body = response.json()

    assert response.status_code == 400
    assert "id" in body or "message" in body
