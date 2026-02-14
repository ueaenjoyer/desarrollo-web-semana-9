from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    """Página principal de TechByte - Tienda de Gadgets"""
    return render_template("index.html")

@app.route("/producto/<nombre>")
def producto(nombre):
    """Ruta dinámica para mostrar información de productos"""
    return f"""
    <h1>🔍 Producto: {nombre}</h1>
    <p>Estado: <strong>Disponible en TechByte</strong></p>
    <p>Este producto está listo para ser agregado a tu carrito.</p>
    <a href="/">← Volver al inicio</a>
    """

if __name__ == "__main__":
    # debug=True permite que el servidor se reinicie automáticamente al cambiar el código
    app.run(debug=True)
