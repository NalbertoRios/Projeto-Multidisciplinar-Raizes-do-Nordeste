# Projeto Multidisciplinar Backend - Rede Raízes do Nordeste

## Requisitos Não Funcionais (RNF)

* **RNF-01 (Segurança e Criptografia):** O sistema deve armazenar as senhas dos usuários utilizando algoritmos seguros de hash (como bcrypt ou Argon2), garantindo que senhas em texto plano nunca sejam salvas no banco de dados.
* **RNF-02 (Autenticação e Autorização):** O acesso aos endpoints protegidos da API deve ser realizado via tokens de autenticação baseados em padrão JWT (*JSON Web Tokens*), com controle de permissões por perfis/papéis (*roles*, ex: `CLIENTE`, `ATENDENTE`, `COZINHA`, `GERENTE`, `ADMINISTRADOR`).
* **RNF-03 (Privacidade e LGPD):** O sistema deve assegurar a privacidade dos dados pessoais e sensíveis dos usuários, coletando apenas informações estritamente necessárias, registrando o consentimento explícito e evitando a exposição indevida de dados nas respostas (*responses*) da API.
* **RNF-04 (Documentação de Contrato):** A API deve fornecer documentação interativa e automatizada utilizando o padrão OpenAPI (Swagger), refletindo fielmente os contratos de rotas, parâmetros, exemplos de *request/response* e códigos de status HTTP.
* **RNF-05 (Padronização de Erros):** Todas as falhas e exceções retornadas pela API devem seguir um formato JSON padronizado, contendo carimbo de data/hora (*timestamp*), código do erro, mensagem legível e o caminho da requisição.
* **RNF-06 (Confiabilidade, Disponibilidade e Desempenho):** O back-end deve ser projetado para operar com alta disponibilidade e tolerância a falhas nos momentos de pico de acesso, garantindo respostas rápidas nas consultas de cardápio e controle de estoque por unidade, além de suportar escalabilidade horizontal.
* **RNF-07 (Logs e Auditoria):** O sistema deve registrar logs estruturados e auditoria de ações sensíveis (como cancelamentos e alterações de status), garantindo rastreabilidade e conformidade.
* **RNF-08 (Usabilidade da API):** A API deve seguir padrões REST consistentes, garantindo previsibilidade, facilidade de integração e consumo por diferentes canais (APP, Totem, Web).
* **RNF-09 (Testabilidade e Manutenção):** O sistema deve permitir testes automatizados reprodutíveis e possuir documentação clara para manutenção futura.
