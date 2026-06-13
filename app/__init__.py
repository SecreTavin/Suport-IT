from flask import Flask
from app.repositories import database

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-123'
    
    @app.teardown_appcontext
    def close_db(e=None):
        database.close_db(e)
        
    # Registro das rotas (Blueprints)
    from app.controllers import chamado_controller
    app.register_blueprint(chamado_controller.bp)
    
    return app