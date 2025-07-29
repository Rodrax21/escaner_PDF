from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class VistaResultados(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.layout = QVBoxLayout()
        self.label_info = QLabel("Aquí se mostrarán los resultados...")
        self.boton_extraer = QPushButton("Extraer páginas relevantes")
        self.boton_volver = QPushButton("Volver al inicio")

        self.layout.addWidget(self.label_info)
        self.layout.addWidget(self.boton_extraer)
        self.layout.addWidget(self.boton_volver)
        self.setLayout(self.layout)

        self.boton_volver.clicked.connect(self.main_window.volver_a_inicio)

    def mostrar_resultados(self, palabras, archivos):
        texto = f"Palabras clave: {', '.join(palabras)}\nArchivos: {len(archivos)} archivo(s) seleccionado(s)."
        self.label_info.setText(texto)