from enum import Enum
from helpers.database import db

class StatusLimpeza(Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em andamento"
    FINALIZADO = "finalizado"

status = db.Column(db.Enum(StatusLimpeza), nullable=False, default=StatusLimpeza.PENDENTE)
