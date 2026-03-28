# 🚀 Guía de Despliegue - TechByte (Semana 15)

Este documento describe cómo desplegar el proyecto TechByte de manera profesional utilizando un proveedor en la nube compatible con contenedores Python/WSGI, como **Render**, apoyado por una base de datos relacional externa alojada en **Supabase**.

## 1. Preparación de la Base de Datos (Supabase)

Supabase aloja la instancia central de **PostgreSQL** para la aplicación.
1.  Ingresa a [Supabase](https://supabase.com) y crea un proyecto gratuito.
2.  Al inicializarse el proyecto, dirígete a **Project Settings -> Database** (Configuración -> Base de datos).
3.  Copia y reserva el enlace **Connection string (URI)**. Usualmente tiene este formato:
    ```
    postgresql://postgres.nombredelproyecto:[CONTRASEÑA]@aws-0-region-pooler.supabase.com:6543/postgres?sslmode=require
    ```

**Nota sobre Migraciones:** La función `init_tabla()` interna del código en `app.py` gestionará automáticamente la creación de las tablas relacionales (`categorias`, `productos`, `ventas`, `usuarios`) y generará el administrador primario (`admin@techbyte.com` / `admin123`).

## 2. GitHub (Versión de Control)

1.  Asegúrate de haber resuelto los cambios finales.
2.  Verifica que tu archivo `.gitignore` prohíbe explícitamente la distribución de metadatos confidenciales en la nube subiendo la línea `.env`.
3.  Sube y sube los cambios (Commit + Push) de toda la carpeta `proyecto_Paul_TiendaGadget` a un repositorio remoto de GitHub.

## 3. Despliegue en Render (App Web Flask)

Ocuparemos Render dado su tier gratuito sin tarjetas.

1.  Procede a registrar o iniciar sesión en [Render.com](https://render.com).
2.  Desplázate al marco conceptual en la parte superior derecha y dale a **New -> Web Service**.
3.  Conecta u otorga los permisos para tu cuenta GitHub y busca el repositorio expuesto. Clic en **Connect**.
4.  Llene la información de la siguiente forma:
    *   **Name:** `techbyte-semana15-deploy` (o el nombre deseado)
    *   **Region:** La más cerca a tu país.
    *   **Branch:** `main` (o dependiendo cómo este designada la raíz en GitHub)
    *   **Root Directory:** El caso lo amerita si el archivo `app.py` está inserto dentro de una subcarpeta (ej. `proyecto_Paul_TiendaGadget`). De ser la raíz literal de todo GitHub, déje esto nulo o vacío.
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt` (Aquí se descargará Flask, psycopg2 y fpdf2).
    *   **Start Command:** `gunicorn app:app`

## 4. Variables de Entorno (Environment Variables)

Este es el paso vital. Si falla esto, devolverá error 500 al arrancar ya que intentará buscar bases inexistentes.

*   En la misma configuración de Render (una vez se seleccione a "Web Service"), baja hacia **Environment Variables**.
*   Añade y compila un variable designada `DATABASE_URL`. Pega allí toda la Connection string de su base de Supabase (el enlace extenso con SSL configurado).
*   Recomendable: Añade una nueva directiva nombrada `SECRET_KEY` en donde adjudicas una oración larga y compleja, para proteger encriptaciones y sesiones Flask en el servidor de producción.

## 5. Lanzar y Visualizar

1.  Clic a la opción verde **"Create Web Service"**. Render construirá iteraciones instalando todas las librerías desde el archivo en `requirements.txt`.
2.  Una vez marcado con ✅ Live. Ve al enlace autogenerado emitido en la parte superior izquierda (ejemplo: `techbyte-deploy-h1k5.onrender.com`).
3.  Pruebe su catálogo o inicie al dashboard. Los reportes PDF (FPDF2) no necesitan instalaciones subyacentes ya que el motor usa la RAM transitoriamente para generar la descarga.
