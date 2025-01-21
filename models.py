from flask_sqlalchemy import SQLAlchemy

# Inicializar SQLAlchemy
db = SQLAlchemy()

# Modelos
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

    # Relación muchos a muchos con Categorias
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


class Gasto(db.Model):
    __tablename__ = 'gastos'
    id_gasto = db.Column(db.Integer, primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('eventos.id_evento'), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Numeric, nullable=False)
