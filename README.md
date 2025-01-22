# Eventos Disponibles

Este es un proyecto para gestionar eventos en línea. Permite a los organizadores crear eventos, visualizarlos, editarlos y agregarles categorías. También permite ver gráficos comparativos de los eventos y gestionar los gastos asociados a los mismos.

## Funcionalidades

### 1. Gestión de Eventos
- Crear nuevos eventos con información como nombre, fecha, hora, lugar, presupuesto y categorías.
- Editar eventos ya creados.
- Ver los eventos creados con detalles sobre las categorías, fechas, horarios y presupuestos.

### 2. Categorías de Eventos
- Cada evento puede tener una o más categorías asociadas.
- Las categorías son consultadas y mostradas de forma dinámica para cada evento.

### 3. Gestión de Gastos
- Los organizadores pueden registrar los gastos asociados a cada evento.
- Los gastos pueden ser visualizados y editados.

### 4. Gráficos Comparativos
- Los organizadores pueden ver gráficos comparativos entre el presupuesto y el costo final de los eventos.

### 5. Autenticación de Usuario
- Los organizadores deben registrarse e iniciar sesión para poder crear y gestionar eventos.
- La sesión se maneja con cookies para mantener el estado de la autenticación.

### 6. Sugerencias de Eventos
- Los usuarios pueden obtener sugerencias basadas en las categorías, lugares y presupuestos de eventos anteriores.

## Tecnologías Utilizadas

### Backend:
- **Flask**: Framework web en Python para el desarrollo del backend.
- **SQLAlchemy**: ORM para la interacción con la base de datos.
- **PostgreSQL**: Base de datos utilizada para almacenar la información de los eventos, usuarios y categorías.

### Frontend:
- **Vue.js**: Framework de JavaScript para construir la interfaz de usuario interactiva.
- **Chart.js**: Librería para generar gráficos visuales de los datos de los eventos.
- **TailwindCSS**: Framework de diseño CSS para la creación de la interfaz de usuario.

## Instalación

### Requisitos
- Python 3.7 o superior.
- Node.js (para las dependencias de Vue.js).
- PostgreSQL.

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```
## Paso 2: Configurar el entorno
Crea un entorno virtual para Python:

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa venv\Scripts\activate
```

## Paso 3: Instalar dependencias de Python
```bash
pip install -r requirements.txt
```

## Paso 4: Configurar la base de datos
Asegúrate de tener una base de datos PostgreSQL configurada y actualiza las credenciales en el archivo de configuración `config.py` o en el código del proyecto.

## Paso 5: Instalar dependencias de Node.js
```bash
cd frontend
npm install
```

## Paso 6: Ejecutar el proyecto
Para ejecutar el proyecto en modo desarrollo:

1. Inicia el servidor de Flask:
   ```bash
   python app.py
   ```

El backend se ejecutará en `http://127.0.0.1:5000` y el frontend en `http://localhost:8080`.

## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

