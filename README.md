# TechByte - Proyecto Final Desarrollo Web (Semana 15)

**Desarrollador:** Paul
**Asignatura:** Desarrollo Web

Este proyecto representa la culminación práctica de los conceptos abordados durante el curso. Se trata de una tienda en línea (TechByte) construida con Python y **Flask**, respaldada por una base de datos relacional **PostgreSQL** alojada en la nube (Supabase).

---

## 🏗️ Estructura y Arquitectura del Proyecto

El sistema fue refactorizado esta semana para implementar una sólida **Arquitectura en Capas (N-Tier/MVC)**. El objetivo principal es separar las responsabilidades del código de manera limpia y mantenible:

1.  **Modelos (`models/`):** Contiene las clases orientadas a objetos (`Producto`, `Categoria`, `Venta`, `Usuario`) que mapean los datos traídos de la base de datos hacia estructuras lógicas nativas de Python.
2.  **Servicios (`services/`):** Capa encargada de la lógica de negocio y las consultas de persistencia (SQL CRUD). Archivos como `producto_service.py` aíslan al controlador principal de contactar directamente a la base de datos. También gestionan la integridad, por ejemplo, **descontando el stock** automáticamente tras registrar una venta.
3.  **Formularios (`forms/`):** Capa de validación abstracta. Todas las peticiones `POST` que recibe el servidor pasan por estas clases (ej. `VentaForm`) asegurando que los tipos de datos sean correctos antes de insertarlos a PostgreSQL.
4.  **Controlador (`app.py`):** Mantiene únicamente las reglas de enrutamiento (Flask `@app.route`), la inyección de Jinja2 a `templates/` y la inicialización de la librería `fpdf2` para exportar documentos PDF en memoria.
5.  **Base de Datos Relacional (`database.sql`):** Script base con **4 tablas** relacionales, priorizando restricciones y foreign keys:
    *   `categorias` (1) → (N) `productos`
    *   `productos` (1) → (N) `ventas`
    *   `usuarios` (Base para el login).

---

## 🧪 Instrucciones para el Docente (Prueba del Proyecto)

Para evaluar todas las rúbricas estipuladas para este proyecto, siga estos pasos de verificación:

### 1. Acceso al Proyecto Desplegado (Recomendado)
El proyecto ha sido desplegado en producción utilizando **Render**. Puede probar todas las funcionalidades directamente sin necesidad de instalaciones locales haciendo clic en el siguiente enlace:
👉 **[https://desarrollo-web-semana-9.onrender.com/](https://desarrollo-web-semana-9.onrender.com/)**

### 2. Primera Vista (Sitio Público)
Abra el enlace del proyecto o navegue a la raíz del sitio:
*   Podrá observar el catálogo público donde **cualquier visitante** puede visualizar los gadgets de TechByte, categorizados visualmente sin necesidad de autenticarse.
*   Note los indicadores de "Agotado" y validaciones de visualización en los diseños.

### 3. Ingreso al Panel Administrativo
Haga clic en el botón de la barra de menú superior derecha ("🔑 Admin") o diríjase a la ruta `/login` en la URL desplegada.

El sistema cuenta con prevención contra intrusos (decoradores con soporte de encriptado Hash en Werkzeug). Para testear el acceso use las siguientes credenciales maestras autogeneradas por la plataforma:

*   **Email del Administrador:** `admin@techbyte.com`
*   **Contraseña:** `admin123`

### 4. Evaluación de Operaciones (CRUD Completo)
Una vez en el Dashboard analítico, podrá observar las siguientes funciones conectadas al motor en vivo de Postgres:
1.  **Gestión de Categorías:** Permite dar de alta secciones y editarlas (`INSERT`/`UPDATE`/`DELETE`).
2.  **Gestión de Productos:** Cada producto depende rigurosamente de su categoría vinculada por `id_categoria` (Clave foránea probada). 
3.  **Gestión de Ventas:** Intente registrar una venta; se validará que **haya stock suficiente** en el producto, calculará el total en función del costo unitario y finalmente **descontará la cantidad comprada de la base de datos**.

### 5. Generación de Reportes PDF
Ingrese a cualquiera de los submenús del Dashboard que indican "📄 Reporte Productos" o "📄 Reporte Ventas". 
1.  La aplicación se valdrá de `fpdf2`.
2.  Descargará (sin necesidad de instalaciones extras) reportes estilizados mapeando los resultados desde sus listas de Diccionarios y SQL. No almacenan basura residual en el disco local ya que responden transcodificados a bytes.

---

Cualquier duda adicional referente al diseño de dependencias o esquemas, contactar directamente para soporte local. 
¡Gracias!
