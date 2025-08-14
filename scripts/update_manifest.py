import os
import sys
import json
import hashlib
from pathlib import Path

# Ruta absoluta al directorio raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = os.path.join(Path(__file__).resolve().parent.parent, "manifest.json")

# Carpetas y extensiones a excluir
EXCLUDED_DIRS = {".git", "__pycache__", "build", "dist"}
EXCLUDED_EXTENSIONS = {".spec", ".pyc", ".pyo", ".tmp"}

def md5(fname):
    """Calcula el hash MD5 de un archivo."""
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_all_files():
    """Obtiene todos los archivos del proyecto excluyendo los no relevantes."""
    files = []
    for root, dirs, filenames in os.walk(ROOT_DIR):
        # Excluir carpetas no deseadas
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for filename in filenames:
            path = Path(root) / filename
            # Excluir extensiones no deseadas
            if path.suffix.lower() in EXCLUDED_EXTENSIONS:
                continue
            files.append(path)
    return files

def update_manifest(new_version=None):
    """Actualiza o crea el manifest.json con la versión y los hashes."""
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    else:
        manifest = {"version": "", "files": {}}

    all_files = get_all_files()
    for path in all_files:
        relative_path = str(path.relative_to(ROOT_DIR))
        manifest["files"][relative_path] = md5(path)

    if new_version:
        manifest["version"] = new_version
    elif not manifest.get("version"):
        manifest["version"] = "1.0.0"

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    print(f"Manifest actualizado en {MANIFEST_PATH}")
    print(f"Versión: {manifest['version']}")
    print(f"Archivos: {len(manifest['files'])}")

if __name__ == "__main__":
    version_arg = sys.argv[1] if len(sys.argv) > 1 else None
    update_manifest(version_arg)
