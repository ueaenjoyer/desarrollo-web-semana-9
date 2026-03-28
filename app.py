# ============================================
# app.py - Aplicación Principal TechByte
# Semana 15 - Tienda de Gadgets
# ============================================
#
# Rutas públicas: Inicio, Catálogo, Detalle, Contacto, Login
# Rutas admin: Dashboard, CRUD Productos/Categorías/Ventas, PDF
# ============================================

from flask import (Flask, render_template, request, redirect,
                   url_for, flash, session, make_response)
from functools import wraps
import os

# Servicios (capa de lógica de negocio)
from services import categoria_service, producto_service, venta_service, usuario_service

# Formularios (capa de validación)
from forms.producto_form import ProductoForm
from forms.categoria_form import CategoriaForm
from forms.venta_form import VentaForm

# Generación de PDF
from fpdf import FPDF
from datetime import datetime
import io

# ============================================
# CONFIGURACIÓN
# ============================================

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'techbyte_semana15_secret_key')

# ============================================
# INICIALIZACIÓN DE TABLAS
# ============================================

with app.app_context():
    categoria_service.init_tabla()
    producto_service.init_tabla()
    usuario_service.init_tabla()
    venta_service.init_tabla()


# ============================================
# DECORADOR: Login Requerido
# ============================================

def login_requerido(f):
    """Decorador que protege rutas que requieren autenticación."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash('🔒 Debes iniciar sesión para acceder a esta sección.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================
# RUTAS PÚBLICAS
# ============================================

@app.route("/")
def index():
    """Página principal de la tienda."""
    productos = producto_service.obtener_todos()
    # Mostrar los últimos 4 productos como destacados
    destacados = productos[-4:] if len(productos) >= 4 else productos
    categorias = categoria_service.obtener_todas()
    return render_template("index.html", destacados=destacados, categorias=categorias)


@app.route("/catalogo")
def catalogo():
    """Catálogo público de productos con filtro por categoría."""
    categoria_id = request.args.get('categoria', type=int)
    categorias = categoria_service.obtener_todas()

    if categoria_id:
        productos = producto_service.obtener_por_categoria(categoria_id)
        categoria_activa = categoria_service.obtener_por_id(categoria_id)
    else:
        productos = producto_service.obtener_todos()
        categoria_activa = None

    return render_template("catalogo.html",
                           productos=productos,
                           categorias=categorias,
                           categoria_activa=categoria_activa)


@app.route("/producto/<int:id>")
def producto_detalle(id):
    """Detalle de un producto específico."""
    producto = producto_service.obtener_por_id(id)
    if not producto:
        flash("❌ Producto no encontrado.", "error")
        return redirect(url_for('catalogo'))
    return render_template("producto_detalle.html", producto=producto)


@app.route("/contacto")
def contacto():
    """Página de contacto."""
    return render_template("contacto.html")


# ============================================
# LOGIN / LOGOUT
# ============================================

@app.route("/login", methods=["GET", "POST"])
def login():
    """Inicio de sesión del administrador."""
    if 'usuario' in session:
        return redirect(url_for('admin_dashboard'))

    if request.method == "POST":
        mail = request.form.get('mail', '').strip()
        password = request.form.get('password', '').strip()

        if not mail or not password:
            flash('❌ Completa todos los campos.', 'error')
            return render_template("login.html")

        usuario = usuario_service.autenticar(mail, password)
        if usuario:
            session['usuario'] = usuario
            flash(f"✅ Bienvenido, {usuario['nombre']}!", 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('❌ Correo o contraseña incorrectos.', 'error')

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Cierra la sesión del administrador."""
    session.pop('usuario', None)
    flash('👋 Sesión cerrada correctamente.', 'success')
    return redirect(url_for('index'))


# ============================================
# ADMIN: DASHBOARD
# ============================================

@app.route("/admin")
@app.route("/admin/dashboard")
@login_requerido
def admin_dashboard():
    """Panel de administración con estadísticas."""
    total_productos = producto_service.contar()
    total_ventas = venta_service.contar()
    ingresos = venta_service.total_ingresos()
    categorias = categoria_service.obtener_todas()

    return render_template("admin/dashboard.html",
                           total_productos=total_productos,
                           total_ventas=total_ventas,
                           ingresos=ingresos,
                           total_categorias=len(categorias))


