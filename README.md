# 🧪 Testes Automatizados — ServeRest Usuários

Projeto de automação de testes para o endpoint `/usuarios` da API **ServeRest**, desenvolvido com **Python**, **Pytest**, **Requests** e **Faker**.

---

## 📌 Sobre o projeto

Este projeto faz parte de um desafio de automação de testes de API, com foco em boas práticas de organização, cobertura de cenários e independência entre testes.

A API testada simula uma loja virtual e está disponível em:

```
https://compassuol.serverest.dev
```

Endpoint coberto:

```
/usuarios
```

---

## 🛠️ Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/)
- [Pytest](https://docs.pytest.org/)
- [Requests](https://requests.readthedocs.io/)
- [Faker](https://faker.readthedocs.io/) — geração de dados dinâmicos em português
- [Python-dotenv](https://pypi.org/project/python-dotenv/) — variáveis de ambiente

---

## 📁 Estrutura do projeto

```
serverest-pytest/
│
├── services/
│   └── usuarios_service.py     # Chamadas HTTP com requests.Session
│
├── tests/
│   ├── conftest.py             # Fixtures compartilhadas
│   └── test_usuarios.py        # Casos de teste
│
├── utils/
│   └── data_factory.py         # Geração de dados com Faker
│
├── .env.example                # Exemplo de variáveis de ambiente
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## ⚙️ Como instalar

### 1. Clone o repositório

```bash
git clone https://github.com/kauakirk/serverest-pytest.git
```

### 2. Crie o ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

O arquivo `.env.example` contém:

```
BASE_URL=https://compassuol.serverest.dev
```

---

## ▶️ Como executar os testes

### Todos os testes
```bash
pytest
```

### Com detalhes no terminal
```bash
pytest -v
```

### Apenas testes de cadastro
```bash
pytest -m cadastro
```

### Apenas cenários negativos
```bash
pytest -m negativo
```

### Um teste específico
```bash
pytest tests/test_usuarios.py::test_cadastrar_usuario_valido_retorna_201 -v
```

### Problemas comuns

- Se ao rodar `pytest` você vir erro como `ModuleNotFoundError: No module named 'services'`, execute o pytest através do launcher do Python para garantir que o diretório do projeto esteja no `sys.path`:

```powershell
py -m pytest -q
# ou, se preferir verbose:
py -m pytest -v
```

- Alternativamente, em ambientes onde `python` aponta para o interpretador correto, use:

```powershell
python -m pytest -q
```

---

## 🧩 Markers disponíveis

| Marker | Descrição |
|---|---|
| `usuarios` | Todos os testes do endpoint /usuarios |
| `listagem` | Testes de GET /usuarios |
| `cadastro` | Testes de POST /usuarios |
| `busca` | Testes de GET /usuarios/{id} |
| `atualizacao` | Testes de PUT /usuarios/{id} |
| `exclusao` | Testes de DELETE /usuarios/{id} |
| `negativo` | Cenários de erro esperado |

---

## ✅ Cenários testados

| Teste | Método | Endpoint | Tipo |
|---|---|---|---|
| Listar usuários | GET | `/usuarios` | Positivo |
| Listar filtrando por nome | GET | `/usuarios?nome=` | Positivo |
| Listar filtrando por email | GET | `/usuarios?email=` | Positivo |
| Cadastrar usuário válido | POST | `/usuarios` | Positivo |
| Cadastrar usuário administrador | POST | `/usuarios` | Positivo |
| Cadastrar com email duplicado | POST | `/usuarios` | Negativo |
| Cadastrar sem campo obrigatório (x4) | POST | `/usuarios` | Negativo |
| Buscar usuário por ID válido | GET | `/usuarios/{id}` | Positivo |
| Buscar usuário com ID inexistente | GET | `/usuarios/{id}` | Negativo |
| Atualizar usuário | PUT | `/usuarios/{id}` | Positivo |
| Validar dados após atualização | PUT + GET | `/usuarios/{id}` | Positivo |
| Deletar usuário existente | DELETE | `/usuarios/{id}` | Positivo |
| Deletar usuário inexistente | DELETE | `/usuarios/{id}` | Negativo |

**Total: 16 cenários** (sendo 4 gerados via `@pytest.mark.parametrize`)

---

## 🎯 Estratégia adotada

- **`requests.Session`** — reutiliza a conexão HTTP e centraliza headers em um único lugar, evitando repetição em cada chamada
- **Faker com locale `pt_BR`** — gera nomes e emails brasileiros únicos a cada execução, sem colisão entre testes
- **Fixture com cleanup automático** — o `conftest.py` cria o usuário antes do teste e deleta automaticamente após, sem deixar lixo na API
- **`@pytest.mark.parametrize`** — os 4 campos obrigatórios são validados em um único teste parametrizado, eliminando repetição de código
- **Validação além do status code** — além de checar o HTTP status, os testes validam a estrutura do JSON, os dados retornados e a consistência após operações de escrita
- **Testes independentes** — nenhum teste depende da execução de outro para funcionar

---

## 👤 Autor

[@kauakirk](https://github.com/kauakirk)
