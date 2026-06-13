import sqlite3
from flask import g
import os

DATABASE = 'database/app.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    os.makedirs('database', exist_ok=True)
    
    db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    
    # Criar tabelas
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        db.executescript(f.read())
        
    # Verificar necessidade de seed
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM responsaveis')
    count = cursor.fetchone()[0]
    
    if count == 0:
        with open('database/seed.sql', 'r', encoding='utf-8') as f:
            db.executescript(f.read())
            
    db.commit()
    db.close()