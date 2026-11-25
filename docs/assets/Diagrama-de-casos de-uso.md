@startuml
actor Cliente
actor Atendente
actor Cozinheiro
actor Gerente
actor "Sistema de Pagamento Externo" as Pagamento
actor Sistema

Cliente --> (Fazer Login)
Cliente --> (Visualizar Cardápio)
Cliente --> (Selecionar Produtos)
Cliente --> (Fazer Pedido)
Cliente --> (Efetuar Pagamento)
Cliente --> (Acompanhar Status do Pedido)
Cliente --> (Participar do Programa de Fidelização)

Atendente --> (Registrar Pedido no Balcão)
Atendente --> (Atualizar Status de Entrega)

Cozinheiro --> (Receber Pedido da Cozinha)
Cozinheiro --> (Atualizar Status Pedido -> Pronto)

Gerente --> (Gerenciar Produtos e Estoque)
Gerente --> (Ver Indicadores de Desempenho)
Gerente --> (Gerenciar Promoções/Campanhas)

Sistema --> (Validar Estoque)
Sistema --> (Processar Pedido)
Sistema --> (Integrar Pagamento)
Sistema --> (Aplicar Regras de Fidelização)

(Fazer Pedido) --> (Validar Estoque)
(Efetuar Pagamento) --> (Integrar Pagamento)
Integrar Pagamento --> Pagamento
@enduml
