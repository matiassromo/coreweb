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

## Principios SOLID Aplicados

1. **Single Responsibility Principle (SRP)**
   - **`EventService`** maneja la lógica de negocio relacionada con los eventos.
   - **`EventoRepository`** se encarga de las operaciones de acceso a datos, como la consulta de eventos en la base de datos.
   - Cada clase tiene una responsabilidad única, lo que facilita su mantenimiento y extensión.

2. **Dependency Inversion Principle (DIP)**
   - **`EventService`** depende de **`EventoRepository`** para obtener datos de eventos, pero no está acoplada a una implementación específica. Esto permite intercambiar el repositorio sin afectar el resto del código.

## Patrones de Diseño Aplicados

1. **Repository Pattern**
   - Se ha implementado el patrón **Repository** en **`EventoRepository`** para separar la lógica de acceso a datos de la lógica de negocio. Esto hace que la capa de persistencia esté bien definida y aislada del resto de la aplicación.
   
2. **Dependency Injection**
   - La **inyección de dependencias** se aplica al pasar **`EventoRepository`** como una dependencia en **`EventService`**, lo que desacopla estas clases y facilita su prueba y mantenimiento.

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

