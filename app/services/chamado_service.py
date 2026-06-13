from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

from app.models.domain import Chamado, Prioridade, Status
from app.repositories import chamado_repo, responsavel_repo

@dataclass
class ChamadoCreateDTO:
    titulo: str
    descricao: str
    prioridade: Prioridade
    atribuicao_automatica: bool
    responsavel_id: Optional[int] = None

@dataclass
class ChamadoUpdateDTO:
    chamado_id: int
    prioridade: Prioridade
    status: Status
    titulo: str
    descricao: str

def determinar_responsavel_automatico() -> int:
    # Obtém a contagem de chamados pendentes por responsável (RN01)
    contagem = chamado_repo.contar_chamados_pendentes_por_responsavel()
    
    if not contagem:
        responsaveis = responsavel_repo.listar_todos()
        if not responsaveis:
            raise ValueError("Nenhum responsável cadastrado no sistema.")
        return responsaveis[0].id

    # Busca o ID com o menor número de chamados pendentes
    id_escolhido = min(contagem, key=contagem.get)
    return id_escolhido

def criar_chamado(dados: ChamadoCreateDTO) -> Chamado:
    resp_id = dados.responsavel_id
    if dados.atribuicao_automatica or not resp_id:
        resp_id = determinar_responsavel_automatico()
        
    novo_chamado = Chamado(
        id=0, # Auto-incrementado pelo BD
        titulo=dados.titulo,
        descricao=dados.descricao,
        prioridade=dados.prioridade,
        status=Status.ABERTO,
        responsavel_id=resp_id,
        data_abertura=datetime.now()
    )
    
    novo_id = chamado_repo.criar(novo_chamado)
    novo_chamado.id = novo_id
    return novo_chamado

def atualizar_chamado(dados: ChamadoUpdateDTO) -> Chamado:
    chamado_existente = chamado_repo.obter_por_id(dados.chamado_id)
    if not chamado_existente:
        raise ValueError(f"Chamado com ID {dados.chamado_id} não encontrado.")
        
    chamado_existente.titulo = dados.titulo
    chamado_existente.descricao = dados.descricao
    chamado_existente.prioridade = dados.prioridade
    chamado_existente.status = dados.status
    
    chamado_repo.atualizar(chamado_existente)
    return chamado_existente

def listar_chamados(status: Optional[str] = None, prioridade: Optional[str] = None) -> List[Chamado]:
    return chamado_repo.listar_todos(filtro_status=status, filtro_prioridade=prioridade)

def obter_chamado(chamado_id: int) -> Chamado:
    chamado = chamado_repo.obter_por_id(chamado_id)
    if not chamado:
        raise ValueError("Chamado não encontrado.")
    return chamado