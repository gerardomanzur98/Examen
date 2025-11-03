# Monitoreo del Sistema con Django y Psutil

## Descripción del Proyecto
Esta aplicación web utiliza Django para crear una interfaz sencilla que monitorea el estado del sistema en tiempo real. Emplea la librería psutil para recolectar datos como uso de CPU, RAM, disco y información del sistema operativo. La interfaz permite actualización manual con un botón y opcional automática con JavaScript.

## Instrucciones para Ejecutar el Proyecto Localmente
1. Clona o descarga el proyecto.
2. Instala las dependencias: `pip install -r requirements.txt`.
3. Ejecuta las migraciones (aunque no hay modelos): `python manage.py migrate`.
4. Inicia el servidor: `python manage.py runserver`.
5. Abre tu navegador en `http://127.0.0.1:8000/` para ver la página principal.

## Dependencias
- Django: Framework web para Python.
- Psutil: Librería externa para monitoreo de recursos del sistema. Instálala con `pip install psutil`.

## Componentes Principales
- **Vistas (views.py)**: La función `index` recolecta datos con `get_system_info()` y los pasa a la plantilla. Maneja errores para robustez.
- **Plantillas (index.html)**: Interfaz web con tarjetas Bootstrap para mostrar datos estructurados. Incluye botón de actualización y JS opcional para recarga automática.
- **Lógica de Recolección**: Funciones en Python que usan psutil para obtener métricas del sistema, con validación de errores.

## Notas
- Asegúrate de que psutil tenga permisos para acceder a datos del sistema.
