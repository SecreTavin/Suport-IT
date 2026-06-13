import sys
from app import create_app
from app.repositories.database import init_db

app = create_app()

if __name__ == '__main__':
    # Initialize DB automatically if it doesn't exist
    import os
    if not os.path.exists('database/app.db'):
        with app.app_context():
            init_db()
            print("Banco de dados criado e populado automaticamente.")
            
    app.run(debug=True)