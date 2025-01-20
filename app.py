from flask import Flask, jsonify, flash, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import re

# Cargar las variables de entorno desde .env
load_dotenv()

# Configuración de Flask
app = Flask(__name__)

# Leer la URL de la base de datos desde el archivo .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///fallback.db')  # Usa SQLite como base de datos predeterminada si no se configura DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Leer la clave secreta desde el archivo .env
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Inicializar la base de datos
db = SQLAlchemy(app)

class Organizador(db.Model):
    __tablename__ = "organizadores"
    id_organizador = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, server_default=db.func.now())


class Evento(db.Model):
    __tablename__ = 'eventos'
    id_evento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    lugar = db.Column(db.String(255), nullable=False)
    presupuesto = db.Column(db.Numeric, nullable=False)
    id_organizador = db.Column(db.Integer, db.ForeignKey('organizadores.id_organizador'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())

    categorias = db.relationship(
        'Categoria',
        secondary='evento_categoria',
        backref=db.backref('eventos', lazy='dynamic')
    )


class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)


class EventoCategoria(db.Model):
    __tablename__ = 'evento_categoria'
    id_evento = db.Column(db.Integer, db.ForeignKey('eventos.id_evento'), primary_key=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), primary_key=True)


class Asistente(db.Model):
    __tablename__ = "asistentes"
    id_asistente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)


@app.route("/")
def home():
    return "¡Conexión configurada correctamente!"


if __name__ == "__main__":
    app.run(debug=True)
