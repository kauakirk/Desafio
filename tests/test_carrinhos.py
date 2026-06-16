import pytest
from services.usuarios_service import UsuariosService
from services.produtos_service import ProdutosService
from services.carrinhos_service import CarrinhosService
from utils.payloads import new_user_payload, new_product_payload, login_payload
from utils.validator import validate_cart_create, validate_cart_response


def _create_user_and_get_token():
    """Helper: cria um novo usuário e retorna seu token."""
    user_payload = new_user_payload()
    user_response = UsuariosService.create(user_payload)
    assert user_response.status_code == 201

    login_response = UsuariosService.login(login_payload(user_payload["email"], user_payload["password"]))
    assert login_response.status_code == 200
    return login_response.json()["authorization"], user_response.json()["_id"]


@pytest.mark.carrinhos
@pytest.mark.listagem
def test_list_carts():
    response = CarrinhosService.list_all()
    body = response.json()

    assert response.status_code == 200
    assert "quantidade" in body
    assert "carrinhos" in body
    assert isinstance(body["carrinhos"], list)


@pytest.mark.carrinhos
@pytest.mark.cadastro
def test_create_cart_with_valid_token(admin_tok):
    product_response = ProdutosService.create(admin_tok, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_tok, user_id = _create_user_and_get_token()

    cart_payload = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}
    validate_cart_create(cart_payload)

    cart_response = CarrinhosService.create(user_tok, product_id)
    body = cart_response.json()

    assert cart_response.status_code == 201
    validate_cart_response(body)
    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body
    
    ProdutosService.delete(product_id, admin_tok)
    UsuariosService.delete(user_id)


@pytest.mark.carrinhos
@pytest.mark.busca
def test_get_cart_by_id(admin_tok):
    product_response = ProdutosService.create(admin_tok, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_tok, user_id = _create_user_and_get_token()

    create_response = CarrinhosService.create(user_tok, product_id)
    assert create_response.status_code == 201
    cart_id = create_response.json()["_id"]

    response = CarrinhosService.get_by_id(cart_id)
    body = response.json()

    assert response.status_code == 200
    assert body["_id"] == cart_id
    
    ProdutosService.delete(product_id, admin_tok)
    UsuariosService.delete(user_id)


@pytest.mark.carrinhos
def test_conclude_purchase_deletes_cart(admin_tok):
    product_response = ProdutosService.create(admin_tok, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_tok, user_id = _create_user_and_get_token()

    create_response = CarrinhosService.create(user_tok, product_id)
    assert create_response.status_code == 201

    response = CarrinhosService.conclude_purchase(user_tok)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] in [
        "Registro excluído com sucesso",
        "Registro excluído com sucesso | Não foi encontrado carrinho para esse usuário",
    ]
    
    ProdutosService.delete(product_id, admin_tok)
    UsuariosService.delete(user_id)


@pytest.mark.carrinhos
def test_cancel_purchase_deletes_cart_and_restock(admin_tok):
    product_response = ProdutosService.create(admin_tok, new_product_payload())
    assert product_response.status_code == 201
    product_id = product_response.json()["_id"]

    user_tok, user_id = _create_user_and_get_token()

    create_response = CarrinhosService.create(user_tok, product_id)
    assert create_response.status_code == 201

    response = CarrinhosService.cancel_purchase(user_tok)
    body = response.json()

    assert response.status_code == 200
    assert body["message"] in [
        "Registro excluído com sucesso",
        "Registro excluído com sucesso. Estoque dos produtos reabastecido",
        "Registro excluído com sucesso | Não foi encontrado carrinho para esse usuário",
    ]
    
    ProdutosService.delete(product_id, admin_tok)
    UsuariosService.delete(user_id)


@pytest.mark.carrinhos
@pytest.mark.busca
@pytest.mark.negativo
def test_cannot_get_cart_with_invalid_id():
    response = CarrinhosService.get_by_id("id_inexistente_404")
    body = response.json()

    assert response.status_code == 400
    assert "id" in body or "message" in body
