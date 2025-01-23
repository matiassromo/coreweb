from flask import Blueprint, render_template, request, redirect, session, flash, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, Organizador, Evento, Categoria, EventoCategoria, Asistencia
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
        return redirect(url_for('controllers.login'))

    # Obtener las fechas desde los parámetros de la URL
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    
    # Filtrar eventos si las fechas están presentes
    if start_date and end_date:
        eventos = Evento.query.filter(Evento.fecha.between(start_date, end_date)).all()
    else:
        eventos = Evento.query.all()

    # Pasar los eventos al template
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
# Ruta para obtener todos los eventos
@controllers_bp.route('/api/eventos')
def get_eventos():
    eventos = Evento.query.order_by(Evento.fecha_creacion.desc()).limit(20).all()
    eventos_json = [
        {
            "id_evento": evento.id_evento,
            "nombre": evento.nombre,
            "descripcion": evento.descripcion,
            "fecha": evento.fecha.strftime("%Y-%m-%d"),
            "hora": evento.hora.strftime("%H:%M:%S") if evento.hora else None,
            "lugar": evento.lugar,
            "presupuesto": float(evento.presupuesto),
            "categoria": Categoria.query.get(EventoCategoria.query.filter_by(id_evento=evento.id_evento).first().id_categoria).nombre if EventoCategoria.query.filter_by(id_evento=evento.id_evento).first() else "Sin categoría",
            "asistentes_count": len(evento.asistencias)  # Contamos las asistencias de este evento
        }
        for evento in eventos
    ]
    return jsonify(eventos_json)




@controllers_bp.route('/gastos', methods=['GET', 'POST'])
def gastos():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para gestionar tus eventos.', 'danger')
        return redirect(url_for('controllers.login'))

    # Obtener los eventos creados por el usuario autenticado
    eventos_usuario = Evento.query.filter_by(id_organizador=session['user_id']).all()
    categorias = Categoria.query.all()
    evento_seleccionado = None

    if request.method == 'POST':
        # Si el usuario selecciona un evento para editar
        if 'seleccionar_evento' in request.form:
            evento_id = request.form['evento_id']
            evento_seleccionado = Evento.query.get_or_404(evento_id)

        # Si el usuario guarda cambios en el evento seleccionado
        elif 'guardar_cambios' in request.form:
            evento_id = request.form['evento_id']
            evento = Evento.query.get_or_404(evento_id)

            if evento.id_organizador != session['user_id']:
                flash('No tienes permiso para editar este evento.', 'danger')
                return redirect(url_for('controllers.gastos'))

            # Actualizar los datos del evento
            evento.nombre = request.form.get('nombre')
            evento.descripcion = request.form.get('descripcion')
            evento.fecha = request.form.get('fecha')
            evento.hora = request.form.get('hora')
            evento.lugar = request.form.get('lugar')
            evento.presupuesto = request.form.get('presupuesto')
            
            # Actualizar la categoría asociada al evento
            nueva_categoria_id = request.form.get('categoria')
            if nueva_categoria_id:
                # Eliminar la categoría existente
                EventoCategoria.query.filter_by(id_evento=evento.id_evento).delete()
                # Asociar la nueva categoría
                nueva_categoria = EventoCategoria(
                    id_evento=evento.id_evento,
                    id_categoria=nueva_categoria_id
                )
                db.session.add(nueva_categoria)

            # Guardar el precio final proporcionado por el usuario
            precio_final = request.form.get('precio_final')
            if precio_final:
                try:
                    # Verificar si ya existe un registro en gastos para este evento
                    gasto_existente = db.session.execute(
                        db.text("SELECT id_gasto FROM gastos WHERE id_evento = :id_evento"),
                        {"id_evento": evento.id_evento}
                    ).scalar()

                    if gasto_existente:
                        # Actualizar el registro existente
                        db.session.execute(
                            db.text("UPDATE gastos SET cantidad = :precio_final WHERE id_evento = :id_evento"),
                            {"precio_final": precio_final, "id_evento": evento.id_evento}
                        )
                    else:
                        # Insertar un nuevo registro en la tabla gastos
                        db.session.execute(
                            db.text(
                                "INSERT INTO gastos (id_evento, descripcion, cantidad) VALUES (:id_evento, :descripcion, :precio_final)"
                            ),
                            {"id_evento": evento.id_evento, "descripcion": "Precio Final del Evento", "precio_final": precio_final}
                        )

                    db.session.commit()
                    flash('Evento y precio final actualizados exitosamente.', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error al actualizar el precio final: {e}', 'danger')

            try:
                db.session.commit()
                flash('Evento actualizado exitosamente.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al actualizar el evento: {e}', 'danger')

    # Obtener los gastos asociados a los eventos con una consulta explícita
    gastos_por_evento = {
        evento.id_evento: db.session.execute(
            db.text("SELECT SUM(cantidad) FROM gastos WHERE id_evento = :id_evento"),
            {"id_evento": evento.id_evento}
        ).scalar() or 0
        for evento in eventos_usuario
    }

    return render_template('gastos.html', eventos=eventos_usuario, evento_seleccionado=evento_seleccionado, gastos_por_evento=gastos_por_evento, categorias=categorias)

@controllers_bp.route('/api/eventos_grafico', methods=['GET'])
def eventos_grafico():
    if 'user_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión para ver esta información.'}), 401

    eventos = db.session.execute(
        db.text("""
            SELECT 
                id_evento,
                nombre, 
                presupuesto, 
                COALESCE((SELECT SUM(cantidad) FROM gastos WHERE id_evento = eventos.id_evento), 0) AS costo_final
            FROM eventos
            WHERE id_organizador = :id_organizador
        """),
        {"id_organizador": session['user_id']}
    ).fetchall()

    eventos_data = [
        {"id_evento": evento.id_evento, "nombre": evento.nombre, "presupuesto": float(evento.presupuesto), "costo_final": float(evento.costo_final)}
        for evento in eventos
    ]

    return jsonify(eventos_data)

