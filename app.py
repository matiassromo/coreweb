from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Importar modelos y Blueprints
from models import db
from controllers import controllers_bp

# Cargar variables de entorno
load_dotenv()

# Configuración de Flask (especificar el directorio de plantillas)
app = Flask(__name__, template_folder="eventos/templates", static_folder="eventos/static")

# Configurar base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///fallback.db')  # Base de datos predeterminada (SQLite) si no se configura DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Inicializar la base de datos y migración
db.init_app(app)
migrate = Migrate(app, db)

# Registrar el Blueprint
app.register_blueprint(controllers_bp)

if __name__ == "__main__":
    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(debug=True)
