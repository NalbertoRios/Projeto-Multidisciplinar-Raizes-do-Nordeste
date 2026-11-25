# Projeto Multidisciplinar Backend - Rede Raízes do Nordeste

## 1. Visão Geral e Problema
A franquia fictícia "Rede Raízes do Nordeste" necessita de um sistema centralizado de backend para gerenciar de forma integrada seus pedidos vindos de múltiplos canais de atendimento (APP, TOTEM, BALCÃO, PICKUP e WEB), controlando o estoque por unidade, o fluxo de pedidos e o processamento de pagamentos simulados.  
Sem essa solução, a rede corre risco de inconsistência entre unidades, falhas em horários de pico e perda de confiabilidade junto aos clientes.

## 2. Objetivo do MVP (Minimum Viable Product)
Desenvolver uma API RESTful robusta e funcional utilizando Python e FastAPI, capaz de:
- Autenticar usuários e controlar permissões por perfil.
- Cadastrar e gerenciar produtos e unidades de atendimento.
- Processar a criação de pedidos validando o estoque disponível por unidade.
- Integrar um sistema simulado de pagamento para aprovar ou recusar transações.
- Garantir conformidade inicial com a LGPD e testes automatizados com Pytest.

## 3. Escopo do Projeto
### O que será implementado no MVP:
- Arquitetura em camadas (API, Domínio, Infraestrutura).
- Persistência de dados utilizando SQLAlchemy e SQLite.
- Documentação automática via OpenAPI (Swagger).
- Testes automatizados cobrindo os principais fluxos positivos e negativos.

### O que não será implementado neste MVP:
- Integração real com gateways de pagamento (apenas mock).
- Relatórios avançados da matriz (apenas estrutura inicial).
- Interface gráfica ou protótipos (não fazem parte da trilha Back-end).
