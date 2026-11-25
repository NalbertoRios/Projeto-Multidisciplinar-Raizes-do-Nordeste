# Especificação de Casos de Uso

## UC-01: Realizar Pedido e Processar Venda

* **Descrição:** Permite que o Cliente (via canais digitais) ou o Atendente (via balcão) registrem um novo pedido na rede, validando o estoque e processando o pagamento.
* **Atores:** Cliente, Atendente, Sistema, Cozinheiro.
* **Pré-condições:** 
  * O usuário deve estar autenticado no sistema (possuir token JWT válido).
  * O produto deve estar cadastrado e ativo no cardápio da respectiva unidade.
  * O cliente deve ter consentimento registrado para uso de dados pessoais (LGPD).

### Fluxo Principal (Cenário de Sucesso):
1. O Cliente (via App/Web/Totem) ou o Atendente (via balcão) realiza o login no sistema.
2. O usuário acessa o cardápio da unidade e seleciona os produtos e quantidades desejadas.
3. O sistema solicita a confirmação do pedido informando o canal de origem (`canalPedido`).
4. O Sistema verifica a disponibilidade no estoque da unidade:
   * *Se houver saldo:* O sistema prossegue para a etapa de pagamento.
5. O cliente efetua o pagamento (integrado via serviço de *mock* externo) e o sistema aguarda a confirmação de aprovação.
6. O pagamento sendo aprovado, o pedido é gerado com status inicial (`EM_PREPARO`), com registro de data/hora e ID único, e os Cozinheiros/Atendentes são notificados.
7. A cozinha atualiza o status do pedido para `PRONTO` quando finalizado.
8. O cliente recebe o pedido e o funcionário altera o status final para `FINALIZADO`.

### Fluxos Alternativos / Exceções:
* **4a. Estoque Insuficiente:** 
  * Se o sistema verificar que não há saldo suficiente de estoque para um ou mais itens, a operação é interrompida, uma mensagem de erro é retornada ao usuário (`400 Bad Request`) e o pedido não é criado.
* **5a. Pagamento Recusado:** 
  * Se o serviço de pagamento externo retornar recusa, o sistema notifica o usuário e mantém o pedido com status de aguardando regularização ou cancelamento.
* **1a. Token JWT inválido/expirado:** 
  * O sistema retorna erro de autenticação (`401 Unauthorized`) e não permite prosseguir.
* **5b. Falha de integração com serviço externo:** 
  * Se o mock de pagamento não responder dentro do tempo limite, o sistema retorna mensagem amigável e não trava o banco de dados.
