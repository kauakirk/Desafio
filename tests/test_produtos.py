from services.usuarios_service import UsuariosService
from services.produtos_service import ProdutosService
from utils.payloads import new_user_payload, new_product_payload, login_payload, update_product_payload
from utils.validator import validate_product_create, validate_product_response


def test_list_products():
    response = ProdutosService.list_all()
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "produtos" in body
    assert isinstance(body["produtos"], list)


def test_create_product_as_admin(admin_tok):
    payload = new_product_payload()
    validate_product_create(payload)

    response = ProdutosService.create(admin_tok, payload)
    body = response.json()

    assert response.status_code == 201
    validate_product_response(body)
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body


def test_create_product_without_token():
    payload = new_product_payload()
    response = ProdutosService.create("", payload)

    assert response.status_code == 401


def test_create_product_as_non_admin_returns_forbidden():
    user_payload = new_user_payload(administrador="false")
    create_response = UsuariosService.create(user_payload)
    assert create_response.status_code == 201

    login_response = UsuariosService.login(login_payload(user_payload["email"], user_payload["password"]))
    assert login_response.status_code == 200
    token = login_response.json()["authorization"]

    payload = new_product_payload()
    response = ProdutosService.create(token, payload)

    assert response.status_code == 403


def test_get_product_by_id(admin_tok):
    payload = new_product_payload()
    creation_response = ProdutosService.create(admin_tok, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    response = ProdutosService.get_by_id(product_id)
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == product_id
    assert body["nome"] == payload["nome"]


def test_update_product_as_admin(admin_tok):
    payload = new_product_payload()
    creation_response = ProdutosService.create(admin_tok, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    updated_payload = update_product_payload(payload)

    response = ProdutosService.update(product_id, updated_payload, admin_tok)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Registro alterado com sucesso"


def test_delete_product_as_admin(admin_tok):
    payload = new_product_payload()
    creation_response = ProdutosService.create(admin_tok, payload)
    assert creation_response.status_code == 201
    product_id = creation_response.json()["_id"]

    response = ProdutosService.delete(product_id, admin_tok)
    body = response.json()

    assert response.status_code == 200
    assert "Registro excluído" in body["message"]