# ============================================
# ADMIN: CRUD PRODUCTOS
# ============================================

@app.route("/admin/productos")
@login_requerido
def admin_productos():
    """Lista de productos con acciones CRUD."""
    productos = producto_service.obtener_todos()
    return render_template("admin/productos.html", productos=productos)


@app.route("/admin/productos/agregar", methods=["GET", "POST"])
@login_requerido
def admin_producto_agregar():
    """Formulario para agregar un nuevo producto."""
    categorias = categoria_service.obtener_todas()

    if request.method == "POST":
        form = ProductoForm.desde_request(request.form)
        if not form.es_valido():
            for error in form.errores:
                flash(error, 'error')
            return render_template("admin/producto_form.html",
                                   categorias=categorias, accion="Agregar")

        producto_id = producto_service.insertar(
            form.nombre, form.id_categoria, form.precio, form.stock, form.descripcion
        )
        flash(f"✅ Producto '{form.nombre}' agregado con éxito (ID: {producto_id}).", 'success')
        return redirect(url_for('admin_productos'))

    return render_template("admin/producto_form.html",
                           categorias=categorias, accion="Agregar")


@app.route("/admin/productos/editar/<int:id>", methods=["GET", "POST"])
@login_requerido
def admin_producto_editar(id):
    """Formulario para editar un producto existente."""
    producto = producto_service.obtener_por_id(id)
    categorias = categoria_service.obtener_todas()

    if not producto:
        flash(f"❌ No se encontró producto con ID {id}.", 'error')
        return redirect(url_for('admin_productos'))

    if request.method == "POST":
        form = ProductoForm.desde_request(request.form)
        if not form.es_valido():
            for error in form.errores:
                flash(error, 'error')
            return render_template("admin/producto_form.html",
                                   categorias=categorias, producto=producto, accion="Editar")

        if producto_service.actualizar(id, form.nombre, form.id_categoria,
                                        form.precio, form.stock, form.descripcion):
            flash(f"✅ Producto '{form.nombre}' actualizado correctamente.", 'success')
        else:
            flash("❌ Error al actualizar el producto.", 'error')
        return redirect(url_for('admin_productos'))

    return render_template("admin/producto_form.html",
                           categorias=categorias, producto=producto, accion="Editar")


@app.route("/admin/productos/eliminar/<int:id>", methods=["POST"])
@login_requerido
def admin_producto_eliminar(id):
    """Elimina un producto."""
    producto = producto_service.obtener_por_id(id)
    nombre = producto['nombre'] if producto else f"ID {id}"

    if producto_service.eliminar(id):
        flash(f"✅ Producto '{nombre}' eliminado correctamente.", 'success')
    else:
        flash(f"❌ No se pudo eliminar el producto.", 'error')

    return redirect(url_for('admin_productos'))


# ============================================
# ADMIN: CRUD CATEGORÍAS
# ============================================

@app.route("/admin/categorias")
@login_requerido
def admin_categorias():
    """Lista de categorías con acciones CRUD."""
    categorias = categoria_service.obtener_todas()
    return render_template("admin/categorias.html", categorias=categorias)


@app.route("/admin/categorias/agregar", methods=["GET", "POST"])
@login_requerido
def admin_categoria_agregar():
    """Formulario para agregar una nueva categoría."""
    if request.method == "POST":
        form = CategoriaForm.desde_request(request.form)
        if not form.es_valido():
            for error in form.errores:
                flash(error, 'error')
            return render_template("admin/categoria_form.html", accion="Agregar")

        try:
            cat_id = categoria_service.insertar(form.nombre, form.descripcion)
            flash(f"✅ Categoría '{form.nombre}' agregada con éxito.", 'success')
            return redirect(url_for('admin_categorias'))
        except Exception as e:
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                flash(f"❌ Ya existe una categoría con el nombre '{form.nombre}'.", 'error')
            else:
                flash(f"❌ Error al agregar categoría: {e}", 'error')
            return render_template("admin/categoria_form.html", accion="Agregar")

    return render_template("admin/categoria_form.html", accion="Agregar")


