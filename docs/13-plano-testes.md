# 13. Plano de Testes

## 13.1. Objetivo

Validar os principais fluxos da aplicação Rede Raízes do Nordeste, verificando o funcionamento dos endpoints, as regras de negócio, a autenticação, o processamento de pedidos, os pagamentos, o controle de estoque e o programa de fidelidade.

Os testes foram divididos em duas categorias:

- **Testes automatizados:** executados por meio do Pytest.
- **Testes funcionais manuais:** realizados por meio da documentação interativa Swagger da API.

## 13.2. Ambiente de Testes

| Item | Tecnologia |
|---|---|
| Linguagem | Python 3.12.6 |
| Framework | FastAPI |
| Banco de dados | SQLite |
| ORM | SQLAlchemy |
| Validação de dados | Pydantic |
| Testes automatizados | Pytest |
| Cliente de testes | HTTPX |
| Documentação interativa | Swagger UI |

## 13.3. Cenários de Testes Funcionais

### 1. Autenticação

**Cenário 1.1 — Login com credenciais válidas**
- Entrada: e-mail e senha corretos.
- Resultado esperado: autenticação realizada e retorno de token JWT.
- Situação: funcionalidade validada manualmente.

**Cenário 1.2 — Login com credenciais inválidas**
- Entrada: e-mail ou senha incorretos.
- Resultado esperado: resposta HTTP `401 Unauthorized`.
- Situação: cenário previsto para validação funcional.

### 2. Pedido com Estoque Suficiente

**Cenário 2.1 — Cliente cria pedido com produtos disponíveis**
- Entrada: unidade válida, canal de pedido permitido e itens com quantidades positivas.
- Resultado esperado: pedido criado com status `AGUARDANDO_PAGAMENTO`.
- Resultado observado: pedido criado com HTTP `201 Created`.
- Situação: validado manualmente pelo Swagger.
# 13. Plano de Testes

## 13.1. Objetivo

Validar os principais fluxos da aplicação Rede Raízes do Nordeste, verificando o funcionamento dos endpoints, as regras de negócio, a autenticação, o processamento de pedidos, os pagamentos, o controle de estoque e o programa de fidelidade.

Os testes foram divididos em duas categorias:

- **Testes automatizados:** executados por meio do Pytest.
- **Testes funcionais manuais:** realizados por meio da documentação interativa Swagger da API.

## 13.2. Ambiente de Testes

| Item | Tecnologia |
|---|---|
| Linguagem | Python 3.12.6 |
| Framework | FastAPI |
| Banco de dados | SQLite |
| ORM | SQLAlchemy |
| Validação de dados | Pydantic |
| Testes automatizados | Pytest |
| Cliente de testes | HTTPX |
| Documentação interativa | Swagger UI |

## 13.3. Cenários de Testes Funcionais

### 1. Autenticação

**Cenário 1.1 — Login com credenciais válidas**
- Entrada: e-mail e senha corretos.
- Resultado esperado: autenticação realizada e retorno de token JWT.
- Situação: funcionalidade validada manualmente.

**Cenário 1.2 — Login com credenciais inválidas**
- Entrada: e-mail ou senha incorretos.
- Resultado esperado: resposta HTTP `401 Unauthorized`.
- Situação: cenário previsto para validação funcional.

### 2. Pedido com Estoque Suficiente

**Cenário 2.1 — Cliente cria pedido com produtos disponíveis**
- Entrada: unidade válida, canal de pedido permitido e itens com quantidades positivas.
- Resultado esperado: pedido criado com status `AGUARDANDO_PAGAMENTO`.
- Resultado observado: pedido criado com HTTP `201 Created`.
- Situação: validado manualmente pelo Swagger.

### 3. Pedido com Estoque Insuficiente

**Cenário 3.1 — Tentativa de pedido sem saldo suficiente**
- Entrada: produto cuja quantidade solicitada supera o estoque disponível.
- Resultado esperado: operação rejeitada, sem criação indevida do pedido.
- Situação: regra de negócio validada manualmente.

