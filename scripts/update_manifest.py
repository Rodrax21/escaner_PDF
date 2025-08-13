import os
import sys
import json
import hashlib
from pathlib import Path
import subprocess

MANIFEST_PATH = "manifest.json"

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_changed_files():
    # Devuelve lista de archivos modificados en el último commit
    result = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], capture_output=True, text=True)
    files = result.stdout.strip().splitlines()
    # Filtrar solo archivos que queremos versionar (por ejemplo .pyc, .py, .ico, etc.)
    files = [f for f in files if os.path.isfile(f)]
    return files

def update_manifest(new_version=None):
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    else:
        manifest = {"version": "", "files": {}}

    changed_files = get_changed_files()
    for path in changed_files:
        manifest["files"][path] = md5(path)

    if new_version:
        manifest["version"] = new_version
    elif not manifest.get("version"):
        manifest["version"] = "1.0.0"

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)
    print("Manifest actualizado:", manifest)

if __name__ == "__main__":
    version_arg = sys.argv[1] if len(sys.argv) > 1 else None
    update_manifest(version_arg)
