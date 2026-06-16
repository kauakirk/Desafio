# Testes Automatizados de API com Pytest

Projeto desenvolvido para praticar testes automatizados de APIs REST utilizando Python, Requests e Pytest.

## Tecnologias Utilizadas

- Python 3
- Pytest
- Requests
- UUID

## API Testada

https://compassuol.serverest.dev

## Instalação

Clone o projeto:

```bash
git clone <url-do-repositorio>
cd test-api
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando os Testes

Execute todos os testes:

```bash
pytest
```

Execute testes de um arquivo específico:

```bash
pytest tests/test_usuario.py -v
```

Execute um teste específico:

```bash
pytest tests/test_usuario.py::test_can_create_user -v
```

---

## 📊 Análise de Cobertura de Testes

### Metodologia

A cobertura de testes foi calculada utilizando os critérios definidos no artigo ["Como verificar a cobertura de testes da API REST"](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b) de Nayara Crema, que define os seguintes critérios de entrada (Input) e saída (Output):

- **Path Coverage (Input)**: Endpoints cobertos / Total de endpoints
- **Operator Coverage (Input)**: Operações (GET, POST, PUT, DELETE) cobertas / Total de operações
- **Parameter Coverage (Input)**: Parâmetros de entrada cobertos / Total de parâmetros
- **Status Code Coverage (Output)**: Status codes cobertos / Total de status codes possíveis
- **Operation Flow (Input)**: Fluxos de operação cobertos / Total de fluxos possíveis
- **JSON Schema Validation**: validação de payloads e respostas com jsonschema

### Resultados de Cobertura

| Critério | Coberto | Total | Percentual |
|----------|---------|-------|-----------|
| **Path Coverage** | 16 | 16 | **100%** |
| **Operator Coverage** | 16 | 16 | **100%** |
| **Parameter Coverage** | 8 | 12 | **67%** |
| **Status Code Coverage** | 5 | 8 | **63%** |
| **Operation Flow Coverage** | 11 | 15 | **73%** |
| **Cobertura Total Média** | - | - | **~80.6%** |

### Detalhamento por Critério

#### 1. Path Coverage - **100%**

Todos os 16 endpoints planejados foram implementados com testes:

✅ **Usuários (5 endpoints)**
- `GET /usuarios` - Listar usuários
- `POST /usuarios` - Criar usuário
- `GET /usuarios/{id}` - Buscar por ID
- `PUT /usuarios/{id}` - Atualizar usuário
- `DELETE /usuarios/{id}` - Deletar usuário

✅ **Autenticação (1 endpoint)**
- `POST /login` - Login de usuário

✅ **Produtos (5 endpoints)**
- `GET /produtos` - Listar produtos
- `POST /produtos` - Criar produto
- `GET /produtos/{id}` - Buscar por ID
- `PUT /produtos/{id}` - Atualizar produto
- `DELETE /produtos/{id}` - Deletar produto

✅ **Carrinhos (5 endpoints)**
- `GET /carrinhos` - Listar carrinhos
- `POST /carrinhos` - Criar carrinho
- `GET /carrinhos/{id}` - Buscar por ID
- `DELETE /carrinhos/concluir-compra` - Concluir compra
- `DELETE /carrinhos/cancelar-compra` - Cancelar compra

#### 2. Operator Coverage - **100%**

Todos os 16 operações estão cobertas:

- **GET**: 6 operações cobertos (usuarios list, usuarios by id, produtos list, produtos by id, carrinhos list, carrinhos by id)
- **POST**: 4 operações cobertos (usuarios create, login, produtos create, carrinhos create)
- **PUT**: 2 operações cobertos (usuarios update, produtos update)
- **DELETE**: 4 operações cobertos (usuarios delete, produtos delete, concluir-compra, cancelar-compra)

#### 3. Parameter Coverage - **67%**

**Parâmetros cobertos (8 de 12):**
- ✅ Body: `nome`, `email`, `password`, `administrador` (usuários)
- ✅ Body: `nome`, `preco`, `descricao`, `quantidade` (produtos)
- ✅ Path: `_id` (em usuários, produtos, carrinhos)
- ✅ Header: `Authorization` (token)

**Parâmetros não cobertos (4 de 12):**
- ❌ Body: `idProduto`, `quantidade` (em carrinhos - parâmetros de seleção)
- ❌ Path: `idProduto` em carrinho
- ❌ Query: filtros avançados (não especificados na API)
- ❌ Content-Type alternativo (apenas `application/json` foi testado)

#### 4. Status Code Coverage - **63%**

**Status codes cobertos (5 de 8):**
- ✅ **200** (OK): GET list, DELETE success, PUT success
- ✅ **201** (Created): POST create, PUT create (via ID inexistente)
- ✅ **400** (Bad Request): validações de entrada (email ausente, email duplicado, campos vazios)
- ✅ **401** (Unauthorized): tentativas sem token ou token inválido
- ✅ **403** (Forbidden): acesso negado para não-administradores

**Status codes não cobertos (3 de 8):**
- ❌ **204** (No Content): não testado (API pode não usar)
- ❌ **404** (Not Found): tentativas de buscar recursos não existentes
- ❌ **500** (Internal Server Error): erros do servidor

#### 5. Operation Flow Coverage - **73%**

**Fluxos cobertos (11 de 15):**

✅ **Fluxos de Usuários**
1. POST /usuarios → GET /usuarios (list)
2. POST /usuarios → GET /usuarios?_id (by ID)
3. POST /usuarios → PUT /usuarios/{id}
4. POST /usuarios → DELETE /usuarios/{id}

✅ **Fluxos de Autenticação**
5. POST /usuarios → POST /login → validar token

✅ **Fluxos de Produtos**
6. POST /produtos (admin) → GET /produtos
7. POST /produtos → GET /produtos/{id}
8. POST /produtos → PUT /produtos/{id}
9. POST /produtos → DELETE /produtos/{id}

✅ **Fluxos de Carrinhos**
10. POST /usuarios → POST /login → POST /carrinhos → GET /carrinhos/{id}
11. POST /carrinhos → DELETE /carrinhos/concluir-compra

**Fluxos não cobertos (4 de 15):**
- ❌ Fluxo de produto não encontrado (GET /produtos/{id} com ID inválido)
- ❌ Fluxo de carrinho com produto sem estoque
- ❌ Fluxo de múltiplos produtos em um carrinho (quantidade > 1)
- ❌ Fluxo de busca com múltiplos filtros

### Cenários Fora do Escopo

Os seguintes cenários **não foram implementados** e continuam fora do escopo:

| Cenário | Motivo |
|---------|--------|
| Teste com ID de recurso **404 (Not Found)** | Requer validação de resposta específica para IDs inexistentes, não documentado no plano inicial |
| Teste de **Content-Type alternativo (XML)** | A API aparenta suportar apenas JSON; não foi especificado no plano |
| Teste de **múltiplos produtos em um carrinho** | Funcionalidade complexa, fora do escopo de MVP |
| Teste de **produto com estoque insuficiente** | Validação de negócio complexa, não priorizada |
| Teste de **status 500** | Requer simulação de erro no servidor, não é testável em API pública |
| Teste de **performance/carga** | Explicitamente fora do escopo do projeto |
| Teste de **UI/Frontend** | Projeto focado em testes de API |

### Resumo Executivo

A suíte de testes alcançou uma **cobertura média de ~80.6%** através de:

- ✅ **100% de Path Coverage** - Todos os endpoints estão cobertos
- ✅ **100% de Operator Coverage** - Todos os métodos HTTP estão testados
- ⚠️ **67% de Parameter Coverage** - Parâmetros principais cobertos, mas sem testar todas as combinações
- ⚠️ **63% de Status Code Coverage** - Status codes principais cobertos, mas faltam 404 e 500
- ⚠️ **73% de Operation Flow Coverage** - Fluxos principais cobertos, alguns cenários edge não testados

**Conclusão**: A suíte fornece confiança nos fluxos principais e happy paths da API. Melhorias futuras podem focar em cenários de erro (404, 500) e validações edge-case.

---

## 🚀 Próximos Passos para Melhorar Cobertura

### Prioridade Alta
1. **Adicionar testes de 404 (Not Found)**
   - GET /usuarios/{id_inexistente}
   - GET /produtos/{id_inexistente}
   - GET /carrinhos/{id_inexistente}

2. **Testar fluxos com estoque insuficiente**
   - POST /carrinhos com quantidade > estoque

3. **Validar responses completas**
   - Verificar todas as propriedades retornadas, não apenas as principais

### Prioridade Média
4. **Adicionar testes de content-type alternativo**
   - Se a API suportar XML, testar `Accept: application/xml`

5. **Testar múltiplos produtos em um carrinho**
   - POST /carrinhos com vários idProduto

6. **Validar regras de negócio específicas**
   - Email com caracteres especiais
   - Campos muito longos (string limit)

### Prioridade Baixa
7. **Testes de performance**
   - Tempo de resposta aceitável
   - Quantidade máxima de requisições

8. **Integração contínua**
   - GitHub Actions para rodar testes em cada push
   - Relatório de cobertura automatizado

---

## 📁 Estrutura do Projeto

```
tests/
├── conftest.py           # Fixtures de sessão (tokens admin/user)
├── test_usuario.py       # 12 testes para usuários
├── test_login.py         # 4 testes para autenticação
├── test_produtos.py      # 7 testes para produtos
└── test_carrinhos.py     # 5 testes para carrinhos

services/
├── usuarios_service.py   # Requisições para /usuarios
├── produtos_service.py   # Requisições para /produtos
├── carrinhos_service.py  # Requisições para /carrinhos
└── api_client.py         # Cliente HTTP genérico

utils/
├── payloads.py           # Builders de dados de teste
├── schemas.py            # Definições JSON Schema (entrada e resposta)
├── validator.py          # Funções de validação JSON Schema
└── auth.py               # Funções de autenticação com cache de token

PLANO-DE-TESTES.md        # Documentação do escopo
COVERAGE_REPORT.md        # Relatório detalhado de cobertura
COBERTURA_VISUAL.md       # Resumo visual de cobertura
pytest.ini                # Configuração do pytest
```

---

## 📝 Referências

- [Artigo: Como verificar cobertura de testes API REST](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b)
- [API ServeRest](https://compassuol.serverest.dev)
- [Documentação Pytest](https://docs.pytest.org/)
- [Python Requests](https://docs.python-requests.org/)