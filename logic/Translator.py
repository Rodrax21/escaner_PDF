import json
from PyQt5.QtCore import QFile, QTextStream
from logic.ConfigManager import cargar_config, guardar_config

from translations import language

AVAILABLE_LANGUAGES = {}
language_order = []

# Cargar todos los archivos .json de traducciones embebidos
for lang_code in ["en","es"]:  # Podés hacer que esto venga de otro lado si querés
    file = QFile(f":/{lang_code}.json")
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        stream.setCodec("utf-8")
        data = json.loads(stream.readAll())
        AVAILABLE_LANGUAGES[lang_code] = data
        language_order.append(lang_code)
    file.close()

# Cargar idioma actual desde config
config = cargar_config()
current_index = language_order.index(config.get("idioma", "en")) if config.get("idioma") in language_order else 0
T = AVAILABLE_LANGUAGES[language_order[current_index]]

def get_translation(clave):
    return T.get(clave, clave)

def cycle_language():
    global current_index, T
    print(f"Cambiando idioma: {language_order[current_index]}")

    current_index = (current_index + 1) % len(language_order)
    print(f"Nuevo idioma: {language_order[current_index]}")

    nuevo_idioma = language_order[current_index]
    T = AVAILABLE_LANGUAGES[language_order[current_index]]

    print("Antonio")
    guardar_config({"idioma": nuevo_idioma})
    print(f"Idioma guardado en config: {nuevo_idioma}")
    return nuevo_idioma