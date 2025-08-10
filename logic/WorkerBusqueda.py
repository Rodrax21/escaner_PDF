from PyQt5.QtCore import QObject, pyqtSignal
from pathlib import Path
import fitz  # PyMuPDF
import os
import tempfile
from docx2pdf import convert
from pdf2docx import Converter
from PyPDF2 import PdfReader, PdfWriter
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from logic.Translator import get_translation as T

class WorkerBusqueda(QObject):
    volverSignal = pyqtSignal()
    terminado = pyqtSignal(object)  # Signal to emit results

    def __init__(self, archivos_pdf, palabras_clave, main_window, apellido_paciente, nombre_paciente):
        self.main_window = main_window

        self.apellido_paciente : str = apellido_paciente
        self.nombre_paciente : str = nombre_paciente

        super().__init__()
        self.archivos_pdf = archivos_pdf

        self.palabras_clave = [p.lower() for p in palabras_clave]
        self.resultados = {}


    def run(self):
        self.resultados = self.buscar_palabras_en_pdfs()
        self.terminado.emit(self.resultados)

    def convertir_word_a_pdf(self, ruta_docx):

        # Crear carpeta temporal fija de la app
        temp_dir = os.path.join(tempfile.gettempdir(), "scanner_pdf_temp")
        os.makedirs(temp_dir, exist_ok=True)  # Asegura que exista

        nombre_base = os.path.splitext(os.path.basename(ruta_docx))[0]
        ruta_pdf = os.path.join(temp_dir, f"{nombre_base}.pdf")

        # Convertir solo si no existe (opcional: evita sobrescribir)
        if not os.path.exists(ruta_pdf):
            try:
                print(f"Convirtiendo {ruta_docx} a PDF...")
                convert(ruta_docx, ruta_pdf)
                print(f"PDF convertido: {ruta_pdf}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"{T("WB_critical_docs")}\n{str(e)}")

        if not os.path.exists(ruta_pdf):
            raise FileNotFoundError("Error al convertir el .docx a PDF")

        return ruta_pdf

    def buscar_palabras_en_pdfs(self):

        print("Iniciando búsqueda de palabras clave en PDFs/DOCS")
        resultados = {}

        for ruta_original in self.archivos_pdf:
            try:
                print(f"Procesando archivo: {ruta_original}")
                
                ruta = Path(ruta_original).resolve()
                if ruta.suffix.lower() == ".docx":
                    print(f"Convirtiendo {ruta} a PDF...")
                    ruta_pdf = self.convertir_word_a_pdf(ruta_original)
                else:
                    ruta_pdf = ruta_original

                print(f"Ruta PDF procesada: {ruta_pdf}")
                ruta_pdf = Path(ruta_pdf)

                print(f"Ruta PDF final: {ruta_pdf}")
                resultados[ruta_original] = {}

                doc = fitz.open(ruta_pdf)
                for num_pagina, pagina in enumerate(doc, start=1):
                    texto = pagina.get_text()
                    coincidencias = [palabra for palabra in self.palabras_clave if palabra.lower() in texto.lower()]
                    #coincidencias = [
                    #    palabra for palabra in self.palabras_clave
                    #    if re.search(rf'\b{re.escape(palabra.lower())}\b', texto.lower())
                    #] #Evita busquedas parciales

                    if coincidencias:
                        resultados[ruta_original][num_pagina] = coincidencias

                doc.close()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"{T("WB_critical_1")}\n{str(e)}")

        return resultados

    def obtener_resultados(self):
        return self.resultados
    
    def check_for_empty_pages(self):
        for direccion_path in self.resultados:
            paginas_por_documento = self.resultados[direccion_path]
            # Si el diccionario de páginas no está vacío, significa que hay páginas con resultados.
            # En Python, un diccionario vacío {} se evalúa como False, y uno con contenido como True.
            if paginas_por_documento:
                return False
                
        # Si el bucle termina, significa que no se encontró ningún documento con páginas.
        return True
    
    def exportar_resultados(self):
        print(self.resultados)
        if self.check_for_empty_pages():
            QMessageBox.warning(None, T("WB_warning_1a"), T("WB_warning_1b"))
            return

        ruta_base = os.path.join(os.path.expanduser("~"), "Documents", "PDF Scanner", "extracciones")
        os.makedirs(ruta_base, exist_ok=True)

        folder_path = QFileDialog.getExistingDirectory(
            self.main_window, T("WB_search"), ruta_base
        )

        if not folder_path:
            return

        nombre_carpeta = f"{self.apellido_paciente.upper()}, {self.nombre_paciente}"
        base_dir = os.path.join(folder_path, nombre_carpeta)

        final_dir = base_dir
        counter = 1
        while os.path.exists(final_dir):
            final_dir = base_dir + f" ({counter})"
            counter += 1

        os.makedirs(final_dir, exist_ok=False)

        # Reorganizar resultados: palabra_clave -> {ruta_pdf: [páginas]}
        estructura_exportacion = {}
        for ruta_pdf, paginas in self.resultados.items():
            for pagina, palabras in paginas.items():
                for palabra in palabras:
                    estructura_exportacion.setdefault(palabra, {}).setdefault(ruta_pdf, set()).add(pagina)

        for palabra, archivos in estructura_exportacion.items():
            carpeta_salida = os.path.join(final_dir, palabra)
            os.makedirs(carpeta_salida, exist_ok=True)

            for ruta_pdf, paginas_set in archivos.items():
                try:
                    ext = os.path.splitext(ruta_pdf)[1].lower()

                    if ext == ".pdf":
                        reader = PdfReader(ruta_pdf)
                        for num_pagina in sorted(paginas_set):
                            if 0 < num_pagina <= len(reader.pages):
                                writer = PdfWriter()
                                writer.add_page(reader.pages[num_pagina - 1])

                                nombre_base, extension = os.path.splitext(os.path.basename(ruta_pdf))
                                nombre_salida = f"{nombre_base} (Pag. {num_pagina}){extension}"
                                ruta_salida = os.path.join(carpeta_salida, nombre_salida)

                                with open(ruta_salida, "wb") as f:
                                    writer.write(f)
                            else:
                                print(f"Página {num_pagina} fuera de rango en {ruta_pdf}")

                    elif ext == ".docx":
                        self.extraer_docs_a_docs(ruta_pdf, paginas_set, carpeta_salida)    # Para exportar a DOCX
                        #self.extraer_docs_a_pdfs(ruta_pdf, paginas_set, carpeta_salida)     # Para exportar a PDF

                    else:
                        print(f"Tipo de archivo no soportado: {ruta_pdf}")

                except Exception as e:
                    print(f"Error exportando para palabra '{palabra}': {e}")
                    QMessageBox.critical(self.main_window,
                                        f"Error al exportar para palabra '{palabra}'",
                                        f"No se pudo exportar:\n{str(e)}")

        QMessageBox.information(None, T("WB_success_1"),
                                f"{T('WB_success_2')}\n\n{final_dir}")
        self.volverSignal.emit()

    def extraer_docs_a_pdfs(self, ruta_pdf, paginas_set, carpeta_salida):
        temp_dir = os.path.join(tempfile.gettempdir(), "scanner_pdf_temp")
        nombre_base = os.path.splitext(os.path.basename(ruta_pdf))[0]
        ruta_pdf_temp = os.path.join(temp_dir, f"{nombre_base}.pdf")

        if not os.path.exists(ruta_pdf_temp):
            print(f"PDF temporal no encontrado para {ruta_pdf}")
            return

        reader = PdfReader(ruta_pdf_temp)
        for num_pagina in sorted(paginas_set):
            if 0 < num_pagina <= len(reader.pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[num_pagina - 1])

                nombre_base, extension = os.path.splitext(os.path.basename(ruta_pdf))
                nombre_salida_pdf = f"{nombre_base} (Pag. {num_pagina}).pdf"
                ruta_salida_pdf = os.path.join(carpeta_salida, nombre_salida_pdf)

                with open(ruta_salida_pdf, "wb") as f:
                    writer.write(f)
            else:
                print(f"Página {num_pagina} fuera de rango en {ruta_pdf}")
    
    def extraer_docs_a_docs(self, ruta_pdf, paginas_set, carpeta_salida):
        temp_dir = os.path.join(tempfile.gettempdir(), "scanner_pdf_temp")
        nombre_base = os.path.splitext(os.path.basename(ruta_pdf))[0]
        ruta_pdf_temp = os.path.join(temp_dir, f"{nombre_base}.pdf")

        if not os.path.exists(ruta_pdf_temp):
            print(f"PDF temporal no encontrado para {ruta_pdf}")
            return

        for num_pagina in sorted(paginas_set):
            try:
                # Crear un PDF temporal que solo contenga esa página
                reader = PdfReader(ruta_pdf_temp)
                writer = PdfWriter()
                if 0 < num_pagina <= len(reader.pages):
                    writer.add_page(reader.pages[num_pagina - 1])
                else:
                    continue

                # Guardar temporalmente la página como PDF individual
                temp_pdf_page = os.path.join(tempfile.gettempdir(), f"temp_page_{num_pagina}.pdf")
                with open(temp_pdf_page, "wb") as f:
                    writer.write(f)

                # Convertir esa página PDF a DOCX
                nombre_docx, extension = os.path.splitext(os.path.basename(ruta_pdf))
                nombre_salida_docx = f"{nombre_docx} (Pag. {num_pagina}){extension}"
                ruta_salida_docx = os.path.join(carpeta_salida, nombre_salida_docx)

                cv = Converter(temp_pdf_page)
                cv.convert(ruta_salida_docx, start=0, end=0)  # Solo tiene una página
                cv.close()

                os.remove(temp_pdf_page)

            except Exception as e:
                print(f"Error exportando página {num_pagina} a DOCX: {e}")