### 4. Pagamento Aprovado

**Cenário 4.1 — Simulação de pagamento aprovado**
- Entrada: pedido válido e simulação de pagamento aprovada.
- Resultado esperado: pagamento registrado com status `APROVADO`, pedido encaminhado para `EM_PREPARO` e estoque atualizado.
- Resultado observado: pagamento aprovado com HTTP `201 Created`.
- Situação: validado manualmente pelo Swagger.

### 5. Pagamento Recusado

**Cenário 5.1 — Simulação de pagamento recusado**
- Entrada: pedido válido e simulação de pagamento recusada.
- Resultado esperado: pagamento registrado com status `RECUSADO`, sem baixa indevida do estoque e sem avanço do pedido para preparação.
- Situação: cenário previsto para validação funcional.

### 6. Consentimento e LGPD

**Cenário 6.1 — Registro de consentimento**
- Entrada: cliente autenticado informa a finalidade do consentimento.
- Resultado esperado: registro do consentimento associado ao usuário.
- Resultado observado: consentimento registrado com HTTP `201 Created`.
- Situação: validado manualmente pelo Swagger.

### 7. Programa de Fidelidade

**Cenário 7.1 — Crédito de pontos após pagamento aprovado**
- Entrada: cliente com adesão ativa ao programa realiza pedido e obtém pagamento aprovado.
- Resultado esperado: pontos calculados conforme a regra de negócio de 1 ponto por real pago, com descarte de frações.
- Resultado observado: pedido de R$ 36,90 gerou 36 pontos.
- Situação: validado manualmente pelo Swagger.

**Cenário 7.2 — Consulta de saldo e histórico**
- Entrada: cliente autenticado consulta seus pontos.
- Resultado esperado: retorno do saldo e do histórico de créditos associados ao próprio cliente.
- Resultado observado: saldo de 36 pontos e registro correspondente no histórico.
- Situação: validado manualmente pelo Swagger.

## 13.4. Testes Automatizados com Pytest

Foi executado o comando:

```powershell
python -m pytest -v
```

O teste automatizado implementado verifica a criação e a existência das principais tabelas do banco de dados de testes, incluindo:

- usuários;
- produtos;
- pedidos;
- pagamentos;
- consentimentos;
- pontos de fidelidade.

### Resultado da execução

| Indicador | Resultado |
|---|---:|
| Testes coletados | 1 |
| Testes aprovados | 1 |
| Testes reprovados | 0 |
| Avisos | 1 |

O teste `test_banco_de_testes_criado` foi executado com sucesso.

Foi apresentado um aviso de descontinuação relacionado à integração entre Starlette e HTTPX no cliente de testes. Esse aviso não impediu a execução nem comprometeu o resultado do teste.

## 13.5. Evidências dos Testes

As evidências devem ser organizadas por funcionalidade, contendo capturas de tela do Swagger UI e do terminal de execução do Pytest.

Sugestão de evidências:

1. Autenticação e obtenção do token JWT.
2. Criação de pedido.
3. Aprovação de pagamento.
4. Registro de consentimento.
5. Consulta de saldo de fidelidade.
6. Consulta do histórico de pontos.
7. Execução do Pytest com resultado aprovado.

## 13.6. Considerações Finais

Os testes realizados permitiram verificar o funcionamento de fluxos importantes da aplicação, incluindo autenticação, criação de pedidos, processamento de pagamentos, registro de consentimentos e consulta do programa de fidelidade.

A execução automatizada confirmou a criação das principais tabelas do banco de dados de testes.

Embora os testes realizados tenham apresentado resultados satisfatórios, a ampliação da cobertura automatizada dos serviços e das rotas da API permanece como uma melhoria futura, assim como a validação sistemática de cenários negativos e de segurança.
### 3. Pedido com Estoque Insuficiente

