from typing import List, Optional
from app.models.domain import Responsavel
from app.repositories.database import get_db

def listar_todos() -> List[Responsavel]:
    db = get_db()
    cursor = db.execute('SELECT id, nome FROM responsaveis ORDER BY nome')
    rows = cursor.fetchall()
    return [Responsavel(id=row['id'], nome=row['nome']) for row in rows]

def obter_por_id(responsavel_id: int) -> Optional[Responsavel]:
    db = get_db()
    cursor = db.execute('SELECT id, nome FROM responsaveis WHERE id = ?', (responsavel_id,))
    row = cursor.fetchone()
    if row:
        return Responsavel(id=row['id'], nome=row['nome'])
    return None