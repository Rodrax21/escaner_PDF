from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QLabel, QPushButton, QFrame,QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from widgets.FlowLayout import FlowLayout 

class TagInput(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.layout)

        self.tags = []
        self.input = QLineEdit()
        self.input.setPlaceholderText("Escribí palabras y presioná coma o Enter")
        self.input.returnPressed.connect(self.convertir_a_tag)
        self.input.textChanged.connect(self.chequear_coma)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(150)

        self.layout.addWidget(self.input)


    def chequear_coma(self):
        texto = self.input.text()
        if ',' in texto:
            palabras = texto.split(',')
            for palabra in palabras[:-1]:
                self.agregar_tag(palabra.strip())
            self.input.setText(palabras[-1])

    def convertir_a_tag(self):
        texto = self.input.text().strip()
        if texto:
            self.agregar_tag(texto)
            self.input.clear()

    def agregar_tag(self, texto):
        if not texto or texto in self.tags:
            return

        self.tags.append(texto)

        # Crear contenedor visual del tag (etiqueta + botón)
        tag_frame = QFrame()
        tag_layout = QHBoxLayout()
        tag_layout.setContentsMargins(10, 2, 10, 2)
        tag_layout.setSpacing(5)

        tag_label = QLabel(texto)
        tag_label.setFont(QFont("Courier New", 10))
        tag_label.setStyleSheet("color: #3366cc;")

        boton_cerrar = QPushButton("x")
        boton_cerrar.setFixedSize(16, 16)
        boton_cerrar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-weight: bold;
                color: #666;
            }
            QPushButton:hover {
                color: red;
            }
        """)
        boton_cerrar.clicked.connect(lambda _, t=texto, f=tag_frame: self.eliminar_tag(t, f))

        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(boton_cerrar)
        tag_frame.setLayout(tag_layout)
        tag_frame.setStyleSheet("""
            QFrame {
                background-color: #e0e0e0;
                border-radius: 10px;
            }
        """)

        self.layout.insertWidget(self.layout.count() - 1, tag_frame)

    def eliminar_tag(self, texto, frame):
        if texto in self.tags:
            self.tags.remove(texto)
        self.layout.removeWidget(frame)
        frame.deleteLater()

    def obtener_tags(self):
        return self.tags

