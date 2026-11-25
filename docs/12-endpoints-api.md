# Endpoints da API

## Objetivo
Este documento especifica os principais endpoints da API REST que suportam os casos de uso e o modelo de dados definidos anteriormente. Todos os endpoints seguem o padrão RESTful e retornam respostas em JSON.

---

## Autenticação
- **POST /auth/login**
  - Entrada: `{ email, senha }`
  - Saída: `{ token_jwt }`
  - Erros: `401 Unauthorized`

---

## Usuários
- **POST /usuarios**
  - Cria um novo usuário (perfil CLIENTE, ATENDENTE, etc.)
- **GET /usuarios/{id}**
  - Retorna dados de um usuário específico
- **PUT /usuarios/{id}**
  - Atualiza dados do usuário
- **DELETE /usuarios/{id}**
  - Remove usuário

---

## Produtos
- **GET /produtos**
  - Lista produtos ativos por unidade
- **POST /produtos**
  - Cria novo produto vinculado a uma unidade
- **PUT /produtos/{id}**
  - Atualiza informações do produto
- **DELETE /produtos/{id}**
  - Remove produto

---

## Estoque
- **GET /estoque/{produto_id}**
  - Consulta quantidade disponível
- **PUT /estoque/{produto_id}**
  - Atualiza saldo de estoque

---

## Pedidos
- **POST /pedidos**
  - Cria novo pedido (perfil CLIENTE)
- **GET /pedidos/{id}**
  - Retorna detalhes de um pedido
- **PUT /pedidos/{id}/status**
  - Atualiza status do pedido (`EM_PREPARO`, `PRONTO`, etc.)
- **GET /pedidos?cliente_id=...**
  - Lista pedidos de um cliente

---

## Itens do Pedido
- **POST /pedidos/{id}/itens**
  - Adiciona item ao pedido
- **DELETE /pedidos/{id}/itens/{item_id}**
  - Remove item do pedido

---

## Pagamentos
- **POST /pagamentos**
  - Processa pagamento de um pedido
- **GET /pagamentos/{pedido_id}**
  - Consulta status do pagamento

-----------------------------------------------------------

# 12. Endpoints da API

## Objetivo
Este documento especifica os principais endpoints da API REST que suportam os casos de uso e o modelo de dados definidos anteriormente. Todos os endpoints seguem o padrão RESTful e retornam respostas em JSON.

---

## Autenticação

### POST /auth/login
- **Descrição:** Realiza login e retorna token JWT.
- **Entrada:**
```json
{ "email": "cliente@exemplo.com", "senha": "123456" }

Saída:

json
{ "token": "jwt_token_aqui", "expira_em": "2026-11-01T14:00:00" }
Erros: 401 Unauthorized

Usuários
POST /usuarios
Descrição: Cria novo usuário (perfil CLIENTE, ATENDENTE, etc.)

Entrada:

json
{ "nome": "Maria Silva", "email": "maria@exemplo.com", "senha": "123456", "perfil": "CLIENTE" }
Saída:

json
{ "id": 1, "nome": "Maria Silva", "email": "maria@exemplo.com", "perfil": "CLIENTE" }
GET /usuarios/{id}
Descrição: Retorna dados de um usuário específico.

Saída:

json
{ "id": 1, "nome": "Maria Silva", "email": "maria@exemplo.com", "perfil": "CLIENTE" }
Produtos
GET /produtos?unidade_id=1
Descrição: Lista produtos ativos de uma unidade.

Saída:

json
[
  { "id": 10, "nome": "Cuscuz Nordestino", "preco": 12.50, "ativo": true, "unidade_id": 1 }
]
POST /produtos
Descrição: Cria novo produto vinculado a uma unidade.

Entrada:

json
{ "nome": "Tapioca", "descricao": "Tapioca com queijo coalho", "preco": 8.00, "unidade_id": 1, "ativo": true }
Estoque
GET /estoque/{produto_id}
Descrição: Consulta quantidade disponível.

Saída:

json
{ "produto_id": 10, "quantidade_disponivel": 25 }
PUT /estoque/{produto_id}
Descrição: Atualiza saldo de estoque.

Entrada:

json
{ "quantidade_disponivel": 30 }
Pedidos
POST /pedidos
Descrição: Cria novo pedido.

Entrada:

json
{
  "cliente_id": 1,
  "unidade_id": 1,
  "canal_pedido": "APP",
  "itens": [ { "produto_id": 10, "quantidade": 2 } ]
}
Saída:

json
{ "id": 100, "status": "AGUARDANDO_PAGAMENTO", "valor_total": 25.00, "data_criacao": "2026-11-01T13:55:00" }
GET /pedidos/{id}
Descrição: Retorna detalhes de um pedido.

Saída:

json
{
  "id": 100,
  "cliente_id": 1,
  "unidade_id": 1,
  "status": "EM_PREPARO",
  "valor_total": 25.00,
  "itens": [ { "produto_id": 10, "quantidade": 2, "preco_unitario": 12.50 } ]
}
Pagamentos
POST /pagamentos
Descrição: Processa pagamento de um pedido.

Entrada:

json
{ "pedido_id": 100, "valor": 25.00, "metodo": "CARTAO" }
Saída:

json
{ "id": 200, "pedido_id": 100, "status_pagamento": "APROVADO", "data_pagamento": "2026-11-01T13:56:00", "valor": 25.00 }
GET /pagamentos/{pedido_id}
Descrição: Consulta status do pagamento.

Saída:

json
{ "pedido_id": 100, "status_pagamento": "APROVADO" }
Código

