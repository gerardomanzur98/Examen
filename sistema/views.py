import psutil
import platform
from django.shortcuts import render

def get_system_info():
    """
    Función para recolectar información del sistema usando psutil.
    Maneja errores y devuelve datos estructurados.
    """
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)  # Porcentaje de uso del CPU
        
        # RAM
        ram = psutil.virtual_memory()
        ram_used_gb = round(ram.used / (1024**3), 2)  # Usado en GB
        ram_total_gb = round(ram.total / (1024**3), 2)  # Total en GB
        ram_percent = ram.percent  # Porcentaje
        
        # Disco (usando la raíz del sistema)
        disk = psutil.disk_usage('/')
        disk_used_gb = round(disk.used / (1024**3), 2)
        disk_free_gb = round(disk.free / (1024**3), 2)
        disk_total_gb = round(disk.total / (1024**3), 2)
        
        # Información del sistema operativo y CPU
        os_info = platform.uname()
        os_name = os_info.system + " " + os_info.release  # Ej: Windows 10 o Linux 6.8
        cores = psutil.cpu_count(logical=True)  # Número de núcleos lógicos
        
        return {
            'cpu_percent': cpu_percent,
            'ram_used_gb': ram_used_gb,
            'ram_total_gb': ram_total_gb,
            'ram_percent': ram_percent,
            'disk_used_gb': disk_used_gb,
            'disk_free_gb': disk_free_gb,
            'disk_total_gb': disk_total_gb,
            'os_name': os_name,
            'cores': cores,
            'error': None
        }
    except Exception as e:
        return {
            'error': f"Error al obtener datos del sistema: {str(e)}"
        }

def index(request):
    """
    Vista principal que recolecta datos y los pasa a la plantilla.
    """
    data = get_system_info()
    return render(request, 'sistema/index.html', {'data': data})
