from faker import Faker

fake = Faker("pt_BR")


def novo_usuario(administrador: str = "false") -> dict:
    """
    Gera um payload válido com dados aleatórios em português.
    Usa Faker para garantir nome e email únicos a cada chamada,
    evitando conflitos de cadastro na ServeRest.
    """
    return {
        "nome": fake.name(),
        "email": fake.unique.email(),
        "password": fake.password(length=10),
        "administrador": administrador,
    }


def novo_usuario_admin() -> dict:
    """Atalho para gerar um usuário administrador."""
    return novo_usuario(administrador="true")


def usuario_sem_campo(campo: str) -> dict:
    """
    Gera um payload com um campo propositalmente removido.
    Útil para testes de validação de campos obrigatórios.

    Exemplo: usuario_sem_campo("email") retorna payload sem email.
    """
    payload = novo_usuario()
    payload.pop(campo, None)
    return payload