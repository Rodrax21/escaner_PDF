import os
import sys
import hashlib
import shutil
import json
import subprocess
import urllib.request
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
from logic.Translator import get_translation as T

# URL directa al manifest del último release en GitHub
MANIFEST_URL = "https://raw.githubusercontent.com/Rodrax21/escaner_PDF/main/manifest.json"
APP_EXE_NAME = "PDF Scanner v1.exe"
BACKUP_DIR = "backup_launcher"

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def archivos_a_actualizar(install_dir, manifest):
    archivos_a_descargar = []
    for path, hash_esperado in manifest.get("files", {}).items():
        local_path = os.path.join(install_dir, path)
        if not os.path.exists(local_path) or md5(local_path) != hash_esperado:
            archivos_a_descargar.append(path)
    return archivos_a_descargar

def descargar_archivo(url, local_path):
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with urllib.request.urlopen(url, timeout=30) as response:
            with open(local_path, "wb") as f:
                shutil.copyfileobj(response, f)
        print(f"Actualizado: {local_path}")
        return True
    except Exception as e:
        print(f"Error descargando {url}: {e}")
        return False

def actualizar_archivos(install_dir, archivos):
    backup_path = os.path.join(install_dir, BACKUP_DIR)
    os.makedirs(backup_path, exist_ok=True)

    for path in archivos:
        url = f"https://raw.githubusercontent.com/Rodrax21/escaner_PDF/main/{path}"
        local_path = os.path.join(install_dir, path)

        # Respaldo del archivo actual
        if os.path.exists(local_path):
            rel_path = os.path.relpath(local_path, install_dir)
            backup_file = os.path.join(backup_path, rel_path)
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            shutil.copy2(local_path, backup_file)

        # Descargar y reemplazar
        if not descargar_archivo(url, local_path):
            print(f"No se pudo actualizar {path}. Se mantiene la versión anterior.")

def ejecutar_app(install_dir):
    exe_path = os.path.join(install_dir, APP_EXE_NAME)
    if os.path.exists(exe_path):
        try:
            subprocess.Popen([exe_path])
        except Exception as e:
            print(f"No se pudo ejecutar {APP_EXE_NAME}: {e}")
    else:
        print(f"No se encontró {APP_EXE_NAME} en {install_dir}")

def main():
    install_dir = Path(sys.executable).parent

    # Descargar manifest
    try:
        with urllib.request.urlopen(MANIFEST_URL, timeout=30) as response:
            manifest = json.load(response)
    except Exception as e:
        print("Error descargando manifest:", e)
        ejecutar_app(install_dir)
        return

    # Verificar archivos a actualizar
    archivos = archivos_a_actualizar(install_dir, manifest)
    if archivos:
        ultima_version = manifest.get("version", "desconocida")
        respuesta = QMessageBox.question(
            None,
            T("AU_question_a"),
            f"{T('AU_question_b')} ({ultima_version}). {T('AU_question_c')}",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            print("Archivos a actualizar:", archivos)
            actualizar_archivos(install_dir, archivos)
    else:
        print("Todo actualizado")

    # Ejecutar la app principal
    ejecutar_app(install_dir)

if __name__ == "__main__":
    main()
