# PLANO-DE-TESTES

## Objetivo da suíte

O objetivo desta suíte de testes é validar o comportamento da API de usuários e garantir que os principais fluxos de cadastro, autenticação e gerenciamento de usuário funcionem corretamente. O foco inicial é oferecer confiança na camada de API REST do serviço público `https://compassuol.serverest.dev` e suportar a evolução dos testes conforme o desafio avança.

## Estratégia

- Tipo de teste: Testes de API automatizados.
- Camada: camada de integração / contrato da API, com foco na validação de endpoints REST.
- Ferramentas: Python, Requests, Pytest e jsonschema.
- Abordagem: validar respostas HTTP, contratos JSON via JSON Schema, fluxos de criação/edição/exclusão de usuários e tratamento de erros.

## Escopo

### Coberto

- Endpoints de usuários:
  - `GET /usuarios` - listar usuários
  - `POST /usuarios` - criar usuário
  - `GET /usuarios/{_id}` - buscar usuário por ID (path param)
  - `PUT /usuarios/{_id}` - editar usuário
  - `DELETE /usuarios/{_id}` - excluir usuário
- Endpoint de autenticação:
  - `POST /login` - login de usuário
- Endpoint de produtos:
  - `GET /produtos` - listar produtos
  - `POST /produtos` - cadastrar produto (exige token de admin)
  - `GET /produtos/{_id}` - buscar produto por ID
  - `PUT /produtos/{_id}` - editar produto (exige token de admin)
  - `DELETE /produtos/{_id}` - excluir produto (exige token de admin)
- Endpoint de carrinhos:
  - `GET /carrinhos` - listar carrinhos
  - `POST /carrinhos` - cadastrar carrinho (exige token do usuário)
  - `GET /carrinhos/{_id}` - buscar carrinho por ID
  - `DELETE /carrinhos/concluir-compra` - concluir compra do carrinho autenticado
  - `DELETE /carrinhos/cancelar-compra` - cancelar compra e reabastecer estoque
- Regras de negócio importantes:
  - não permitir cadastro com email já existente
  - não permitir edição para email já utilizado por outro usuário
  - permitir criação de usuário via PUT em ID inexistente, conforme comportamento observado
  - validar mensagens e códigos de status esperados
  - validar autorização de rotas administrativas para produtos
  - validar fluxo de token para carrinho vinculado ao usuário logado

### Fora do escopo inicial

- Testes de performance ou carga
- Testes de UI ou frontend

## Organização dos testes

- `test_usuario.py` - casos de usuário e endpoints de cadastro/consulta/edição/exclusão
- `test_login.py` - casos de autenticação de usuário
- `test_produtos.py` - casos de produtos com autorização de administrador
- `test_carrinhos.py` - casos de carrinho e fluxo de usuário autenticado

## Cenários a implementar

> Legenda: ✅ implementado | ⬜ pendente

### Endpoint `GET /usuarios`

- ✅ Deve retornar status `200` e lista de usuários
- ✅ Deve retornar os campos esperados `quantidade` e `usuarios`

### Endpoint `POST /usuarios`

- ✅ Deve criar um usuário com sucesso e retornar `201`
- ✅ Deve falhar com `400` quando `email` estiver ausente
- ✅ Deve falhar com `400` quando o email já estiver em uso

### Endpoint `POST /login`

- ✅ Deve autenticar um usuário válido e retornar `200`
- ✅ Deve retornar token/autorização no corpo da resposta
- ✅ Deve falhar com `401` quando a senha estiver incorreta
- ✅ Deve falhar com `401` quando o email não existir
- ✅ Deve falhar com `400` quando campos estiverem vazios

### Endpoint `GET /usuarios/{id}`

- ✅ Deve retornar o usuário correto ao buscar por ID
- ✅ Deve retornar o campo `_id` correspondente ao ID buscado

### Endpoint `PUT /usuarios/{id}`

- ✅ Deve editar um usuário existente e retornar `200`
- ✅ Deve permitir criar um novo usuário via `PUT` em ID inexistente e retornar `201`
- ✅ Deve falhar com `400` ao tentar editar um usuário para um email já existente

### Endpoint `DELETE /usuarios/{id}`

- ✅ Deve excluir usuário existente e retornar mensagem de sucesso
- ✅ Deve retornar comportamento consistente quando o usuário não existe

### Endpoint `GET /produtos`

- ✅ Deve retornar status `200` e lista de produtos
- ✅ Deve retornar `quantidade` e `produtos`

### Endpoint `POST /produtos`

- ✅ Deve cadastrar produto com token de administrador e retornar `201`
- ✅ Deve falhar com `401` quando o token de admin estiver ausente
- ✅ Deve falhar com `403` quando o token não pertencer a administrador
- ⬜ Deve falhar com `400` quando nome de produto duplicado

### Endpoint `GET /produtos/{id}`

- ✅ Deve retornar o produto correto ao buscar por ID
- ⬜ Deve retornar `400` quando o produto não existir

### Endpoint `PUT /produtos/{id}`

- ✅ Deve editar produto existente com token de admin e retornar `200`
- ⬜ Deve criar novo produto se o ID não existir e retornar `201`
- ⬜ Deve falhar com `401` sem token de admin
- ⬜ Deve falhar com `403` quando o token não for de admin

### Endpoint `DELETE /produtos/{id}`

- ✅ Deve excluir produto existente com token de admin e retornar mensagem de sucesso
- ⬜ Deve falhar com `401` sem token de admin
- ⬜ Deve falhar com `403` quando o token não for de admin
- ⬜ Deve falhar com `400` quando o produto faz parte de carrinho

### Endpoint `GET /carrinhos`

- ✅ Deve retornar status `200` e lista de carrinhos
- ✅ Deve retornar `quantidade` e `carrinhos`

### Endpoint `POST /carrinhos`

- ✅ Deve cadastrar carrinho com token de usuário e retornar `201`
- ⬜ Deve falhar com `401` quando o token estiver ausente ou inválido
- ⬜ Deve falhar com `400` para produtos inválidos, quantidade insuficiente ou duplicada

### Endpoint `GET /carrinhos/{id}`

- ✅ Deve retornar o carrinho correto ao buscar por ID
- ⬜ Deve retornar `400` quando o carrinho não existir

### Endpoint `DELETE /carrinhos/concluir-compra`

- ✅ Deve excluir o carrinho do usuário autenticado e retornar mensagem de sucesso
- ✅ Deve retornar mensagem consistente quando não existir carrinho para o usuário
- ⬜ Deve falhar com `401` sem token válido

### Endpoint `DELETE /carrinhos/cancelar-compra`

- ✅ Deve excluir o carrinho e reabastecer estoque
- ✅ Deve retornar mensagem consistente quando não existir carrinho
- ⬜ Deve falhar com `401` sem token válido

## Critérios de qualidade

- Um teste está pronto quando:
  - valida o status HTTP esperado
  - valida o corpo da resposta e os campos essenciais
  - valida o payload e/ou response via JSON Schema sempre que aplicável
  - isola o caso de teste criando dados únicos quando necessário
  - não depende de dados de outros testes
  - roda de forma confiável em sequência e em execução isolada
  - documenta claramente o objetivo do caso de teste

## Observações iniciais

- A API pública do ServeRest tem documentação disponível em `https://compassuol.serverest.dev/` e `https://compassuol.serverest.dev/swagger.json?lang=pt-BR`.
- Este documento deve ser atualizado sempre que novos endpoints, regras de negócio ou critérios forem adicionados.
