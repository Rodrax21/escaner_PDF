import sys
import ctypes
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from views.VistaBusqueda import VistaBusqueda
from views.VistaResultados import VistaResultados

from resources import recursos

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscador de Palabras en PDF")
        self.setFixedSize(700, 500)

        # Stacked widget para cambiar de vistas
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.setWindowIcon(QIcon(":/Antodrogas.ico"))

        self.centrar_ventana()

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

    def centrar_ventana(self):
        # Obtener geometría de la pantalla actual (donde está el cursor)
        pantalla = QApplication.primaryScreen()
        rect_pantalla = pantalla.availableGeometry()

        # Obtener el rectángulo de la ventana y moverla
        rect_ventana = self.frameGeometry()
        rect_ventana.moveCenter(rect_pantalla.center())
        self.move(rect_ventana.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/Antodrogas.ico"))

    # Forzar el cambio del ícono en la barra de tareas 
    if os.name == 'nt': # Solo pasa este if si la computadora que lo ejecuta es de Windows)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"mi_aplicacion.unica.id")

    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())