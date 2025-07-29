from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QObject
from widgets.FlowLayout import FlowLayout
from PyQt5.QtCore import pyqtSignal


class TagInput(QWidget):
    def __init__(self):
        super().__init__()

        self.tags = []
        class Emisor(QObject):
            tags_cambiaron = pyqtSignal()

        self.emisor = Emisor()

        # Entrada superior (donde se escribe)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Escribí palabras y presioná coma o Enter")
        self.input.returnPressed.connect(self.convertir_a_tag)
        self.input.textChanged.connect(self.chequear_coma)

        # FlowLayout para los tags
        self.flow_widget = QWidget()
        self.flow_widget.setObjectName("tagContainer")
        self.flow_layout = FlowLayout()
        self.flow_widget.setLayout(self.flow_layout)
        self.flow_widget.setContentsMargins(5,5,5,5)

        self.flow_widget.setStyleSheet("""
            QWidget#tagContainer {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #f9f9f9;
                padding: 5px;
            }
        """)

        # Scroll area para los tags si hay muchos
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet( 
        """QScrollArea {
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
        """)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.flow_widget)
        self.scroll_area.setFixedHeight(100)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Layout final (input arriba, tags abajo)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        self.main_layout.addWidget(self.input)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

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

        self.flow_layout.addWidget(tag_frame)

        self.emisor.tags_cambiaron.emit()  # Emitir señal de cambio

    def eliminar_tag(self, texto, frame):
        if texto in self.tags:
            self.tags.remove(texto)
        self.flow_layout.removeWidget(frame)
        frame.deleteLater()

        self.emisor.tags_cambiaron.emit()  # Emitir señal de cambio

    def obtener_tags(self):
        return self.tags
