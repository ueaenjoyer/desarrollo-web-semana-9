# ============================================
# MENÚ INTERACTIVO EN CONSOLA (CLI)
# Semana 11 - Sistema Avanzado de Gestión de Inventario
# TechByte - Tienda de Gadgets
# ============================================
# Este script permite gestionar el inventario desde la terminal.
# Utiliza las clases Producto e Inventario definidas en models.py.
# ============================================

from models import Inventario, Producto, DatabaseManager


def mostrar_menu():
    """Muestra el menú principal de opciones."""
    print("\n" + "=" * 55)
    print("  🛒 TechByte - Sistema de Gestión de Inventario")
    print("=" * 55)
    print("  1. 📋 Mostrar todos los productos")
    print("  2. ➕ Agregar nuevo producto")
    print("  3. ✏️  Actualizar producto")
    print("  4. ❌ Eliminar producto")
    print("  5. 🔍 Buscar producto por nombre")
    print("  6. 📊 Ver estadísticas del inventario")
    print("  0. 🚪 Salir")
    print("=" * 55)


def mostrar_productos(productos):
    """
    Muestra una LISTA de productos en formato tabla.

    Args:
        productos (list): Lista de diccionarios con datos de productos.
    """
    if not productos:
        print("\n  ⚠️  No hay productos en el inventario.")
        return

    print(f"\n  {'ID':<5} {'Nombre':<25} {'Categoría':<15} {'Precio':<12} {'Cantidad':<10}")
    print("  " + "-" * 67)
    for p in productos:
        print(f"  {p['id']:<5} {p['nombre']:<25} {p['categoria']:<15} ${p['precio']:<11.2f} {p['cantidad']:<10}")

    print(f"\n  Total: {len(productos)} producto(s)")


def agregar_producto(inventario):
    """
    Solicita datos al usuario y agrega un producto al inventario.
    Usa la TUPLA Producto.CATEGORIAS_VALIDAS para mostrar opciones válidas.
    """
    print("\n  ➕ AGREGAR NUEVO PRODUCTO")
    print("  " + "-" * 30)

    nombre = input("  Nombre: ").strip()
    if not nombre:
        print("  ❌ El nombre no puede estar vacío.")
        return

    # Mostramos las categorías disponibles desde la TUPLA inmutable
    print("\n  Categorías disponibles:")
    for i, cat in enumerate(Producto.CATEGORIAS_VALIDAS, 1):
        print(f"    {i}. {cat}")

    try:
        opcion_cat = int(input("  Seleccione categoría (número): "))
        if 1 <= opcion_cat <= len(Producto.CATEGORIAS_VALIDAS):
            categoria = Producto.CATEGORIAS_VALIDAS[opcion_cat - 1]
        else:
            categoria = "Otros"
    except ValueError:
        categoria = "Otros"

    try:
        precio = float(input("  Precio ($): "))
    except ValueError:
        print("  ❌ Precio inválido.")
        return

    try:
        cantidad = int(input("  Cantidad: "))
    except ValueError:
        print("  ❌ Cantidad inválida.")
        return

    descripcion = input("  Descripción: ").strip()

    producto = inventario.agregar(nombre, categoria, precio, cantidad, descripcion)
    print(f"\n  ✅ Producto '{producto.nombre}' agregado con ID {producto.id}")


def actualizar_producto(inventario):
    """Solicita ID y nuevos datos para actualizar un producto."""
    print("\n  ✏️  ACTUALIZAR PRODUCTO")
    print("  " + "-" * 30)

    try:
        producto_id = int(input("  ID del producto a actualizar: "))
    except ValueError:
        print("  ❌ ID inválido.")
        return

    # Búsqueda O(1) en el DICCIONARIO del inventario
    producto = inventario.obtener_por_id(producto_id)
    if not producto:
        print(f"  ❌ No se encontró producto con ID {producto_id}")
        return

    print(f"  Producto actual: {producto['nombre']} | {producto['categoria']} | "
          f"${producto['precio']:.2f} | Cant: {producto['cantidad']}")
    print("  (Deje vacío para mantener el valor actual)")

    nombre = input(f"  Nuevo nombre [{producto['nombre']}]: ").strip()
    nombre = nombre if nombre else producto['nombre']

    # Mostrar categorías de la TUPLA
    print("\n  Categorías disponibles:")
    for i, cat in enumerate(Producto.CATEGORIAS_VALIDAS, 1):
        print(f"    {i}. {cat}")
    cat_input = input(f"  Nueva categoría [{producto['categoria']}]: ").strip()
    try:
        cat_num = int(cat_input)
        categoria = Producto.CATEGORIAS_VALIDAS[cat_num - 1] if 1 <= cat_num <= len(Producto.CATEGORIAS_VALIDAS) else producto['categoria']
    except (ValueError, IndexError):
        categoria = producto['categoria'] if not cat_input else cat_input

    precio_input = input(f"  Nuevo precio [{producto['precio']}]: ").strip()
    try:
        precio = float(precio_input) if precio_input else producto['precio']
    except ValueError:
        precio = producto['precio']

    cant_input = input(f"  Nueva cantidad [{producto['cantidad']}]: ").strip()
    try:
        cantidad = int(cant_input) if cant_input else producto['cantidad']
    except ValueError:
        cantidad = producto['cantidad']

    descripcion = input(f"  Nueva descripción [{producto['descripcion']}]: ").strip()
    descripcion = descripcion if descripcion else producto['descripcion']

    if inventario.actualizar(producto_id, nombre, categoria, precio, cantidad, descripcion):
        print(f"\n  ✅ Producto ID {producto_id} actualizado correctamente.")
    else:
        print("  ❌ Error al actualizar el producto.")


