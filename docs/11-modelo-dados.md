# Modelo de Dados e DER (Diagrama Entidade-Relacionamento)

Para garantir a integridade referencial, o desempenho nas consultas por unidade e a atomicidade nas transações (como a baixa de estoque), o banco de dados relacional foi estruturado com as seguintes entidades principais:

## Principais Entidades e Atributos

### 1. Usuario
* `id` (PK, Integer)
* `nome` (String)
* `email` (String, Unique)
* `senha_hash` (String - Criptografada via bcrypt)
* `perfil` (Enum: `CLIENTE`, `ATENDENTE`, `COZINHA`, `GERENTE`, `MATRIZ`)

### 2. Unidade
* `id` (PK, Integer)
* `nome` (String)
* `cidade` / `regiao` (String)

### 3. Produto
* `id` (PK, Integer)
* `nome` (String)
* `descricao` (Text)
* `preco` (Decimal)
* `unidade_id` (FK → Unidade)
* `ativo` (Boolean)

### 4. Estoque
* `id` (PK, Integer)
* `produto_id` (FK → Produto)
* `quantidade_disponivel` (Integer)

### 5. Pedido
* `id` (PK, Integer)
* `cliente_id` (FK → Usuario)
* `unidade_id` (FK → Unidade)
* `canal_pedido` (Enum: `APP`, `TOTEM`, `BALCAO`, `PICKUP`, `WEB`)
* `status` (Enum: `AGUARDANDO_PAGAMENTO`, `EM_PREPARO`, `PRONTO`, `ENTREGUE`, `CANCELADO`)
* `valor_total` (Decimal)
* `data_criacao` (Timestamp)

### 6. ItemPedido (Tabela Associativa)
* `id` (PK, Integer)
* `pedido_id` (FK → Pedido)
* `produto_id` (FK → Produto)
* `quantidade` (Integer)
* `preco_unitario` (Decimal)

### 7. Pagamento
* `id` (PK, Integer)
* `pedido_id` (FK → Pedido)
* `status_pagamento` (Enum: `APROVADO`, `RECUSADO`, `PENDENTE`)
* `data_pagamento` (Timestamp)
* `valor` (Decimal)

---

## Relacionamentos

- **Usuario (perfil CLIENTE) → Pedido:** 1:N  
- **Unidade → Produto:** 1:N  
- **Produto → Estoque:** 1:1  
- **Pedido → ItemPedido:** 1:N  
- **Pedido → Pagamento:** 1:1  

---

## Diagrama Textual Simplificado (ERD)

Usuario (perfil CLIENTE) (1) ────< Pedido (N)
Pedido (1) ────< ItemPedido (N)
Unidade (1) ────< Produto (N)
Produto (1) ────< Estoque (1)
Pedido (1) ────< Pagamento (1)


---

## Observações Técnicas

- Implementação inicial em **SQLite** via **SQLAlchemy ORM** para simplicidade e portabilidade.  
- Evolução futura para **PostgreSQL** visando maior volume de dados e concorrência.  
- Relacionamentos garantem integridade referencial com PK e FK.  
- O campo `perfil` em **Usuario** permite diferenciar funções sem duplicar tabelas.  
- O campo `canal_pedido` rastreia a origem do pedido (APP, TOTEM, BALCAO, PICKUP, WEB).  
