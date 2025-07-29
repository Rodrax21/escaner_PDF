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

        # Layout principal
        layout_principal = QVBoxLayout()

        # --- TÍTULO ---
        self.titulo = QLabel("Buscador de Palabras Clave en PDF")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setFont(QFont("Arial", 18, QFont.Bold))
        layout_principal.addWidget(self.titulo)

        # --- Palabras clave ---
        self.label_palabras = QLabel("Palabras clave (separadas por coma):")
        self.input_palabras = TagInput()

        layout_principal.addWidget(self.label_palabras)
        layout_principal.addWidget(self.input_palabras)

        # --- Selección de PDFs ---
        self.boton_pdf = QPushButton("Seleccionar archivos PDF")
        self.boton_pdf.clicked.connect(self.abrir_dialogo_pdf)

        self.lista_pdfs = QListWidget()

        layout_principal.addWidget(self.boton_pdf)
        layout_principal.addWidget(self.lista_pdfs)

        # --- Botón continuar ---
        self.boton_continuar = QPushButton("Buscar y continuar")
        self.boton_continuar.clicked.connect(self.continuar)

        layout_principal.addWidget(self.boton_continuar)

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
