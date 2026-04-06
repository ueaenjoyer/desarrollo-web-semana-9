# 🛒 TechByte - Proyecto Final Desarrollo Web

**Sistema web transaccional completo, estructurado bajo el patrón MVC, desplegado en la nube e interconectado con una base de datos relacional.**

Este proyecto representa la entrega de la **Semana Final** de nuestra asignatura, cumpliendo al 100% con los requerimientos técnicos y funcionales solicitados en la rúbrica de evaluación.

---

## 👥 Equipo de Desarrollo

*   **Paul** (Desarrollador Backend / Arquitectura de Software)
*   **Noelia** (Backend / QA Funcionalidad)
*   **Marleyth** (Frontend / Exposición)
*   **John** *(Nota: Nuestro compañero John colaboró en el desarrollo del código como evidencian nuestras sesiones, pero no pudo salir en la grabación del video por calamidades domésticas).*

---

## 🚀 Entregables Principales

Para facilitar la revisión por parte del docente, adjuntamos a continuación los enlaces cruciales del proyecto. Al haber utilizado un enfoque práctico y profesional, **la aplicación web ya se encuentra probada y desplegada en un entorno real.**

### 1. Sistema en Vivo (Producción)
🌐 **[Acceso a la plataforma en vivo - Render (Clic aquí)](https://desarrollo-web-semana-9.onrender.com/)**

Para verificar el cumplimiento del ecosistema interno (Auth y CRUD), por favor ingrese a la ruta de `/login` o haga clic en el botón superior derecho de "Admin" utilizando nuestras credenciales protegidas de acceso universal:

*   **Usuario:** `admin@techbyte.com`
*   **Contraseña:** `admin123`

### 2. Video de Sustentación Grupal (Opción Alternativa de Defensa)
Hemos preparado y subido a la red la grabación de la demostración guiada del sistema y la revisión de requisitos:

🎥 **[Videodemostración del Proyecto en YouTube](https://youtu.be/v2u3WZ0GZls)**

---

## 🎯 Cumplimiento de la Rúbrica de Evaluación

En este aplicativo, las funcionalidades solicitadas fueron implementadas satisfactoriamente de la siguiente forma:

| Requerimiento Solicitado | Cumplimiento e Implementación Técnica en TechByte |
| :--- | :--- |
| **🔐 Sistema de login** | **Validado.** Se protege el Panel Administrativo (MVC: Carpeta `templates/admin/`) con restricción de Flask (`@login_requerido`). Las contraseñas del administrador jamás viajan solas, están hasheadas vía *Werkzeug Security*. |
| **🗂️ Operaciones CRUD** | **Validado.** Control y creación, lectura, actualización y eliminación de los objetos virtuales `Productos` (con foto, precio, descripción) y las `Categorías` (tipo computo). Las entidades se blindan usando *Forms*. |
| **🧩 3 Tablas Relacionadas** | **Completamente Validado (Tenemos 4).** Diseñamos un core relacional duro sobre **PostgreSQL (Supabase)**. Tenemos la tabla `Usuarios` (Login), y las tablas interconectadas para soportar la lógica de negocio real (`Categorías → Productos → Ventas`). Si intentas generar una Venta, nuestra lógica transaccional descuenta automáticamente el 'stock' que el Producto provee utilizando `FOREIGN KEYS`. |
| **☁️ Despliegue en la Nube** | **Validado Extras.** La inicialización la programamos para evitar el bloqueo Gunicorn sobre la nube de Render (separando en script `init_db.py`). |

---

## 🧑‍💻 Evidencia de Trabajo Colaborativo (Pair Programming)

El desarrollo del Backend, la programación del enrutamiento y la maquetación del diseño se realizaron a través de mecánicas de programación en pares y lluvia de ideas a distancia.

<div align="center">
  <img src="https://i.ibb.co/HpCMKxYX/Whats-App-Image-2026-04-05-at-8-13-59-PM-1.jpg" width="45%" alt="Evidencia Pair Programming 1">
  <img src="https://i.ibb.co/bMXGjPHw/Whats-App-Image-2026-04-05-at-8-13-27-PM.jpg" width="45%" alt="Evidencia Pair Programming 2">
</div>
