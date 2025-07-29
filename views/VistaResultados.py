from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal

class VistaResultados(QWidget):
    volverSignal = pyqtSignal()  # Señal para volver a la vista anterior

    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Resultados de la búsqueda")
        layout.addWidget(self.label)

        self.resultado_texto = QTextEdit()
        self.resultado_texto.setReadOnly(True)
        layout.addWidget(self.resultado_texto)

        self.boton_volver = QPushButton("Volver")
        self.boton_volver.clicked.connect(self.volverSignal.emit)
        layout.addWidget(self.boton_volver)

        self.setLayout(layout)

    def mostrar_resultados(self, resultados):
        texto = ""
        for archivo, paginas in resultados.items():
            texto += f"\nArchivo: {archivo}\nPáginas: {', '.join(map(str, paginas))}\n"
        self.resultado_texto.setPlainText(texto)
