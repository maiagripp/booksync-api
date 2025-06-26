# app.py

from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config  # O seu ficheiro de configuração
from database import db   # A instância do db que criámos

def create_app(config_class=Config):
    """
    Cria e configura a instância da aplicação Flask.
    Este é o padrão Application Factory.
    """
    info = Info(title="BookSync API", version="1.0.0")
    app = OpenAPI(__name__, info=info, doc_url="/docs")

    # Carrega a configuração a partir do objeto
    app.config.from_object(config_class)

    # Inicializa as extensões Flask com a aplicação
    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # --- Importa e registra os Blueprints DENTRO da factory ---
    # Isto evita importações circulares.
    from routes.auth_routes import auth_bp
    from routes.book_routes import book_bp
    
    app.register_api(auth_bp)
    app.register_api(book_bp)

    # Cria as tabelas da base de dados se não existirem
    with app.app_context():
        db.create_all()

    return app

# --- Bloco de Execução ---
# Este bloco só é executado quando você corre `python app.py`
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

