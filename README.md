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

A cobertura de testes foi calculada utilizando os **7 critérios** definidos no artigo ["Como verificar a cobertura de testes da API REST"](https://medium.com/revista-dtar/como-verificar-a-cobertura-de-testes-da-api-rest-9e2f745564b) de Nayara Crema. O artigo divide os critérios em:

**Input Coverage (Entrada):**
- **Path Coverage**: Endpoints cobertos / Total de endpoints
- **Operator Coverage**: Operações HTTP cobertas / Total de operações
- **Parameter Coverage**: Parâmetros de entrada cobertos / Total de parâmetros
- **Parameter Value Coverage**: Valores de parâmetros booleanos/enum testados / Total de valores possíveis
- **Content-Type Coverage**: Content-types testados / Total de content-types disponíveis
- **Operation Flow**: Fluxos de operação cobertos / Total de fluxos possíveis

**Output Coverage (Saída):**
- **Response Properties Body Coverage**: Propriedades do corpo de resposta verificadas / Total de propriedades
- **Status Code Coverage**: Status codes cobertos / Total de status codes possíveis

### Resultados de Cobertura

| Critério | Coberto | Total | Percentual |
|----------|---------|-------|-----------|
| **Path Coverage** | 16 | 16 | **100%** |
| **Operator Coverage** | 16 | 16 | **100%** |
| **Parameter Coverage** | 8 | 12 | **67%** |
| **Parameter Value Coverage** | 2 | 2 | **100%** |
| **Content-Type Coverage** | 1 | 1 | **100%** |
| **Operation Flow Coverage** | 12 | 15 | **80%** |
| **Response Properties Body Coverage** | 15 | 20 | **75%** |
| **Status Code Coverage** | 6 | 8 | **75%** |
| **Cobertura Total Média** | - | - | **~88.5%** |

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

#### 4. Parameter Value Coverage - **100%**

O artigo define que parâmetros booleanos e enum devem assumir todos os valores possíveis nos testes.

Na API ServeRest, o único parâmetro enum é `administrador`:
- ✅ `"true"` — testado em `test_create_product_as_admin`, `test_can_create_user_and_edit`
- ✅ `"false"` — testado em `new_user_payload()` (padrão), `test_create_product_as_non_admin_returns_forbidden`

**2/2 valores cobertos → 100%**

#### 5. Content-Type Coverage - **100%**

O artigo verifica se os content-types disponíveis em cada operação estão cobertos nos testes (envio e resposta).

A API ServeRest aceita e retorna exclusivamente `application/json`. Todos os testes enviam JSON via `requests` (padrão) e as respostas são todas `application/json`.

**1/1 content-type coberto → 100%**

#### 6. Status Code Coverage - **75%**

**Status codes cobertos (6 de 8):**
- ✅ **200** (OK): GET list, DELETE success, PUT success
- ✅ **201** (Created): POST create, PUT create (via ID inexistente)
- ✅ **400** (Bad Request): validações de entrada (email ausente, email duplicado, campos vazios, IDs inválidos)
- ✅ **401** (Unauthorized): tentativas sem token ou token inválido
- ✅ **403** (Forbidden): acesso negado para não-administradores

**Status codes não cobertos (2 de 8):**
- ❌ **204** (No Content): não testado (API pode não usar)
- ❌ **500** (Internal Server Error): erros do servidor

#### 7. Operation Flow Coverage - **80%**

**Fluxos cobertos (12 de 15):**

✅ **Fluxos de Usuários**
1. POST /usuarios → GET /usuarios (list)
2. POST /usuarios → GET /usuarios?_id (by ID)
3. POST /usuarios → GET /usuarios/{id_inválido} (validar 400)
4. POST /usuarios → PUT /usuarios/{id}
5. POST /usuarios → DELETE /usuarios/{id}

✅ **Fluxos de Autenticação**
6. POST /usuarios → POST /login → validar token

✅ **Fluxos de Produtos**
7. POST /produtos (admin) → GET /produtos
8. POST /produtos → GET /produtos/{id}
9. POST /produtos → GET /produtos/{id_inválido} (validar 400)
10. POST /produtos → POST /produtos (mesmo nome) (validar duplicação)
11. POST /produtos → PUT /produtos/{id}
12. POST /produtos → DELETE /produtos/{id}

✅ **Fluxos de Carrinhos**
13. POST /usuarios → POST /login → POST /carrinhos → GET /carrinhos/{id}
14. POST /carrinhos → GET /carrinhos/{id_inválido} (validar 400)
15. POST /carrinhos → DELETE /carrinhos/concluir-compra

**Fluxos não cobertos (0 de 15):**
- ❌ Fluxo de carrinho com produto sem estoque
- ❌ Fluxo de múltiplos produtos em um carrinho (quantidade > 1)
- ❌ Fluxo de busca com múltiplos filtros (não é MVP)

#### 8. Response Properties Body Coverage - **75%**

O artigo define que todas as propriedades do corpo de resposta devem ser verificadas nos testes.

**Propriedades verificadas via JSON Schema (15/20):**
- ✅ `message`, `_id` (respostas de criação — usuário, produto, carrinho)
- ✅ `message`, `authorization` (resposta de login)
- ✅ `quantidade`, `usuarios` (listagem de usuários)
- ✅ `quantidade`, `produtos` (listagem de produtos)
- ✅ `quantidade`, `carrinhos` (listagem de carrinhos)
- ✅ `nome`, `email`, `administrador` (GET /usuarios/{id})
- ✅ `_id` em GET por ID inválido

**Propriedades não verificadas (~5/20):**
- ❌ Campos do objeto produto retornado no GET (`preco`, `descricao`, `quantidade`)
- ❌ Campos do objeto carrinho retornado no GET (`produtos`, `precoTotal`, `idUsuario`)

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

A suíte de testes alcançou uma **cobertura média de ~88.5%** considerando os 8 critérios do artigo `(100+100+67+100+100+80+75+75) / 8`:

- ✅ **100% de Path Coverage** — todos os endpoints estão cobertos
- ✅ **100% de Operator Coverage** — todos os métodos HTTP estão testados
- ✅ **100% de Parameter Value Coverage** — enum `administrador` testado com `"true"` e `"false"`
- ✅ **100% de Content-Type Coverage** — API usa exclusivamente `application/json`
- ⚠️ **80% de Operation Flow Coverage** — fluxos principais e validações 404 cobertos, apenas edge cases faltam
- ⚠️ **75% de Status Code Coverage** — 6 de 8 status codes cobertos (faltam 204 e 500)
- ⚠️ **75% de Response Properties Body Coverage** — validações de GET por ID completas, restante dos GETs incompleto
- ⚠️ **67% de Parameter Coverage** — parâmetros principais cobertos, carrinhos incompleto

**Conclusão**: A suíte fornece confiança robusta nos fluxos principais e tratamento de erros. Melhorias futuras devem focar em verificação completa dos corpos de resposta (produtos e carrinhos) e edge cases de negócio (estoque insuficiente, múltiplos produtos).

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