**Cenário 3.1 — Tentativa de pedido sem saldo suficiente**
- Entrada: produto cuja quantidade solicitada supera o estoque disponível.
- Resultado esperado: operação rejeitada, sem criação indevida do pedido.
- Situação: regra de negócio validada manualmente.

### 4. Pagamento Aprovado

**Cenário 4.1 — Simulação de pagamento aprovado**
- Entrada: pedido válido e simulação de pagamento aprovada.
- Resultado esperado: pagamento registrado com status `APROVADO`, pedido encaminhado para `EM_PREPARO` e estoque atualizado.
- Resultado observado: pagamento aprovado com HTTP `201 Created`.
- Situação: validado manualmente pelo Swagger.

### 5. Pagamento Recusado

**Cenário 5.1 — Simulação de pagamento recusado**
- Entrada: pedido válido e simulação de pagamento recusada.
- Resultado esperado: pagamento registrado com status `RECUSADO`, sem baixa indevida do estoque e sem avanço do pedido para preparação.
- Situação: cenário previsto para validação funcional.

### 6. Consentimento e LGPD

**Cenário 6.1 — Registro de consentimento**
- Entrada: cliente autenticado informa a finalidade do consentimento.
- Resultado esperado: registro do consentimento associado ao usuário.
- Resultado observado: consentimento registrado com HTTP `201 Created`.
- Situação: validado manualmente pelo Swagger.

### 7. Programa de Fidelidade

**Cenário 7.1 — Crédito de pontos após pagamento aprovado**
- Entrada: cliente com adesão ativa ao programa realiza pedido e obtém pagamento aprovado.
- Resultado esperado: pontos calculados conforme a regra de negócio de 1 ponto por real pago, com descarte de frações.
- Resultado observado: pedido de R$ 36,90 gerou 36 pontos.
- Situação: validado manualmente pelo Swagger.

**Cenário 7.2 — Consulta de saldo e histórico**
- Entrada: cliente autenticado consulta seus pontos.
- Resultado esperado: retorno do saldo e do histórico de créditos associados ao próprio cliente.
- Resultado observado: saldo de 36 pontos e registro correspondente no histórico.
- Situação: validado manualmente pelo Swagger.

## 13.4. Testes Automatizados com Pytest

Foi executado o comando:

```powershell
python -m pytest -v
```

O teste automatizado implementado verifica a criação e a existência das principais tabelas do banco de dados de testes, incluindo:

- usuários;
- produtos;
- pedidos;
- pagamentos;
- consentimentos;
- pontos de fidelidade.

### Resultado da execução

| Indicador | Resultado |
|---|---:|
| Testes coletados | 1 |
| Testes aprovados | 1 |
| Testes reprovados | 0 |
| Avisos | 1 |

O teste `test_banco_de_testes_criado` foi executado com sucesso.

Foi apresentado um aviso de descontinuação relacionado à integração entre Starlette e HTTPX no cliente de testes. Esse aviso não impediu a execução nem comprometeu o resultado do teste.

## 13.5. Evidências dos Testes

As evidências devem ser organizadas por funcionalidade, contendo capturas de tela do Swagger UI e do terminal de execução do Pytest.

Sugestão de evidências:

1. Autenticação e obtenção do token JWT.
2. Criação de pedido.
3. Aprovação de pagamento.
4. Registro de consentimento.
5. Consulta de saldo de fidelidade.
6. Consulta do histórico de pontos.
7. Execução do Pytest com resultado aprovado.

## 13.6. Considerações Finais

Os testes realizados permitiram verificar o funcionamento de fluxos importantes da aplicação, incluindo autenticação, criação de pedidos, processamento de pagamentos, registro de consentimentos e consulta do programa de fidelidade.

A execução automatizada confirmou a criação das principais tabelas do banco de dados de testes.

Embora os testes realizados tenham apresentado resultados satisfatórios, a ampliação da cobertura automatizada dos serviços e das rotas da API permanece como uma melhoria futura, assim como a validação sistemática de cenários negativos e de segurança.