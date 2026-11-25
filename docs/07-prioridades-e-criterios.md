# Projeto Multidisciplinar Backend - Rede Raízes do Nordeste

## Prioridades e Critérios do MVP

Para garantir a entrega ponta a ponta dentro do prazo acadêmico, o escopo foi dividido em prioridades:

### MVP Essencial (Alta Prioridade - Implementado)
- **Autenticação via JWT com controle de perfis (roles):** Usuário deve conseguir autenticar e acessar apenas recursos permitidos conforme seu perfil.
- **Gestão de unidades e cardápios vinculados:** API deve permitir cadastrar unidades e vincular cardápios específicos a cada uma.
- **Criação de pedidos com validação de estoque e registro do `canalPedido`:** Pedido só deve ser confirmado se houver saldo suficiente na unidade e deve registrar o canal de origem.
- **Integração com o serviço de pagamento simulado (mock):** API deve enviar solicitação ao mock e registrar status de retorno (`APROVADO` ou `RECUSADO`).
- **Documentação interativa via Swagger/OpenAPI:** Swagger deve refletir fielmente os endpoints implementados, com exemplos de request/response.
- **Relatórios básicos e logs de auditoria:** Sistema deve gerar relatórios de vendas por unidade e registrar logs de operações sensíveis (cancelamentos, alterações de status).

### Evoluções Futuras (Baixa Prioridade - Proposto)
- **Notificações em tempo real via WebSockets para a cozinha.**
- **Painéis avançados de Business Intelligence (BI) para a matriz.**
- **Deploy em nuvem e escalabilidade horizontal.**
- **Testes automatizados avançados (cobertura de carga e segurança).**
