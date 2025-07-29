import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from views.VistaBusqueda import VistaBusqueda
from views.VistaResultados import VistaResultados

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscador de Palabras en PDF")
        self.setFixedSize(700, 500)

        # Stacked widget para cambiar de vistas
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Crear vistas
        print("Inicializando vistas")
        self.vista_1 = VistaBusqueda(self)

        print("Vista de búsqueda creada")
        self.vista_2 = VistaResultados(self)

        print("Vista de resultados creada")

        self.stack.addWidget(self.vista_1)  # Índice 0
        self.stack.addWidget(self.vista_2)  # Índice 1

        print("Vistas agregadas al stack")

        self.stack.setCurrentIndex(0)

    def cambiar_a_resultados(self, palabras_clave, archivos_pdf):
        # Pasamos datos a la segunda vista antes de cambiar
        self.vista_2.mostrar_resultados(palabras_clave, archivos_pdf)
        self.stack.setCurrentIndex(1)

    def volver_a_inicio(self):
        self.stack.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())