from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QListWidget, QVBoxLayout, QHBoxLayout, QScrollArea
)
import os
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from widgets.TagInput import TagInput
from widgets.EtiquetaPDF import EtiquetaPDF

class VistaBusqueda(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.rutas_pdf = set()  # Usar un set para evitar duplicados

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
            QPushButton:hover {
                background-color: #357abd;
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
        self.boton_continuar = QPushButton("Buscar y continuar")
        self.boton_continuar.setObjectName("boton_vista")
        self.boton_continuar.clicked.connect(self.continuar)

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

    def remover_pdf(self, item):
        ruta_str = item.pdf_path.resolve()
        if ruta_str in self.rutas_pdf:
            self.lista_pdf_layout.removeWidget(item)
            item.deleteLater()
            self.rutas_pdf.remove(ruta_str)
            # El widget ya se elimina con .setParent(None) desde EtiquetaPDF

    def continuar(self):
        palabras = self.input_palabras.obtener_tags()
        palabras = [p.strip() for p in palabras if p.strip()]
        if palabras and self.rutas_pdf:
            self.main_window.cambiar_a_resultados(palabras, self.rutas_pdf)
        else:
            print("Faltan palabras clave o archivos PDF")
