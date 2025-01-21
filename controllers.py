from flask import Blueprint, render_template, request, redirect, session, flash, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Organizador, Evento, Categoria, EventoCategoria, Asistente
import re

# Crear un Blueprint para las rutas
controllers_bp = Blueprint('controllers', __name__)

# --- Rutas de autenticación ---
@controllers_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            email = request.form['email']
            password = request.form['password']

            # Validar el formato del correo
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash("Correo no válido.", "error")
                return redirect(url_for('controllers.registro'))

            # Eliminar la validación estricta de la contraseña
            # Validar si el correo ya está registrado
            if Organizador.query.filter_by(email=email).first():
                flash("El correo ya está registrado.", "error")
                return redirect(url_for('controllers.registro'))

            # Encriptar la contraseña y guardar el organizador
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            nuevo_organizador = Organizador(nombre=nombre, email=email, password=hashed_password)

            db.session.add(nuevo_organizador)
            db.session.commit()

            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('controllers.login'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error durante el registro: {str(e)}", "error")
            return redirect(url_for('controllers.registro'))

    return render_template('registro.html')





@controllers_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Intentando iniciar sesión: Email={email}, Password={password}")

        # Verificar las credenciales del usuario
        user = Organizador.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # Guardar información del usuario en la sesión
            session['user_id'] = user.id_organizador
            session['user_name'] = user.nombre
            session['user_email'] = user.email
            flash("Inicio de sesión exitoso.", "success")
            print("Inicio de sesión exitoso.")
            return redirect(url_for('controllers.home'))
        else:
            flash("Correo o contraseña incorrectos.", "error")
            print("Correo o contraseña incorrectos.")

    return render_template('login.html')


@controllers_bp.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "info")
    print("Sesión cerrada correctamente.")
    return redirect(url_for('controllers.login'))


# --- Rutas protegidas ---
@controllers_bp.route('/')
def home():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "error")
        print("Intento de acceso sin sesión activa.")
        return redirect(url_for('controllers.login'))

    eventos = Evento.query.order_by(Evento.fecha_creacion.desc()).all()
    return render_template("index.html", eventos=eventos, user_name=session.get('user_name'))


@controllers_bp.route('/crear_evento', methods=['GET', 'POST'])
def crear_evento():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para crear un evento.", "error")
        print("Intento de crear evento sin sesión activa.")
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
            flash("Debes seleccionar una categoría.", "error")
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

            flash("Evento creado exitosamente.", "success")
            print("Evento creado exitosamente.")
            return redirect(url_for('controllers.home'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear el evento: {e}")
            flash(f"Error al crear el evento: {e}", "error")

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

        # Verificar si el asistente ya existe en la tabla "asistentes"
        asistente = Asistente.query.filter_by(email=email).first()

        if not asistente:
            # Si no existe, crear un nuevo asistente
            asistente = Asistente(nombre=nombre, email=email)
            db.session.add(asistente)
            db.session.commit()

        # Verificar si el asistente ya está registrado para este evento en la tabla intermedia
        evento_asistente = db.session.execute(
            db.text("""
                SELECT 1 FROM evento_asistente
                WHERE id_asistente = :id_asistente AND id_evento = :id_evento
            """),
            {"id_asistente": asistente.id_asistente, "id_evento": id_evento}
        ).fetchone()

        if evento_asistente:
            return jsonify({'message': f'Ya estás registrado en este evento, {nombre} ({email}).'}), 200

        # Registrar al asistente en el evento
        db.session.execute(
            db.text("""
                INSERT INTO evento_asistente (id_evento, id_asistente)
                VALUES (:id_evento, :id_asistente)
            """),
            {"id_evento": id_evento, "id_asistente": asistente.id_asistente}
        )
        db.session.commit()

        return jsonify({'message': f'¡Registro exitoso como asistente en el evento {id_evento}, {nombre} ({email})!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

