-- Tabla de Organizadores
CREATE TABLE organizadores (
    id_organizador SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Eventos
CREATE TABLE eventos (
    id_evento SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    lugar VARCHAR(255) NOT NULL,
    presupuesto NUMERIC NOT NULL,
    id_organizador INTEGER NOT NULL REFERENCES organizadores(id_organizador),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Categorías
CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL
);

-- Tabla de Categorías por Evento (relación muchos a muchos)
CREATE TABLE evento_categoria (
    id_evento INTEGER NOT NULL REFERENCES eventos(id_evento) ON DELETE CASCADE,
    id_categoria INTEGER NOT NULL REFERENCES categorias(id_categoria) ON DELETE CASCADE,
    PRIMARY KEY (id_evento, id_categoria)
);

-- Tabla de Asistentes
CREATE TABLE asistentes (
    id_asistente SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    eventos_registrados TEXT
);

-- Tabla de Gastos
CREATE TABLE gastos (
    id_gasto SERIAL PRIMARY KEY,
    id_evento INTEGER NOT NULL REFERENCES eventos(id_evento) ON DELETE CASCADE,
    descripcion TEXT NOT NULL,
    cantidad NUMERIC NOT NULL,
    fecha_gasto TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