@controllers_bp.route('/grafico')
def grafico():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver esta página.', 'danger')
        return redirect(url_for('login'))
    return render_template('grafico.html')

@controllers_bp.route('/sugerencias_evento', methods=['GET', 'POST'])
def sugerencias_evento():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta funcionalidad.", "error")
        return redirect(url_for('controllers.login'))

    # Consultar todas las categorías disponibles
    categorias = Categoria.query.all()

    # Inicializar filtros
    categoria_seleccionada = request.form.get('categoria', None)
    presupuesto_filtro = request.form.get('presupuesto', None)

    # Convertir presupuesto si se ingresó
    try:
        presupuesto_filtro = float(presupuesto_filtro) if presupuesto_filtro else None
    except ValueError:
        flash("El presupuesto debe ser un número válido.", "error")
        return redirect(url_for('controllers.sugerencias_evento'))

    # Filtrar eventos históricos según los filtros seleccionados
    query = Evento.query

    if categoria_seleccionada:
        # Filtrar eventos que coincidan con la categoría seleccionada
        query = query.join(EventoCategoria).filter(EventoCategoria.id_categoria == categoria_seleccionada)

    if presupuesto_filtro:
        # Filtrar eventos con presupuestos similares (+/- 20%)
        query = query.filter(Evento.presupuesto.between(presupuesto_filtro * 0.8, presupuesto_filtro * 1.2))

    eventos_historicos = query.all()

    # Inicializar contadores y acumuladores para las sugerencias
    lugares_contador = {}
    categorias_contador = {}
    presupuestos = []

    # Procesar los eventos filtrados
    for evento in eventos_historicos:
        # Categorías asociadas al evento
        categorias_evento = [
            ec.id_categoria
            for ec in EventoCategoria.query.filter_by(id_evento=evento.id_evento).all()
        ]

        # Contar lugares
        lugares_contador[evento.lugar] = lugares_contador.get(evento.lugar, 0) + 1

        # Acumular presupuestos
        presupuestos.append(evento.presupuesto)

        # Contar categorías
        for categoria in categorias_evento:
            categorias_contador[categoria] = categorias_contador.get(categoria, 0) + 1

    # Sugerir lugar más frecuente
    lugar_sugerido = max(lugares_contador, key=lugares_contador.get, default=None)

    # Sugerir presupuesto promedio
    presupuesto_sugerido = round(sum(presupuestos) / len(presupuestos), 2) if presupuestos else None

    # Sugerir categoría solo si no se seleccionó una
    categoria_sugerida_id = (
        max(categorias_contador, key=categorias_contador.get, default=None)
        if not categoria_seleccionada else None
    )
    categoria_sugerida = (
        Categoria.query.get(categoria_sugerida_id).nombre if categoria_sugerida_id else None
    )

    # Crear un mensaje de sugerencias
    sugerencias = {
        "categoria": categoria_sugerida or None,
        "lugar": lugar_sugerido or "No se encontró un lugar sugerido.",
        "presupuesto": presupuesto_sugerido or "No se encontró un presupuesto sugerido.",
    }

    return render_template(
        'sugerencias_evento.html',
        sugerencias=sugerencias,
        categorias=categorias,
        categoria_seleccionada=categoria_seleccionada,
        presupuesto_filtro=presupuesto_filtro,
    )
    
    
@controllers_bp.route('/asistir_evento/<int:id_evento>', methods=['POST'])
def asistir_evento(id_evento):
    if 'user_id' not in session:
        flash("Debes iniciar sesión para asistir a un evento.", "error")
        return redirect(url_for('controllers.login'))

    evento = Evento.query.get_or_404(id_evento) #se busca el evento en la bdd
    if evento:
        # Crea un nuevo registro de asistencia en base al evento que desea asistir y el id usuario que asisite
        asistencia = Asistencia(id_evento=id_evento, id_usuario=session['user_id'])
        
        db.session.add(asistencia)
        
        db.session.commit()
        flash(f"Te has inscrito correctamente al evento {evento.nombre}.", "success")

    return redirect(url_for('controllers.home'))


@controllers_bp.route('/filtrar_eventos', methods=['GET'])
def filtrar_eventos():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta funcionalidad.", "error")
        return redirect(url_for('controllers.login'))

    # Obtener las fechas de los parámetros 'start_date' y 'end_date'
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)

    if start_date and end_date:
        # Filtrar los eventos por fecha de asistencia 
        eventos = Evento.query.join(Asistencia).filter(
            Asistencia.fecha_asistencia.between(start_date, end_date)
        ).all()
    else:
        # Si no hay filtro, obtener todos los eventos
        eventos = Evento.query.all()

    return render_template('index.html', eventos=eventos)


if __name__ == "__main__":
    controllers_bp.run(debug=True)


