# Projeto Multidisciplinar Backend - Rede Raízes do Nordeste

## Análise de Riscos e Decisões Técnicas

* **Risco 1 (Indisponibilidade do Gateway de Pagamento Externo):**
  * *Impacto:* Clientes não conseguem concluir pedidos, afetando faturamento e experiência.
  * *Mitigação:* Implementação de tratamento de exceções robusto e tempo limite (*timeout*) configurado na requisição *mock*, retornando mensagem amigável ao cliente sem travar o banco de dados.

* **Risco 2 (Inconsistência de Estoque em Horários de Pico):**
  * *Impacto:* Vendas de produtos indisponíveis, gerando insatisfação e falhas operacionais.
  * *Mitigação:* Uso de transações atômicas no banco de dados via ORM (SQLAlchemy) para garantir que a baixa de estoque ocorra de forma síncrona e segura apenas após a validação.

* **Risco 3 (Segurança e LGPD):**
  * *Impacto:* Vazamento de dados pessoais e descumprimento da legislação.
  * *Mitigação:* Hash seguro de senhas, autenticação JWT, logs de auditoria e anonimização de dados conforme prazo legal.

## Decisões Tecnológicas
* Escolha do **FastAPI** e **SQLAlchemy** em conjunto com **SQLite** para agilizar o desenvolvimento do back-end, mantendo alta performance, tipagem rigorosa via Pydantic e geração automática de documentação via Swagger.
* O **SQLite** foi adotado por simplicidade e portabilidade no MVP, mas poderá ser substituído futuramente por **PostgreSQL** ou **MySQL** para suportar escalabilidade e ambientes de produção.
