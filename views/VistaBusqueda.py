from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QListWidget, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from widgets.TagInput import TagInput

class VistaBusqueda(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.rutas_pdf = []

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
        self.lista_pdfs = QListWidget()
        layout_principal.addWidget(self.lista_pdfs)

        # --- Layout de botones ---
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_pdf)
        layout_botones.addWidget(self.boton_continuar)
        layout_principal.addLayout(layout_botones)

        self.setLayout(layout_principal)

    def abrir_dialogo_pdf(self):
        archivos, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar archivos PDF", "", "Archivos PDF (*.pdf)"
        )
        if archivos:
            self.rutas_pdf = archivos
            self.lista_pdfs.clear()
            self.lista_pdfs.addItems(archivos)

    def continuar(self):
        palabras = self.input_palabras.obtener_tags()
        palabras = [p.strip() for p in palabras if p.strip()]
        if palabras and self.rutas_pdf:
            self.main_window.cambiar_a_resultados(palabras, self.rutas_pdf)
        else:
            print("Faltan palabras clave o archivos PDF")
