-- ============================================
-- TechByte - Script de Base de Datos
-- Semana 15 - PostgreSQL (Supabase)
-- ============================================
-- 3 Tablas Relacionadas:
--   categorias → productos (1:N via id_categoria FK)
--   productos → ventas (1:N via id_producto FK)
-- + usuarios (independiente, para login admin)
-- ============================================

-- Tabla de CATEGORÍAS
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT DEFAULT ''
);

-- Tabla de PRODUCTOS (FK a categorias)
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    id_categoria INTEGER REFERENCES categorias(id) ON DELETE SET NULL,
    precio NUMERIC(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    descripcion TEXT DEFAULT ''
);

-- Tabla de VENTAS (FK a productos)
CREATE TABLE IF NOT EXISTS ventas (
    id SERIAL PRIMARY KEY,
    id_producto INTEGER NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    cliente_nombre VARCHAR(200) NOT NULL,
    cliente_email VARCHAR(200) DEFAULT '',
    cantidad INTEGER NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de USUARIOS (login admin)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    mail VARCHAR(200) UNIQUE NOT NULL,
    password VARCHAR(300) NOT NULL
);

-- ============================================
-- DATOS DE EJEMPLO
-- ============================================

-- Categorías iniciales
INSERT INTO categorias (nombre, descripcion) VALUES
    ('Laptops', 'Computadoras portátiles de alto rendimiento'),
    ('Smartphones', 'Teléfonos inteligentes de última generación'),
    ('Audio', 'Audífonos, parlantes y equipos de sonido'),
    ('Accesorios', 'Cargadores, cables, fundas y más'),
    ('Gaming', 'Consolas, controles y periféricos para gamers'),
    ('Tablets', 'Tablets para trabajo y entretenimiento'),
    ('Wearables', 'Relojes inteligentes y dispositivos portátiles'),
    ('Otros', 'Otros productos tecnológicos')
ON CONFLICT (nombre) DO NOTHING;

-- Productos de ejemplo
INSERT INTO productos (nombre, id_categoria, precio, stock, descripcion) VALUES
    ('MacBook Pro 16 M3', 1, 2499.99, 10, 'Laptop Apple con chip M3 Pro, 18GB RAM, 512GB SSD'),
    ('iPhone 15 Pro Max', 2, 1199.99, 25, 'Smartphone Apple con chip A17 Pro, cámara 48MP'),
    ('AirPods Pro 2', 3, 249.99, 50, 'Auriculares con cancelación de ruido activa'),
    ('Cargador MagSafe', 4, 39.99, 100, 'Cargador inalámbrico magnético para iPhone'),
    ('PS5 Slim', 5, 449.99, 15, 'Consola PlayStation 5 versión delgada'),
    ('iPad Air M2', 6, 599.99, 20, 'Tablet Apple con chip M2, pantalla 10.9"'),
    ('Apple Watch Series 9', 7, 399.99, 30, 'Reloj inteligente con sensor de temperatura'),
    ('Samsung Galaxy S24 Ultra', 2, 1299.99, 18, 'Smartphone Samsung con S-Pen y cámara 200MP'),
    ('Sony WH-1000XM5', 3, 349.99, 35, 'Auriculares premium con cancelación de ruido'),
    ('Logitech G Pro X', 5, 129.99, 40, 'Teclado mecánico para gaming profesional')
ON CONFLICT DO NOTHING;
