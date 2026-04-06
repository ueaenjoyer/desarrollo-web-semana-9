# ============================================
# init_db.py - Inicialización manual de tablas
# ============================================
# Ejecuta este script localmente si necesitas 
# crear las tablas en tu base de datos Supabase
# por primera vez.
# ============================================

from services import categoria_service, producto_service, venta_service, usuario_service

def inicializar():
    print("⏳ Iniciando la creación de tablas en Supabase...\n")
    
    try:
        categoria_service.init_tabla()
        print("✅ Tabla 'categorias' y datos por defecto inicializados correctamente.")
        
        producto_service.init_tabla()
        print("✅ Tabla 'productos' inicializada correctamente.")
        
        usuario_service.init_tabla()
        print("✅ Tabla 'usuarios' y usuario admin configurado.")
        
        venta_service.init_tabla()
        print("✅ Tabla 'ventas' inicializada correctamente.")
        
        print("\n🎉 ¡Inicialización completada con éxito!")
    except Exception as e:
        print(f"\n❌ Ocurrió un error general: {e}")

if __name__ == "__main__":
    inicializar()
