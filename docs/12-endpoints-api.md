
# 12. Endpoints da API

## 12.1. Visão geral

A API da Rede Raízes do Nordeste foi desenvolvida utilizando FastAPI e segue o padrão REST.

A autenticação é realizada por meio de JWT (JSON Web Token). As rotas protegidas exigem o envio do token no cabeçalho HTTP:

```http
Authorization: Bearer SEU_TOKEN
```

A documentação interativa pode ser acessada pelo Swagger:

```text
http://127.0.0.1:8000/docs
```

## 12.2. Verificação da API

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verifica se a API está funcionando. |

## 12.3. Autenticação

Prefixo: `/auth`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/auth/cadastro` | Cadastra um novo usuário. |
| POST | `/auth/login` | Realiza a autenticação e retorna o token JWT. |
| GET | `/auth/me` | Retorna os dados do usuário autenticado. |

## 12.4. Produtos

Prefixo: `/produtos`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/produtos/` | Cadastra um produto. |
| GET | `/produtos/` | Lista os produtos. |
| GET | `/produtos/{produto_id}` | Consulta um produto pelo identificador. |
| PATCH | `/produtos/{produto_id}` | Atualiza os dados de um produto. |
| DELETE | `/produtos/{produto_id}` | Desativa um produto logicamente. |

As operações de cadastro, atualização e desativação são restritas aos perfis GERENTE e MATRIZ.

## 12.5. Unidades

Prefixo: `/unidades`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/unidades/` | Cadastra uma unidade. |
| GET | `/unidades/` | Lista as unidades. |
| GET | `/unidades/{unidade_id}` | Consulta uma unidade pelo identificador. |
| PATCH | `/unidades/{unidade_id}` | Atualiza os dados de uma unidade. |
| DELETE | `/unidades/{unidade_id}` | Desativa uma unidade logicamente. |

As operações de cadastro, atualização e desativação são restritas aos perfis GERENTE e MATRIZ.

## 12.6. Produtos por unidade

Prefixo: `/produto-unidades`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/produto-unidades/` | Associa um produto a uma unidade. |
| GET | `/produto-unidades/` | Lista as associações entre produtos e unidades. |
| GET | `/produto-unidades/{produto_unidade_id}` | Consulta uma associação específica. |
| PATCH | `/produto-unidades/{produto_unidade_id}` | Atualiza os dados da associação. |
| DELETE | `/produto-unidades/{produto_unidade_id}` | Desabilita a associação logicamente. |

Essa funcionalidade permite que um mesmo produto tenha condições específicas em diferentes unidades, incluindo preço e disponibilidade.

O cadastro de uma associação também cria seu registro de estoque inicial, com quantidade zero.

## 12.7. Estoques

Prefixo: `/estoques`

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/estoques/` | Lista os registros de estoque. |
| GET | `/estoques/{estoque_id}` | Consulta um registro de estoque. |
| PATCH | `/estoques/{estoque_id}` | Atualiza a quantidade disponível. |

A consulta de estoque é permitida aos perfis ATENDENTE, COZINHA, GERENTE e MATRIZ.

A atualização é restrita aos perfis GERENTE e MATRIZ.

## 12.8. Pedidos

Prefixo: `/pedidos`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/pedidos/` | Cria um novo pedido. |

O cliente é identificado por meio do token JWT, evitando que outro usuário informe livremente a identificação de um cliente no corpo da requisição.

O pedido pode ser realizado pelos canais previstos no sistema, como APP, TOTEM, BALCAO, PICKUP e WEB.

## 12.9. Pagamentos

Prefixo: `/pagamentos`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/pagamentos/{pedido_id}/simular` | Simula o processamento do pagamento de um pedido. |

A simulação permite testar situações de aprovação e recusa de pagamento, sem integração com uma instituição financeira real.

A operação é permitida aos perfis CLIENTE e ATENDENTE, respeitando as regras de acesso ao pedido.

## 12.10. Consentimentos e LGPD

Prefixo: `/consentimentos`

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/consentimentos/` | Registra um consentimento. |
| GET | `/consentimentos/meus` | Lista os consentimentos do usuário autenticado. |
| PATCH | `/consentimentos/{consentimento_id}/revogar` | Revoga um consentimento. |

As operações consideram o usuário autenticado, permitindo registrar e consultar seus próprios consentimentos e solicitar a revogação.

## 12.11. Programa de fidelidade

Prefixo: `/fidelidade`

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/fidelidade/meus-pontos` | Consulta a pontuação do cliente autenticado. |
| GET | `/fidelidade/meu-historico` | Consulta o histórico de movimentações de pontos. |

Essas operações são destinadas ao perfil CLIENTE.

## 12.12. Códigos HTTP utilizados

| Código | Significado | Aplicação |
|---|---|---|
| 200 | OK | Operação realizada com sucesso. |
| 201 | Created | Cadastro ou criação realizada com sucesso. |
| 400 | Bad Request | Solicitação inválida ou regra de negócio não atendida. |
| 401 | Unauthorized | Falha de autenticação ou token inválido. |
| 403 | Forbidden | Usuário sem permissão para realizar a operação. |
| 404 | Not Found | Recurso não encontrado. |
| 409 | Conflict | Conflito com o estado atual do recurso. |
| 422 | Unprocessable Entity | Dados enviados não atendem à validação. |
| 500 | Internal Server Error | Erro interno durante o processamento. |

**Observação:** os endpoints e permissões apresentados correspondem às rotas implementadas no projeto. Os códigos HTTP indicam situações previstas na aplicação e não significam que todos sejam retornados por todas as operações.
