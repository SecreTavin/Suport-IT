from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class Prioridade(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"

class Status(str, Enum):
    ABERTO = "Aberto"
    EM_ANDAMENTO = "Em Andamento"
    RESOLVIDO = "Resolvido"
    FECHADO = "Fechado"

@dataclass
class Responsavel:
    id: int
    nome: str

@dataclass
class Chamado:
    id: int
    titulo: str
    descricao: str
    prioridade: Prioridade
    status: Status
    responsavel_id: int
    data_abertura: datetime