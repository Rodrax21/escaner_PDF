# logic/AutoUpdater.py

import requests
import os
import sys
import tempfile
import subprocess
from PyQt5.QtWidgets import QMessageBox

# Versión actual del programa
__version__ = "v1.0.0"  # Se actualizará automáticamente en el flujo de trabajo de GitHub

GITHUB_USER = "Rodrax21"
GITHUB_REPO = "escaner_PDF"

def obtener_ultima_version():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["tag_name"], data["assets"]
    except Exception as e:
        QMessageBox.critical(None, f"Error al intentar actualizar el programa", f"No se pudo comprobar la ultima versión:\n{str(e)}")
        print(f"Error al consultar actualizaciones: {e}")
        return None, None

def hay_actualizacion_disponible():
    ultima_version, _ = obtener_ultima_version()
    if ultima_version is None:
        return False
    return ultima_version != __version__

def descargar_instalador(assets):
    for asset in assets:
        nombre = asset["name"]
        url = asset["browser_download_url"]
        if nombre.endswith(".exe") and "Scanner" in nombre:
            print(f"Descargando instalador desde: {url}")
            temp_dir = tempfile.gettempdir()
            ruta_destino = os.path.join(temp_dir, nombre)
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(ruta_destino, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return ruta_destino
    return None

def ejecutar_instalador_y_salir(instalador_path):
    try:
        subprocess.Popen([instalador_path], shell=True)
        sys.exit()  # Cierra la aplicación actual
    except Exception as e:
        print(f"Error al ejecutar el instalador: {e}")

def comprobar_actualizaciones(parent=None):
    ultima_version, assets = obtener_ultima_version()
    if ultima_version is None or assets is None:
        QMessageBox.warning(parent, "Actualización", "No se pudo comprobar si hay una nueva versión.")
        return

    if ultima_version != __version__:
        respuesta = QMessageBox.question(
            parent,
            "Actualización disponible",
            f"Hay una nueva versión disponible ({ultima_version}). ¿Deseás descargarla ahora?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            ruta = descargar_instalador(assets)
            if ruta:
                ejecutar_instalador_y_salir(ruta)
            else:
                QMessageBox.critical(parent, "Error", "No se pudo descargar el instalador.")
    else:
        QMessageBox.information(parent, "Actualización", "Ya tenés la última versión.")
