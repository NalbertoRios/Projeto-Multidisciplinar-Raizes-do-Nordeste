@startuml
actor Cliente
actor Atendente
participant "Sistema Backend" as Sistema
participant "Gateway de Pagamento" as Pagamento
actor Cozinheiro

Cliente -> Sistema: Fazer Login
Sistema --> Cliente: Token JWT válido

Cliente -> Sistema: Criar Pedido (itens, canalPedido)
Sistema -> Sistema: Validar Estoque
Sistema --> Cliente: Pedido criado (status = AGUARDANDO_PAGAMENTO)

Cliente -> Sistema: Efetuar Pagamento
Sistema -> Pagamento: Solicitar pagamento (mock)
Pagamento --> Sistema: Retorno (APROVADO ou RECUSADO)

alt Pagamento Aprovado
  Sistema -> Sistema: Atualizar status Pedido = EM_PREPARO
  Sistema --> Cozinheiro: Notificação de novo pedido
  Cozinheiro -> Sistema: Atualizar status Pedido = PRONTO
  Sistema --> Cliente: Pedido pronto para retirada/entrega
else Pagamento Recusado
  Sistema --> Cliente: Notificação de pagamento recusado
  Sistema -> Sistema: Pedido permanece em AGUARDANDO_PAGAMENTO ou CANCELADO
end
@enduml