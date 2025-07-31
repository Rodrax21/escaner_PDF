from PyQt5.QtCore import QObject, pyqtSignal
from pathlib import Path
import fitz  # PyMuPDF
import os
import re
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from PyQt5.QtWidgets import QMessageBox

class WorkerBusqueda(QObject):
    volverSignal = pyqtSignal()
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
                    #coincidencias = [
                    #    palabra for palabra in self.palabras_clave
                    #    if re.search(rf'\b{re.escape(palabra.lower())}\b', texto.lower())
                    #] #Evita busquedas parciales

                    if coincidencias:
                        resultados[ruta_archivo][num_pagina] = coincidencias

                doc.close()

            except Exception as e:
                QMessageBox.critical(self, "Error al cargar", f"No se pudo cargar el pdf:\n{str(e)}")


        return resultados

    def obtener_resultados(self):
        return self.resultados
    
    def exportar_resultados(self):
        if not self.resultados:
            QMessageBox.warning(None, "Sin resultados", "No hay resultados para exportar.")
            return

        # Obtener fecha y hora para la carpeta principal
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        base_dir = os.path.join(os.path.expanduser("~"), "Documents", "Extraccion del Escaner PDF", timestamp)
        
        final_dir = base_dir
        counter = 1

        # Bucle para verificar existencia y agregar sufijo incremental
        while os.path.exists(final_dir):
            final_dir = base_dir + f"_{counter}"
            counter += 1

        # Crear la carpeta final
        os.makedirs(final_dir, exist_ok=False)

        # palabra_clave -> {ruta_pdf: [páginas]}
        estructura_exportacion = {}

        for ruta_pdf, paginas in self.resultados.items():
            for pagina, palabras in paginas.items():
                for palabra in palabras:
                    if palabra not in estructura_exportacion:
                        estructura_exportacion[palabra] = {}

                    if ruta_pdf not in estructura_exportacion[palabra]:
                        estructura_exportacion[palabra][ruta_pdf] = set()

                    estructura_exportacion[palabra][ruta_pdf].add(pagina)

        # Exportar
        for palabra, archivos in estructura_exportacion.items():
            for ruta_pdf, paginas_set in archivos.items():
                try:
                    reader = PdfReader(ruta_pdf)
                    writer = PdfWriter()

                    paginas_ordenadas = sorted(paginas_set)

                    for num_pagina in paginas_ordenadas:
                        if 0 < num_pagina <= len(reader.pages):
                            writer.add_page(reader.pages[num_pagina-1])#
                        else:
                            print(f"Página {num_pagina} fuera de rango en {ruta_pdf}")

                    # Preparar rutas
                    nombre_archivo = os.path.basename(ruta_pdf)
                    nombre_salida = f"Hojas de {nombre_archivo}"
                    carpeta_salida = os.path.join(final_dir, palabra)
                    os.makedirs(carpeta_salida, exist_ok=True)

                    ruta_salida = os.path.join(carpeta_salida, nombre_salida)

                    # Guardar nuevo PDF
                    with open(ruta_salida, "wb") as f:
                        writer.write(f)

                except Exception as e:
                    print(f"Error exportando {final_dir} para palabra '{palabra}': {e}")
                    QMessageBox.critical(self, f"Error al exportar {final_dir} para palabra '{palabra}'", f"No se pudo exportar el pdf:\n{str(e)}")

        # Mostrar mensaje de finalización
        QMessageBox.information(None, "Exportación completada",
                                f"Los resultados fueron exportados correctamente a:\n\n{final_dir}")

        # Volver a la pantalla inicial (VistaBusqueda)
        self.volverSignal.emit()