@app.route("/admin/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_requerido
def admin_categoria_editar(id):
    """Formulario para editar una categoría existente."""
    categoria = categoria_service.obtener_por_id(id)
    if not categoria:
        flash(f"❌ No se encontró categoría con ID {id}.", 'error')
        return redirect(url_for('admin_categorias'))

    if request.method == "POST":
        form = CategoriaForm.desde_request(request.form)
        if not form.es_valido():
            for error in form.errores:
                flash(error, 'error')
            return render_template("admin/categoria_form.html",
                                   categoria=categoria, accion="Editar")

        try:
            if categoria_service.actualizar(id, form.nombre, form.descripcion):
                flash(f"✅ Categoría '{form.nombre}' actualizada correctamente.", 'success')
            else:
                flash("❌ Error al actualizar la categoría.", 'error')
        except Exception as e:
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                flash(f"❌ Ya existe otra categoría con el nombre '{form.nombre}'.", 'error')
            else:
                flash(f"❌ Error: {e}", 'error')
            return render_template("admin/categoria_form.html",
                                   categoria=categoria, accion="Editar")

        return redirect(url_for('admin_categorias'))

    return render_template("admin/categoria_form.html",
                           categoria=categoria, accion="Editar")


@app.route("/admin/categorias/eliminar/<int:id>", methods=["POST"])
@login_requerido
def admin_categoria_eliminar(id):
    """Elimina una categoría."""
    categoria = categoria_service.obtener_por_id(id)
    nombre = categoria['nombre'] if categoria else f"ID {id}"

    if categoria_service.eliminar(id):
        flash(f"✅ Categoría '{nombre}' eliminada correctamente.", 'success')
    else:
        flash(f"❌ No se pudo eliminar la categoría.", 'error')

    return redirect(url_for('admin_categorias'))


# ============================================
# ADMIN: CRUD VENTAS
# ============================================

@app.route("/admin/ventas")
@login_requerido
def admin_ventas():
    """Lista de ventas registradas."""
    ventas = venta_service.obtener_todas()
    return render_template("admin/ventas.html", ventas=ventas)


@app.route("/admin/ventas/registrar", methods=["GET", "POST"])
@login_requerido
def admin_venta_registrar():
    """Formulario para registrar una nueva venta."""
    productos = producto_service.obtener_todos()

    if request.method == "POST":
        form = VentaForm.desde_request(request.form)
        if not form.es_valido():
            for error in form.errores:
                flash(error, 'error')
            return render_template("admin/venta_form.html", productos=productos)

        # Obtener precio del producto
        producto = producto_service.obtener_por_id(form.id_producto)
        if not producto:
            flash("❌ El producto seleccionado no existe.", 'error')
            return render_template("admin/venta_form.html", productos=productos)

        venta_id = venta_service.registrar(
            form.id_producto, form.cliente_nombre, form.cliente_email,
            form.cantidad, producto['precio']
        )

        if venta_id:
            total = producto['precio'] * form.cantidad
            flash(f"✅ Venta registrada (ID: {venta_id}). Total: ${total:.2f}", 'success')
            return redirect(url_for('admin_ventas'))
        else:
            flash("❌ Stock insuficiente para realizar esta venta.", 'error')
            return render_template("admin/venta_form.html", productos=productos)

    return render_template("admin/venta_form.html", productos=productos)


@app.route("/admin/ventas/eliminar/<int:id>", methods=["POST"])
@login_requerido
def admin_venta_eliminar(id):
    """Elimina una venta."""
    if venta_service.eliminar(id):
        flash("✅ Venta eliminada correctamente.", 'success')
    else:
        flash("❌ No se pudo eliminar la venta.", 'error')
    return redirect(url_for('admin_ventas'))


# ============================================
# REPORTES PDF
# ============================================

@app.route("/admin/reporte/productos")
@login_requerido
def reporte_productos():
    """Genera un PDF con el listado de productos."""
    productos = producto_service.obtener_todos()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Encabezado
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 15, 'TechByte - Reporte de Productos', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)

    # Tabla de productos
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(102, 126, 234)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(15, 8, 'ID', border=1, fill=True, align='C')
    pdf.cell(50, 8, 'Nombre', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'Categoria', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'Precio', border=1, fill=True, align='C')
    pdf.cell(20, 8, 'Stock', border=1, fill=True, align='C')
    pdf.cell(45, 8, 'Descripcion', border=1, fill=True, align='C', new_x="LMARGIN", new_y="NEXT")

    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(0, 0, 0)
    fill = False
    for p in productos:
        if fill:
            pdf.set_fill_color(240, 244, 255)
        else:
            pdf.set_fill_color(255, 255, 255)

        nombre = str(p['nombre'])[:25]
        cat = str(p.get('categoria_nombre', ''))[:18]
        desc = str(p.get('descripcion', ''))[:25]

        pdf.cell(15, 7, str(p['id']), border=1, fill=True, align='C')
        pdf.cell(50, 7, nombre, border=1, fill=True)
        pdf.cell(35, 7, cat, border=1, fill=True)
        pdf.cell(25, 7, f"${p['precio']:.2f}", border=1, fill=True, align='R')
        pdf.cell(20, 7, str(p['stock']), border=1, fill=True, align='C')
        pdf.cell(45, 7, desc, border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
        fill = not fill

    # Total
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 8, f'Total de productos: {len(productos)}', new_x="LMARGIN", new_y="NEXT")

    # Generar respuesta
    pdf_output = bytes(pdf.output())
    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_productos.pdf'
    return response


