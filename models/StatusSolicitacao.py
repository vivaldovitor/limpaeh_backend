from enum import Enum


class StatusSolicitacao(Enum):
    PENDENTE = "pendente"
    EM_ANALISE = "em análise"
    ENVIADO_SUPERVISOR = "enviado ao supervisor"
    FINALIZADO = "finalizado"