# Regras de Negócio (RN)

* **RN-01 (Validação de Estoque por Unidade):** Nenhum pedido pode ser confirmado caso a quantidade solicitada de um produto exceda o saldo de estoque disponível na respectiva unidade selecionada.
* **RN-02 (Obrigatoriedade do Canal):** Todo pedido gerado no sistema deve obrigatoriamente registrar o seu canal de origem (`canalPedido`: `APP`, `TOTEM`, `BALCAO`, `PICKUP`, `WEB`) para fins de rastreabilidade e consolidação de relatórios pela matriz.
* **RN-03 (Desacoplamento de Pagamento):** O processamento de pagamentos ocorre de forma externa (*mock*). O back-end não armazena dados sensíveis de cartão de crédito; ele apenas envia a solicitação de cobrança e registra o status de retorno (`APROVADO` ou `RECUSADO`).
* **RN-04 (Ciclo de Vida do Pedido):** Um pedido deve transicionar de forma controlada por seu fluxo operacional: `AGUARDANDO_PAGAMENTO` -> `EM_PREPARO` -> `PRONTO` -> `ENTREGUE`. Cancelamentos só podem ocorrer antes do status `PRONTO` e devem ser autorizados por gerente ou administrador.
* **RN-05 (Promoções e Fidelização):** Pontos de fidelidade e descontos promocionais só podem ser aplicados mediante consentimento do cliente e regras definidas pela matriz.
* **RN-06 (Controle de Perfis):** Apenas usuários com perfil `GERENTE` ou `ADMINISTRADOR` podem autorizar cancelamentos de pedidos e aplicar promoções.
* **RN-07 (Auditoria):** Toda operação sensível (cancelamento, alteração de status, aplicação de desconto) deve gerar registro em log com usuário responsável, data/hora e motivo.
