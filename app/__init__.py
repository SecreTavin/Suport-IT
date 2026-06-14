from flask import Flask
from app.repositories import database
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv

load_dotenv()

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-fallback-key-for-dev')
    
    csrf.init_app(app)
    
    @app.teardown_appcontext
    def close_db(e=None):
        database.close_db(e)
        
    # Registro das rotas (Blueprints)
    from app.controllers import chamado_controller
    app.register_blueprint(chamado_controller.bp)
    
    return app