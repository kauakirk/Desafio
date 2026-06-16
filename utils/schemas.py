user_create_schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "administrador": {"type": "string", "enum": ["true", "false"]},
    },
    "required": ["nome", "email", "password", "administrador"],
    "additionalProperties": False,
}

user_login_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"],
    "additionalProperties": False,
}

product_create_schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "preco": {"type": "number"},
        "descricao": {"type": "string"},
        "quantidade": {"type": "integer", "minimum": 0},
    },
    "required": ["nome", "preco", "descricao", "quantidade"],
    "additionalProperties": False,
}

cart_create_schema = {
    "type": "object",
    "properties": {
        "produtos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "idProduto": {"type": "string"},
                    "quantidade": {"type": "integer", "minimum": 1},
                },
                "required": ["idProduto", "quantidade"],
                "additionalProperties": False,
            },
            "minItems": 1,
        },
    },
    "required": ["produtos"],
    "additionalProperties": False,
}

user_response_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"},
    },
    "required": ["message", "_id"],
    "additionalProperties": True,
}

login_response_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "authorization": {"type": "string"},
    },
    "required": ["message", "authorization"],
    "additionalProperties": True,
}

product_response_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"},
    },
    "required": ["message", "_id"],
    "additionalProperties": True,
}

cart_response_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"},
    },
    "required": ["message", "_id"],
    "additionalProperties": True,
}
