# Projeto Multidisciplinar Backend - Rede Raízes do Nordeste

## Requisitos Funcionais (RF)

### Canal do Cliente / Multicanalidade
* **RF-01:** O sistema deve permitir a criação de pedidos informando obrigatoriamente o canal de origem (`canalPedido`: `APP`, `TOTEM`, `BALCAO`, `PICKUP`, `WEB`).
* **RF-02:** O sistema deve permitir consultar o cardápio filtrando pelos produtos disponíveis na unidade selecionada da franquia.
* **RF-03:** O sistema deve permitir que o cliente selecione os produtos e quantidades desejadas para compor o pedido.
* **RF-04:** O sistema deve processar a solicitação de pagamento por meio de um serviço externo simulado (*mock*), registrando o retorno de aprovação ou recusa, incluindo payload da transação.
* **RF-05:** O sistema deve gerenciar o programa de fidelização de clientes com controle de pontos, histórico de consumo e registro de consentimento explícito para o tratamento de dados (LGPD).

## Operação Interna (Atendente e Cozinha)
* **RF-06:** O sistema deve permitir que o atendente registre novos pedidos manualmente ou finalize pedidos originados pelos canais de autoatendimento.
* **RF-07:** O sistema deve validar a disponibilidade de estoque por unidade antes de confirmar a criação de qualquer pedido.
* **RF-08:** O sistema deve permitir a atualização do status do pedido no fluxo operacional (`AGUARDANDO_PAGAMENTO`, `EM_PREPARO`, `PRONTO`, `ENTREGUE`, `CANCELADO`).

### Gestão e Relatórios (Gerência e Matriz)
* **RF-09:** O sistema deve disponibilizar relatórios consolidados de vendas por unidade e por região, com filtros por período.
* **RF-10:** O sistema deve registrar logs de auditoria para operações sensíveis (como cancelamentos e alterações de status), garantindo rastreabilidade.
* **RF-11:** O sistema deve fornecer indicadores de desempenho e o ranking dos produtos mais consumidos na rede.
* **RF-12:** O sistema deve permitir cadastro e autenticação de usuários, com controle de acesso por perfis/roles (ADMIN, GERENTE, CLIENTE).
* **RF-13:** O sistema deve permitir o registro de promoções/campanhas vinculadas a produtos ou unidades, aplicando regras de desconto conforme definido pela matriz.
