# ============================================
# IMPORTACIONES
# ============================================

# Flask: El framework web principal que usamos para crear la aplicación
from flask import Flask, render_template

# render_template: Función que permite renderizar plantillas HTML con Jinja2
# En lugar de retornar texto plano (strings), usamos render_template para:
# 1. Separar la lógica (Python) de la presentación (HTML)
# 2. Reutilizar código HTML mediante herencia de plantillas
# 3. Pasar datos dinámicos desde Python a las plantillas


# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================

# Creamos la instancia de la aplicación Flask
# __name__ le dice a Flask dónde buscar recursos (templates, static, etc.)
app = Flask(__name__)


# ============================================
# RUTAS (ROUTES) Y VISTAS (VIEWS)
# ============================================

# Una RUTA define qué URL activará una función específica
# Una VISTA es la función que se ejecuta cuando se accede a esa ruta

@app.route("/")  # Decorador que asocia la URL "/" con la función index()
def index():
    """
    Página principal de TechByte - Tienda de Gadgets
    
    Esta es la vista para la ruta raíz ("/") de la aplicación.
    Cuando un usuario visita http://localhost:5000/, esta función se ejecuta.
    
    render_template("index.html") hace lo siguiente:
    1. Busca el archivo "index.html" en la carpeta "templates/"
    2. Procesa las directivas de Jinja2 ({% extends %}, {% block %}, etc.)
    3. Genera el HTML final combinando base.html e index.html
    4. Retorna ese HTML al navegador del usuario
    """
    return render_template("index.html")


@app.route("/about")  # Ruta para la página "Acerca de"
def about():
    """
    Página "Acerca de" - Información sobre TechByte
    
    Esta vista renderiza la plantilla about.html que contiene:
    - Historia de la empresa
    - Misión y visión
    - Valores corporativos
    - Información del equipo
    
    Nota: El nombre de la función (about) se usa en url_for('about')
    en las plantillas para generar enlaces a esta página.
    """
    return render_template("about.html")


@app.route("/productos")  # Ruta para el catálogo de productos
def productos():
    """
    Página de Productos - Catálogo completo de gadgets
    
    Actualmente muestra productos estáticos definidos en productos.html.
    
    En futuras versiones, esta función podría:
    1. Consultar una base de datos para obtener productos
    2. Pasar esos datos a la plantilla usando:
       return render_template("productos.html", productos=lista_productos)
    3. La plantilla usaría un bucle {% for %} para mostrar cada producto
    
    Ejemplo de cómo pasar datos a una plantilla:
    productos_db = [
        {"nombre": "Laptop X", "precio": 999},
        {"nombre": "Phone Y", "precio": 699}
    ]
    return render_template("productos.html", productos=productos_db)
    """
    return render_template("productos.html")


@app.route("/contacto")  # Ruta para la página de contacto
def contacto():
    """
    Página de Contacto - Información de contacto y formulario
    
    Renderiza la plantilla contacto.html que incluye:
    - Información de contacto (teléfono, email, dirección)
    - Horarios de atención
    - Preguntas frecuentes
    - Placeholder para formulario de contacto (próximamente)
    
    En el futuro, esta ruta podría manejar el envío de formularios:
    @app.route("/contacto", methods=["GET", "POST"])
    def contacto():
        if request.method == "POST":
            # Procesar datos del formulario
            nombre = request.form.get("nombre")
            email = request.form.get("email")
            # Enviar email, guardar en DB, etc.
        return render_template("contacto.html")
    """
    return render_template("contacto.html")


@app.route("/producto/<nombre>")  # Ruta DINÁMICA con parámetro
def producto(nombre):
    """
    Ruta dinámica para mostrar información de productos individuales
    
    El parámetro <nombre> en la ruta captura parte de la URL.
    Por ejemplo:
    - /producto/laptop → nombre = "laptop"
    - /producto/iphone → nombre = "iphone"
    
    Esta función actualmente retorna HTML plano (no usa plantilla).
    Es un ejemplo de ruta dinámica que quedó de la semana anterior.
    
    MEJORA FUTURA: Crear una plantilla producto_detalle.html y hacer:
    return render_template("producto_detalle.html", nombre_producto=nombre)
    
    Luego en la plantilla podrías usar: {{ nombre_producto }}
    """
    return f"""
    <h1>🔍 Producto: {nombre}</h1>
    <p>Estado: <strong>Disponible en TechByte</strong></p>
    <p>Este producto está listo para ser agregado a tu carrito.</p>
    <a href="/">← Volver al inicio</a>
    """


# ============================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ============================================

if __name__ == "__main__":
    """
    Este bloque se ejecuta solo cuando ejecutas este archivo directamente
    (python app.py), no cuando se importa como módulo.
    
    app.run() inicia el servidor de desarrollo de Flask.
    
    Parámetros importantes:
    - debug=True: Habilita el modo de depuración
      * El servidor se reinicia automáticamente cuando cambias el código
      * Muestra errores detallados en el navegador (útil para desarrollo)
      * NUNCA uses debug=True en producción (es un riesgo de seguridad)
    
    - host='0.0.0.0': Hace que el servidor sea accesible desde otras máquinas
    - port=5000: Puerto en el que corre el servidor (por defecto es 5000)
    
    Para ejecutar:
    1. Abre la terminal en la carpeta del proyecto
    2. Activa el entorno virtual: .venv\\Scripts\\activate (Windows)
    3. Ejecuta: python app.py
    4. Abre el navegador en: http://localhost:5000
    """
    app.run(debug=True)
