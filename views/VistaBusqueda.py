from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout, QScrollArea
)
import os
from pathlib import Path
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread

from widgets.TagInput import TagInput
from widgets.EtiquetaPDF import EtiquetaPDF
from logic.WorkerBusqueda import WorkerBusqueda
from views.VistaCarga import VistaCarga

class VistaBusqueda(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.rutas_pdf = set()  # Usar un set para evitar duplicados
        class Emisor(QObject):
            archivos_cambiaron = pyqtSignal()

        self.emisor = Emisor()

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLabel#Titulo {
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }
            QLabel#label_pdf {
                font-size: 14px;
                font-weight: bold;           
                color: #444;
            }               
            QLineEdit {
                font-size: 14px;
                padding: 6px 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: #ffffff;
            }
            QPushButton#boton_vista {
                font-size: 14px;
                padding: 8px 18px;
                border: none;
                border-radius: 8px;
                background-color: #4a90e2;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover#boton_vista {
                background-color: #357abd;
            }
            QPushButton:disabled#boton_vista {
                background-color: #cccccc;
                color: #666666;
            }               
        """)

        # Layout principal
        layout_principal = QVBoxLayout()

        # --- TÍTULO ---
        self.titulo = QLabel("Buscador de Palabras Clave en PDF")
        self.titulo.setObjectName("Titulo")
        self.titulo.setAlignment(Qt.AlignCenter)
        #self.titulo.setFont(QFont("Arial", 18, QFont.Bold))
        layout_principal.addWidget(self.titulo)

        # --- Palabras clave ---
        self.input_palabras = TagInput()
        layout_principal.addWidget(self.input_palabras)

        # --- texto de pdf seleccionados ---
        self.label_pdf = QLabel("PDf's seleccionados:")
        self.label_pdf.setAlignment(Qt.AlignLeft)
        self.label_pdf.setObjectName("label_pdf")
        layout_principal.addWidget(self.label_pdf)

        # --- Selección de PDFs ---
        self.boton_pdf = QPushButton("Seleccionar archivos PDF")
        self.boton_pdf.setObjectName("boton_vista")
        self.boton_pdf.clicked.connect(self.abrir_dialogo_pdf)

        # --- Botón continuar ---
        self.boton_continuar = QPushButton("Comenzar búsqueda")
        self.boton_continuar.setObjectName("boton_vista")
        self.boton_continuar.clicked.connect(self.iniciar_busqueda)

        # Inhabilitar botón al inicio y habilitarlo cuando haya PDFs y palabras clave
        self.boton_continuar.setEnabled(False)
        self.input_palabras.emisor.tags_cambiaron.connect(self.actualizar_estado_boton_buscar)
        self.emisor.archivos_cambiaron.connect(self.actualizar_estado_boton_buscar)

        # --- Lista de PDFs seleccionados ---
        self.lista_pdf_layout = QVBoxLayout()
        self.lista_pdf_layout.setAlignment(Qt.AlignTop)
        self.lista_pdf_layout.setSpacing(6)

        self.lista_pdf_container = QWidget()
        self.lista_pdf_container.setStyleSheet("""
            QWidget {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #f9f9f9;
                padding: 5px;
            }
        """)
        self.lista_pdf_container.setLayout(self.lista_pdf_layout)

        self.scroll_area_pdf = QScrollArea()  # ya deberías tenerla creada
        self.scroll_area_pdf.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #f9f9f9;
                padding: 5px;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                margin: 2px 2px 2px 2px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #999;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                background: #f0f0f0;
                height: 10px;
                margin: 2px;
                border-radius: 4px;
            }

            QScrollBar::handle:horizontal {
                background: #999;
                min-width: 20px;
                border-radius: 4px;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }                                                                                           
        """)
        self.scroll_area_pdf.setWidgetResizable(True)
        self.scroll_area_pdf.setWidget(self.lista_pdf_container)
        
        layout_principal.addWidget(self.scroll_area_pdf)

        # --- Layout de botones ---
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_pdf)
        layout_botones.addWidget(self.boton_continuar)
        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)

    def abrir_dialogo_pdf(self):
        ruta_base = os.path.join(os.path.expanduser("~"), "Documents")
        os.makedirs(ruta_base, exist_ok=True)
        archivos, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar archivos PDF", ruta_base, "Archivos PDF (*.pdf)"
        )
        if archivos:
            self.agregar_pdfs(archivos)

    def agregar_pdfs(self, rutas):
        for ruta_str in rutas:
            ruta = Path(ruta_str).resolve()
            if ruta not in self.rutas_pdf:
                self.rutas_pdf.add(ruta)
                etiqueta = EtiquetaPDF(ruta, self.remover_pdf)
                self.lista_pdf_layout.addWidget(etiqueta)
        self.emisor.archivos_cambiaron.emit()

    def remover_pdf(self, item):
        ruta_str = item.pdf_path.resolve()
        if ruta_str in self.rutas_pdf:
            self.lista_pdf_layout.removeWidget(item)
            item.deleteLater()
            self.rutas_pdf.remove(ruta_str)
            self.emisor.archivos_cambiaron.emit()
            # El widget ya se elimina con .setParent(None) desde EtiquetaPDF

    def informar_estado(self):
        palabras = self.input_palabras.obtener_tags()
        palabras_clave = [p.strip() for p in palabras if p.strip()]
        print(f"Palabras clave: {palabras_clave}")
        print(f"Archivos PDF seleccionados: {[str(r) for r in self.rutas_pdf]}")

    def actualizar_estado_boton_buscar(self):
        hay_palabras = self.input_palabras.obtener_tags() != []
        hay_pdfs = self.rutas_pdf.__len__() > 0

        if hay_palabras and hay_pdfs:
            self.boton_continuar.setEnabled(True)
        else:
            self.boton_continuar.setEnabled(False)

    def iniciar_busqueda(self):
        self.informar_estado()

        self.dialogo_carga = VistaCarga(self)
        self.dialogo_carga.show()
        self.dialogo_carga.centrar_en_ventana_principal()

        # Crear el hilo y el worker
        self.thread = QThread()
        self.worker = WorkerBusqueda(self.rutas_pdf, self.input_palabras.obtener_tags(),self.main_window)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

        self.worker.terminado.connect(self.resultado_busqueda)
        self.worker.terminado.connect(self.dialogo_carga.close)
        self.worker.terminado.connect(self.thread.quit)

        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def resultado_busqueda(self, resultado):
        try:
            self.main_window.vista_2.volverSignal.disconnect()
            self.main_window.vista_2.exportarSignal.disconnect()
            self.worker.volverSignal.disconnect()
        except TypeError:
            pass  # No estaba conectado aún

        print(self.worker)
        # Conectar señales de la vista de resultados
        self.main_window.vista_2.volverSignal.connect(self.main_window.volver_a_inicio)
        self.main_window.vista_2.exportarSignal.connect(self.exportar)
        self.worker.volverSignal.connect(self.main_window.volver_a_inicio)

        self.main_window.cambiar_a_resultados(resultado)

    def exportar(self):
        self.worker.exportar_resultados()
