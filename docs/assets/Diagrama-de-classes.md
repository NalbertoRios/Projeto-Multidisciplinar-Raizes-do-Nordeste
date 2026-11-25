@startuml
class Usuario {
  - id : int
  - nome : string
  - email : string
  - senha_hash : string
  - perfil : enum {CLIENTE, ATENDENTE, COZINHA, GERENTE, MATRIZ}
}

class Unidade {
  - id : int
  - nome : string
  - cidade : string
  - regiao : string
}

class Produto {
  - id : int
  - nome : string
  - descricao : text
  - preco : decimal
  - ativo : boolean
}

class Estoque {
  - id : int
  - quantidade_disponivel : int
}

class Pedido {
  - id : int
  - canal_pedido : enum {APP, TOTEM, BALCAO, PICKUP, WEB}
  - status : enum {AGUARDANDO_PAGAMENTO, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO}
  - valor_total : decimal
  - data_criacao : timestamp
}

class ItemPedido {
  - id : int
  - quantidade : int
  - preco_unitario : decimal
}

class Pagamento {
  - id : int
  - status_pagamento : enum {APROVADO, RECUSADO, PENDENTE}
  - data_pagamento : timestamp
  - valor : decimal
}

Usuario "1" --> "N" Pedido : cliente_id
Unidade "1" --> "N" Produto : unidade_id
Produto "1" --> "1" Estoque : produto_id
Pedido "1" --> "N" ItemPedido : pedido_id
Produto "1" --> "N" ItemPedido : produto_id
Pedido "1" --> "1" Pagamento : pedido_id
@enduml