def eliminar_producto(inventario):
    """Solicita ID y elimina un producto del inventario."""
    print("\n  ❌ ELIMINAR PRODUCTO")
    print("  " + "-" * 30)

    try:
        producto_id = int(input("  ID del producto a eliminar: "))
    except ValueError:
        print("  ❌ ID inválido.")
        return

    producto = inventario.obtener_por_id(producto_id)
    if not producto:
        print(f"  ❌ No se encontró producto con ID {producto_id}")
        return

    confirmar = input(f"  ¿Eliminar '{producto['nombre']}'? (s/n): ").strip().lower()
    if confirmar == 's':
        if inventario.eliminar(producto_id):
            print(f"  ✅ Producto '{producto['nombre']}' eliminado correctamente.")
        else:
            print("  ❌ Error al eliminar el producto.")
    else:
        print("  ℹ️  Operación cancelada.")


def buscar_producto(inventario):
    """Busca productos por nombre y muestra los resultados."""
    print("\n  🔍 BUSCAR PRODUCTO")
    print("  " + "-" * 30)

    termino = input("  Buscar por nombre: ").strip()
    if not termino:
        print("  ❌ Debe ingresar un término de búsqueda.")
        return

    # La búsqueda retorna una LISTA de diccionarios
    resultados = inventario.buscar_por_nombre(termino)
    print(f"\n  Resultados para '{termino}':")
    mostrar_productos(resultados)


def ver_estadisticas(inventario):
    """Muestra estadísticas generales del inventario usando colecciones."""
    print("\n  📊 ESTADÍSTICAS DEL INVENTARIO")
    print("  " + "-" * 40)

    stats = inventario.obtener_estadisticas()

    print(f"  Total de productos: {stats['total_productos']}")
    print(f"  Total de unidades:  {stats['total_unidades']}")
    print(f"  Valor total:        ${stats['valor_total']:.2f}")

    # LISTA ordenada de categorías activas (convertida desde CONJUNTO)
    if stats['categorias_activas']:
        print(f"  Categorías activas: {', '.join(stats['categorias_activas'])}")

    if stats['producto_mas_caro']:
        mc = stats['producto_mas_caro']
        print(f"  Producto más caro:  {mc['nombre']} (${mc['precio']:.2f})")

    if stats['producto_mas_barato']:
        mb = stats['producto_mas_barato']
        print(f"  Producto más barato: {mb['nombre']} (${mb['precio']:.2f})")


def main():
    """Función principal que ejecuta el menú interactivo."""
    print("\n  🚀 Iniciando sistema de inventario TechByte...")

    # Inicializamos la base de datos y el inventario
    db = DatabaseManager()
    inventario = Inventario(db)

    while True:
        mostrar_menu()
        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            # mostrar_todos() retorna una LISTA de diccionarios
            productos = inventario.mostrar_todos()
            mostrar_productos(productos)
        elif opcion == "2":
            agregar_producto(inventario)
        elif opcion == "3":
            actualizar_producto(inventario)
        elif opcion == "4":
            eliminar_producto(inventario)
        elif opcion == "5":
            buscar_producto(inventario)
        elif opcion == "6":
            ver_estadisticas(inventario)
        elif opcion == "0":
            print("\n  👋 ¡Hasta luego! Gracias por usar TechByte.")
            break
        else:
            print("  ⚠️  Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
