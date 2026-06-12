import pytest
from utils.data_factory import novo_usuario, novo_usuario_admin, usuario_sem_campo


# ───────────────────────────────────────────
# GET /usuarios
# ───────────────────────────────────────────

@pytest.mark.usuarios
@pytest.mark.listagem
def test_listar_usuarios_retorna_200(service):
    response = service.listar_usuarios()

    assert response.status_code == 200
    assert "quantidade" in response.json()
    assert "usuarios" in response.json()


@pytest.mark.usuarios
@pytest.mark.listagem
def test_listar_usuarios_filtro_por_nome(service, usuario_criado):
    nome = usuario_criado["payload"]["nome"]

    response = service.listar_usuarios(params={"nome": nome})
    data = response.json()

    assert response.status_code == 200
    assert data["quantidade"] >= 1
    assert any(u["nome"] == nome for u in data["usuarios"])


@pytest.mark.usuarios
@pytest.mark.listagem
def test_listar_usuarios_filtro_por_email(service, usuario_criado):
    email = usuario_criado["payload"]["email"]

    response = service.listar_usuarios(params={"email": email})
    data = response.json()

    assert response.status_code == 200
    assert data["quantidade"] == 1
    assert data["usuarios"][0]["email"] == email


# ───────────────────────────────────────────
# POST /usuarios
# ───────────────────────────────────────────

@pytest.mark.usuarios
@pytest.mark.cadastro
def test_cadastrar_usuario_valido_retorna_201(service):
    response = service.cadastrar_usuario(novo_usuario())

    assert response.status_code == 201
    assert "_id" in response.json()
    assert response.json()["message"] == "Cadastro realizado com sucesso"


@pytest.mark.usuarios
@pytest.mark.cadastro
def test_cadastrar_usuario_admin_retorna_201(service):
    response = service.cadastrar_usuario(novo_usuario_admin())

    assert response.status_code == 201
    assert "_id" in response.json()


@pytest.mark.usuarios
@pytest.mark.cadastro
@pytest.mark.negativo
def test_cadastrar_email_duplicado_retorna_400(service, usuario_criado):
    payload = novo_usuario()
    payload["email"] = usuario_criado["payload"]["email"]

    response = service.cadastrar_usuario(payload)

    assert response.status_code == 400
    assert "email" in response.json()["message"].lower()


@pytest.mark.usuarios
@pytest.mark.cadastro
@pytest.mark.negativo
@pytest.mark.parametrize("campo", ["nome", "email", "password", "administrador"])
def test_cadastrar_sem_campo_obrigatorio_retorna_400(service, campo):
    payload = usuario_sem_campo(campo)

    response = service.cadastrar_usuario(payload)

    assert response.status_code == 400
    assert campo in response.json()


# ───────────────────────────────────────────
# GET /usuarios/{id}
# ───────────────────────────────────────────

@pytest.mark.usuarios
@pytest.mark.busca
def test_buscar_usuario_por_id_valido_retorna_200(service, usuario_criado):
    usuario_id = usuario_criado["id"]

    response = service.buscar_por_id(usuario_id)
    data = response.json()

    assert response.status_code == 200
    assert data["_id"] == usuario_id
    assert data["email"] == usuario_criado["payload"]["email"]
    assert data["nome"] == usuario_criado["payload"]["nome"]


@pytest.mark.usuarios
@pytest.mark.busca
@pytest.mark.negativo
def test_buscar_usuario_id_inexistente_retorna_400(service):
    response = service.buscar_por_id("id_que_nao_existe")

    assert response.status_code == 400
    data = response.json()
    # Aceita mensagens de erro no formato {"message": ...} ou {"id": ...}
    assert ("message" in data) or ("id" in data)


# ───────────────────────────────────────────
# PUT /usuarios/{id}
# ───────────────────────────────────────────

@pytest.mark.usuarios
@pytest.mark.atualizacao
def test_atualizar_usuario_retorna_200(service, usuario_criado):
    usuario_id = usuario_criado["id"]
    payload_atualizado = novo_usuario()

    response = service.atualizar_usuario(usuario_id, payload_atualizado)

    assert response.status_code == 200
    assert response.json()["message"] == "Registro alterado com sucesso"


@pytest.mark.usuarios
@pytest.mark.atualizacao
def test_atualizar_usuario_valida_dados_alterados(service, usuario_criado):
    usuario_id = usuario_criado["id"]
    payload_atualizado = novo_usuario()

    response = service.atualizar_usuario(usuario_id, payload_atualizado)
    assert response.status_code == 200
    assert response.json()["message"] == "Registro alterado com sucesso"

    response = service.buscar_por_id(usuario_id)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == payload_atualizado["nome"]
    assert data["email"] == payload_atualizado["email"]


# ───────────────────────────────────────────
# DELETE /usuarios/{id}
# ───────────────────────────────────────────

@pytest.mark.usuarios
@pytest.mark.exclusao
def test_deletar_usuario_existente_retorna_200(service):
    payload = novo_usuario()
    usuario_id = service.cadastrar_usuario(payload).json().get("_id")

    response = service.deletar_usuario(usuario_id)

    assert response.status_code == 200
    assert response.json()["message"] == "Registro excluído com sucesso"


@pytest.mark.usuarios
@pytest.mark.exclusao
@pytest.mark.negativo
def test_deletar_usuario_inexistente_retorna_200_com_mensagem(service):
    response = service.deletar_usuario("id_inexistente_xyz")

    assert response.status_code == 200
    assert "nenhum" in response.json()["message"].lower()