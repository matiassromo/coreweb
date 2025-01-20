from flask import Blueprint, render_template, request, redirect, session, flash, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Organizador, Evento, Categoria, EventoCategoria
import re

# Crear un Blueprint para las rutas
controllers_bp = Blueprint('controllers', __name__)

# --- Rutas de autenticación ---
@controllers_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        # Validar el formato del correo
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template('registro.html', error="Correo no válido.")

        # Validar la fuerza de la contraseña
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&\-])[A-Za-z\d@$!%*?&\-]{8,}$', password):
            return render_template(
                'registro.html',
                error="La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula, un número y un símbolo."
            )

        # Verificar si el correo ya está registrado
        if Organizador.query.filter_by(email=email).first():
            return render_template('registro.html', error="El correo ya está registrado.")

        # Encriptar la contraseña y guardar el organizador
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        nuevo_organizador = Organizador(nombre=nombre, email=email, password=hashed_password)
        db.session.add(nuevo_organizador)
        db.session.commit()

        return render_template('login.html', success="Registro exitoso. Ahora puedes iniciar sesión.")

    return render_template('registro.html')


@controllers_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verificar las credenciales del usuario
        user = Organizador.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Guardar información del usuario en la sesión
            session['user_id'] = user.id_organizador
            session['user_name'] = user.nombre
            session['user_email'] = user.email
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('controllers.home'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')

    return render_template('login.html')


@controllers_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('controllers.login'))


# --- Rutas de gestión de eventos ---
@controllers_bp.route('/')
def home():
    eventos = Evento.query.order_by(Evento.fecha_creacion.desc()).all()
    return render_template("index.html", eventos=eventos, user_name=session.get('user_name'))


@controllers_bp.route('/crear_evento', methods=['GET', 'POST'])
def crear_evento():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para crear un evento.', 'danger')
        return redirect(url_for('controllers.login'))

    categorias = Categoria.query.all()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        lugar = request.form.get('lugar')
        presupuesto = request.form.get('presupuesto')
        id_categoria = request.form.get('categoria')

        if not id_categoria:
            flash('Debes seleccionar una categoría.', 'danger')
            return render_template('crear_evento.html', categorias=categorias)

        try:
            nuevo_evento = Evento(
                nombre=nombre,
                descripcion=descripcion,
                fecha=fecha,
                hora=hora,
                lugar=lugar,
                presupuesto=presupuesto,
                id_organizador=session['user_id']
            )
            db.session.add(nuevo_evento)
            db.session.commit()

            evento_categoria = EventoCategoria(
                id_evento=nuevo_evento.id_evento,
                id_categoria=id_categoria
            )
            db.session.add(evento_categoria)
            db.session.commit()

            flash('Evento creado exitosamente.', 'success')
            return redirect(url_for('controllers.home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el evento: {e}', 'danger')

    return render_template('crear_evento.html', categorias=categorias)

# --- API para obtener eventos ---
@controllers_bp.route('/api/eventos')
def get_eventos():
    eventos = Evento.query.order_by(Evento.fecha_creacion.desc()).limit(6).all()
    eventos_json = [
        {
            "id_evento": evento.id_evento,
            "nombre": evento.nombre,
            "descripcion": evento.descripcion,
            "fecha": evento.fecha.strftime("%Y-%m-%d"),
            "hora": evento.hora.strftime("%H:%M:%S") if evento.hora else None,
            "lugar": evento.lugar,
            "presupuesto": float(evento.presupuesto)
        }
        for evento in eventos
    ]
    return jsonify(eventos_json)

@controllers_bp.route('/api/asistir', methods=['POST'])
def asistir():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Debes iniciar sesión para registrarte como asistente.'}), 401

        data = request.get_json()
        if not data:
            return jsonify({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}), 400

        id_evento = data.get('id_evento')
        if not id_evento:
            return jsonify({'error': 'El campo id_evento es requerido'}), 400

        # Obtener el nombre y el correo desde la sesión
        nombre = session.get('user_name')
        email = session.get('user_email')

        if not email:
            return jsonify({'error': 'El correo electrónico no está disponible en la sesión.'}), 400

        # Verificar si el asistente ya está registrado
        asistente = db.session.execute(
            db.text("SELECT id_asistente FROM asistentes WHERE email = :email"),
            {"email": email}
        ).fetchone()

        if not asistente:
            # Crear un nuevo asistente
            db.session.execute(
                db.text("INSERT INTO asistentes (nombre, email) VALUES (:nombre, :email)"),
                {"nombre": nombre, "email": email}
            )
            db.session.commit()

        return jsonify({'message': f'¡Registro exitoso como asistente en el evento {id_evento}!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

