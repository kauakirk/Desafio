import uuid


def new_user_payload(administrador="false"):
    unique_id = uuid.uuid4().hex
    return {
        "nome": f"User {unique_id}",
        "email": f"user_{unique_id}@qa.com",
        "password": "teste123",
        "administrador": administrador,
    }


def invalid_user_payload():
    """Payload de usuário sem email para validações"""
    unique_id = uuid.uuid4().hex
    return {
        "nome": "Fulano",
        "password": "123",
        "administrador": "false",
    }


def login_payload(email, password):
    """Payload de login com email e senha"""
    return {
        "email": email,
        "password": password,
    }


def empty_login_payload():
    """Payload de login vazio para validações"""
    return {
        "email": "",
        "password": "",
    }


def new_product_payload():
    unique_id = uuid.uuid4().hex
    return {
        "nome": f"Produto Teste {unique_id}",
        "preco": 100,
        "descricao": "Produto de teste",
        "quantidade": 10,
    }


def update_product_payload(original_payload):
    """Payload de produto atualizado com nome modificado"""
    return {
        "nome": original_payload["nome"] + " Atualizado",
        "preco": original_payload["preco"],
        "descricao": original_payload["descricao"],
        "quantidade": original_payload["quantidade"],
    }
