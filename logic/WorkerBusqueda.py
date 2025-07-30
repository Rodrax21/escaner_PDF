from PyQt5.QtCore import QObject, pyqtSignal
from pathlib import Path
import fitz  # PyMuPDF
import os
from PyQt5.QtWidgets import QMessageBox

class WorkerBusqueda(QObject):
    terminado = pyqtSignal(object)  # Signal to emit results

    def __init__(self, archivos_pdf, palabras_clave):
        print("Inicializando WorkerBusqueda")

        super().__init__()
        self.archivos_pdf = archivos_pdf

        print("palabras_clave:", palabras_clave)
        print("type:", type(palabras_clave))

        self.palabras_clave = [p.lower() for p in palabras_clave]
        print(f"Palabras clave recibidas: {self.palabras_clave}")
        self.resultados = {}

        print("Worker inicializado con archivos")

    def run(self):
        print("Iniciando búsqueda en PDFs...")
        self.resultados = self.buscar_palabras_en_pdfs()
        print("Búsqueda finalizada, enviando resultados...")
        self.terminado.emit(self.resultados)

    def buscar_palabras_en_pdfs(self):
        resultados = {}

        for ruta_pdf in self.archivos_pdf:
            ruta_archivo = Path(ruta_pdf)
            resultados[ruta_archivo] = {}

            try:
                doc = fitz.open(ruta_pdf)
                for num_pagina, pagina in enumerate(doc, start=1):
                    texto = pagina.get_text().lower()
                    coincidencias = [palabra for palabra in self.palabras_clave if palabra.lower() in texto]

                    if coincidencias:
                        resultados[ruta_archivo][num_pagina] = coincidencias

                doc.close()

            except Exception as e:
                QMessageBox.critical(self, "Error al cargar", f"No se pudo cargar el pdf:\n{str(e)}")


        return resultados

    def obtener_resultados(self):
        return self.resultados
    
    def exportar_resultados(self):
        # Implementar lógica para exportar resultados a un archivo
        pass
