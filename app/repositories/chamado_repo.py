from typing import List, Optional, Tuple
from datetime import datetime
from app.models.domain import Chamado, Prioridade, Status
from app.repositories.database import get_db

def _row_to_chamado(row) -> Chamado:
    data_ab = row['data_abertura']
    if isinstance(data_ab, str):
        try:
            # Tenta o formato com timezone primeiro (padrão do Python)
            data_ab = datetime.fromisoformat(data_ab)
        except ValueError:
            # Fallback para o formato do SQLite sem timezone
            data_ab = datetime.strptime(data_ab, "%Y-%m-%d %H:%M:%S")

    return Chamado(
        id=row['id'],
        titulo=row['titulo'],
        descricao=row['descricao'],
        prioridade=Prioridade(row['prioridade']),
        status=Status(row['status']),
        responsavel_id=row['responsavel_id'],
        data_abertura=data_ab
    )

def listar_paginado(
    page: int, 
    per_page: int, 
    filtro_status: Optional[str] = None, 
    filtro_prioridade: Optional[str] = None
) -> Tuple[List[Chamado], int]:
    db = get_db()
    
    # Contagem total de itens com o filtro
    count_query = 'SELECT COUNT(id) as total FROM chamados WHERE 1=1'
    params = []
    
    if filtro_status:
        count_query += ' AND status = ?'
        params.append(filtro_status)
    if filtro_prioridade:
        count_query += ' AND prioridade = ?'
        params.append(filtro_prioridade)
        
    total_items = db.execute(count_query, params).fetchone()['total']

    # Busca dos itens para a página atual
    query = 'SELECT * FROM chamados WHERE 1=1'
    if filtro_status:
        query += ' AND status = ?'
    if filtro_prioridade:
        query += ' AND prioridade = ?'
        
    query += ' ORDER BY data_abertura DESC LIMIT ? OFFSET ?'
    
    offset = (page - 1) * per_page
    params.extend([per_page, offset])
    
    cursor = db.execute(query, params)
    chamados = [_row_to_chamado(row) for row in cursor.fetchall()]
    
    return chamados, total_items

def obter_por_id(chamado_id: int) -> Optional[Chamado]:
    db = get_db()
    cursor = db.execute('SELECT * FROM chamados WHERE id = ?', (chamado_id,))
    row = cursor.fetchone()
    if row:
        return _row_to_chamado(row)
    return None

def criar(chamado: Chamado) -> int:
    db = get_db()
    cursor = db.execute(
        '''INSERT INTO chamados (titulo, descricao, prioridade, status, responsavel_id)
           VALUES (?, ?, ?, ?, ?)''',
        (chamado.titulo, chamado.descricao, chamado.prioridade.value, chamado.status.value, chamado.responsavel_id)
    )
    db.commit()
    return cursor.lastrowid

def atualizar(chamado: Chamado) -> None:
    db = get_db()
    db.execute(
        '''UPDATE chamados SET titulo = ?, descricao = ?, prioridade = ?, status = ?
           WHERE id = ?''',
        (chamado.titulo, chamado.descricao, chamado.prioridade.value, chamado.status.value, chamado.id)
    )
    db.commit()

def contar_chamados_pendentes_por_responsavel() -> dict[int, int]:
    db = get_db()
    cursor = db.execute(
        '''SELECT r.id, COUNT(c.id) as pendentes
           FROM responsaveis r
           LEFT JOIN chamados c ON r.id = c.responsavel_id AND c.status IN (?, ?)
           GROUP BY r.id''',
        (Status.ABERTO.value, Status.EM_ANDAMENTO.value)
    )
    return {row['id']: row['pendentes'] for row in cursor.fetchall()}