@app.route("/admin/reporte/ventas")
@login_requerido
def reporte_ventas():
    """Genera un PDF con el listado de ventas."""
    ventas = venta_service.obtener_todas()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Encabezado
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 15, 'TechByte - Reporte de Ventas', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 8, f'Generado: {datetime.now().strftime("%d/%m/%Y %H:%M")}', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)

    # Tabla de ventas
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(102, 126, 234)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(15, 8, 'ID', border=1, fill=True, align='C')
    pdf.cell(40, 8, 'Producto', border=1, fill=True, align='C')
    pdf.cell(40, 8, 'Cliente', border=1, fill=True, align='C')
    pdf.cell(20, 8, 'Cant.', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'Precio U.', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'Total', border=1, fill=True, align='C')
    pdf.cell(25, 8, 'Fecha', border=1, fill=True, align='C', new_x="LMARGIN", new_y="NEXT")

    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(0, 0, 0)
    total_general = 0
    fill = False
    for v in ventas:
        if fill:
            pdf.set_fill_color(240, 244, 255)
        else:
            pdf.set_fill_color(255, 255, 255)

        producto_n = str(v.get('producto_nombre', ''))[:20]
        cliente_n = str(v.get('cliente_nombre', ''))[:20]
        fecha_str = ''
        if v.get('fecha'):
            try:
                fecha_str = v['fecha'].strftime('%d/%m/%Y')
            except AttributeError:
                fecha_str = str(v['fecha'])[:10]

        pdf.cell(15, 7, str(v['id']), border=1, fill=True, align='C')
        pdf.cell(40, 7, producto_n, border=1, fill=True)
        pdf.cell(40, 7, cliente_n, border=1, fill=True)
        pdf.cell(20, 7, str(v['cantidad']), border=1, fill=True, align='C')
        pdf.cell(25, 7, f"${v['precio_unitario']:.2f}", border=1, fill=True, align='R')
        pdf.cell(25, 7, f"${v['total']:.2f}", border=1, fill=True, align='R')
        pdf.cell(25, 7, fecha_str, border=1, fill=True, align='C', new_x="LMARGIN", new_y="NEXT")
        total_general += v['total']
        fill = not fill

    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(0, 8, f'Total de ventas: {len(ventas)}  |  Ingresos totales: ${total_general:.2f}',
             new_x="LMARGIN", new_y="NEXT")

    pdf_output = bytes(pdf.output())
    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_ventas.pdf'
    return response


# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    app.run(debug=True)
