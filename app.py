from flask import Flask, jsonify, flash, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import re

# Importar modelos
from models import db, Organizador, Evento, Categoria, EventoCategoria, Asistente

# Cargar variables de entorno
load_dotenv()

# Configuración de Flask (especificar el directorio de plantillas)
app = Flask(__name__, template_folder="eventos/templates")

# Configurar base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///fallback.db')  # Base de datos predeterminada (SQLite) si no se configura DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Inicializar la base de datos con la app
db.init_app(app)
migrate = Migrate(app, db)


# Rutas
@app.route("/")
def home():
    # Consultar los eventos de la base de datos
    eventos = Evento.query.order_by(Evento.fecha_creacion.desc()).all()
    return render_template("index.html", eventos=eventos, user_name=session.get('user_name'))


if __name__ == "__main__":
    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()
    app.run(debug=True)
