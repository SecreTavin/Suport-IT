import sys
from app import create_app
from app.repositories.database import init_db

app = create_app()

import os
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis do .env

app = create_app()

if __name__ == '__main__':
    # Initialize DB automatically if it doesn't exist
    if not os.path.exists('database/app.db'):
        with app.app_context():
            init_db()
            print("Banco de dados criado e populado automaticamente.")
            
    # O modo debug é controlado pela variável de ambiente FLASK_DEBUG
    is_debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=is_debug)