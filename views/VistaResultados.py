from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QScrollArea, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QSizePolicy
from collections import defaultdict
import os

from resources import recursos  # Asegúrate de que este recurso esté definido en tu archivo .qrc

class VistaResultados(QWidget):
    volverSignal = pyqtSignal()  # Señal para volver a la vista anterior
    exportarSignal = pyqtSignal()

    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.resultados = {}

        self.init_ui()

    def init_ui(self):
        self.layout_principal = QVBoxLayout(self)

        self.titulo = QLabel("Resultados de la Búsqueda")
        self.titulo.setObjectName("Titulo")
        self.titulo.setAlignment(Qt.AlignCenter)
        #self.titulo.setFont(QFont("Arial", 18, QFont.Bold))
        self.layout_principal.addWidget(self.titulo)

        # Scroll para que sea navegable si hay muchos resultados
        # Scroll para resultados
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(400)  # Altura visible máxima (ajustable)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Contenedor principal dentro del scroll
        self.contenedor = QWidget()
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.contenedor)
        self.scroll_area.setStyleSheet("""
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
        self.layout_principal.addWidget(self.scroll_area)

        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setObjectName("boton_vista")
        self.boton_volver.clicked.connect(self.volverSignal.emit)

        self.boton_exportar = QPushButton("Exportar Resultados")
        self.boton_exportar.setObjectName("boton_vista")
        self.boton_exportar.clicked.connect(self.exportarSignal.emit)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.boton_volver)
        layout_botones.addWidget(self.boton_exportar)
        self.layout_principal.addLayout(layout_botones)

        self.setLayout(self.layout_principal)

        self.setStyleSheet("""
            QLabel {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 10pt;
            }
            QLabel#Titulo {
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }               
            QLabel#pdfTitulo {
                font-weight: bold;
                font-size: 12pt;
                color: #2c3e50;
            }
            QFrame#pdfContenedor {
                border: 1px solid #ccc;
                border-radius: 10px;           
                background-color: #e0f0ff;
                padding: 5px;
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

    def mostrar_resultados(self, resultados):
         # Limpiar resultados previos
        for i in reversed(range(self.contenedor_layout.count())):
            widget = self.contenedor_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.resultados = resultados

        for ruta_pdf, paginas in resultados.items():
            nombre_archivo = os.path.basename(ruta_pdf)

            # Agrupar palabras clave por palabra: palabra -> [paginas]
            palabras_por_pagina = defaultdict(list)
            for pagina, coincidencias in paginas.items():
                for palabra in coincidencias:
                    palabras_por_pagina[palabra].append(pagina)

            # Crear contenedor para esta "fila"
            fila_contenedor = QFrame()
            fila_contenedor.setObjectName("pdfContenedor")
            fila_contenedor.setFrameShape(QFrame.NoFrame)

            fila_contenedor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            fila_contenedor.setMinimumHeight(10)

            fila_layout = QVBoxLayout(fila_contenedor)
            fila_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)  # fuerza ajuste a contenido

            # Cabecera con icono y nombre
            cabecera_layout = QHBoxLayout()
            icono_label = QLabel()
            icono_label.setPixmap(QPixmap(":/logo_pdf.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            texto_label = QLabel(nombre_archivo)
            texto_label.setObjectName("pdfTitulo")

            cabecera_layout.addWidget(icono_label)
            cabecera_layout.addWidget(texto_label)
            cabecera_layout.addStretch()

            fila_layout.addLayout(cabecera_layout)

            # Listar resultados
            for palabra, lista_paginas in palabras_por_pagina.items():
                paginas_ordenadas = sorted(set(lista_paginas))
                texto = f'– "{palabra}" en pág. {", ".join(map(str, paginas_ordenadas))}'
                fila_layout.addWidget(QLabel(texto))

            # Agregar esta fila al contenedor principal
            self.contenedor_layout.addWidget(fila_contenedor)

        self.contenedor.update()
        