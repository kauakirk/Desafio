import requests


class UsuariosService:
    """
    Service responsável pelas chamadas HTTP do endpoint /usuarios.
    Utiliza requests.Session para reutilizar a conexão e centralizar
    configurações como headers e base_url.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.endpoint = f"{base_url}/usuarios"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def listar_usuarios(self, params: dict = None):
        """GET /usuarios — lista todos os usuários, com filtros opcionais."""
        return self.session.get(self.endpoint, params=params)

    def cadastrar_usuario(self, payload: dict):
        """POST /usuarios — cadastra um novo usuário."""
        return self.session.post(self.endpoint, json=payload)

    def buscar_por_id(self, usuario_id: str):
        """GET /usuarios/{id} — busca um usuário específico pelo ID."""
        return self.session.get(f"{self.endpoint}/{usuario_id}")

    def atualizar_usuario(self, usuario_id: str, payload: dict):
        """PUT /usuarios/{id} — atualiza os dados de um usuário."""
        return self.session.put(f"{self.endpoint}/{usuario_id}", json=payload)

    def deletar_usuario(self, usuario_id: str):
        """DELETE /usuarios/{id} — remove um usuário pelo ID."""
        return self.session.delete(f"{self.endpoint}/{usuario_id}")

    def fechar(self):
        """Encerra a sessão HTTP."""
        self.session.close()