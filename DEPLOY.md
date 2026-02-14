# Guía de Despliegue en Render 🚀

Esta guía te ayudará a desplegar tu aplicación TechByte en Render.

## Paso 1: Preparar el Repositorio en GitHub

1. **Inicializa Git** (si no lo has hecho):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: TechByte Flask app"
   ```

2. **Crea un repositorio en GitHub**:
   - Ve a [github.com](https://github.com) y crea un nuevo repositorio
   - Nómbralo `proyecto-techbyte` o similar

3. **Sube tu código**:
   ```bash
   git remote add origin https://github.com/TU_USUARIO/proyecto-techbyte.git
   git branch -M main
   git push -u origin main
   ```

## Paso 2: Configurar Render

1. **Crea una cuenta** en [render.com](https://render.com) (gratis)

2. **Conecta GitHub**:
   - En el dashboard de Render, haz clic en "New +"
   - Selecciona "Web Service"
   - Conecta tu cuenta de GitHub
   - Autoriza a Render para acceder a tus repositorios

3. **Selecciona tu repositorio**:
   - Busca `proyecto-techbyte`
   - Haz clic en "Connect"

## Paso 3: Configuración del Servicio

Completa los siguientes campos:

| Campo | Valor |
|-------|-------|
| **Name** | `techbyte-tienda` (o el nombre que prefieras) |
| **Region** | Selecciona la más cercana (ej: Oregon) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Configuración Avanzada (Opcional)

- **Instance Type**: Free (para empezar)
- **Environment Variables**: No necesitas ninguna por ahora

## Paso 4: Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a:
   - Clonar tu repositorio
   - Instalar dependencias
   - Iniciar tu aplicación

3. **Espera 2-3 minutos** mientras se despliega

## Paso 5: Verificar

1. Una vez completado, Render te dará una URL como:
   ```
   https://techbyte-tienda.onrender.com
   ```

2. **Abre esa URL** en tu navegador
3. ¡Deberías ver tu aplicación TechByte funcionando! 🎉

## 🔄 Actualizaciones Automáticas

Cada vez que hagas `git push` a tu repositorio, Render automáticamente:
- Detectará los cambios
- Reconstruirá la aplicación
- Desplegará la nueva versión

## ⚠️ Notas Importantes

### Plan Gratuito de Render
- Tu app se "dormirá" después de 15 minutos de inactividad
- La primera carga después de dormir puede tardar 30-60 segundos
- Esto es normal en el plan gratuito

### Si hay Errores
1. Revisa los **logs** en el dashboard de Render
2. Verifica que `requirements.txt` esté actualizado
3. Asegúrate de que `gunicorn` esté en `requirements.txt`

## 🎯 Checklist de Despliegue

- [ ] Código subido a GitHub
- [ ] Cuenta creada en Render
- [ ] Repositorio conectado
- [ ] Configuración completada
- [ ] Aplicación desplegada
- [ ] URL funcionando correctamente

## 🆘 Solución de Problemas

### Error: "Application failed to start"
- Verifica que el comando de inicio sea exactamente: `gunicorn app:app`
- Revisa que `app.py` esté en la raíz del proyecto

### Error: "Module not found"
- Actualiza `requirements.txt`:
  ```bash
  uv pip freeze | Out-File -Encoding utf8 requirements.txt
  git add requirements.txt
  git commit -m "Update requirements"
  git push
  ```

### La página no carga
- Espera 1-2 minutos (el plan gratuito tarda en iniciar)
- Revisa los logs en el dashboard de Render

## 📚 Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Guía de Flask en Render](https://render.com/docs/deploy-flask)

---

**¡Listo!** Tu aplicación TechByte ahora está en la nube y accesible desde cualquier lugar del mundo. 🌍
