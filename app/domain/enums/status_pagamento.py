from enum import Enum


class StatusPagamento(str, Enum):

    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"
    