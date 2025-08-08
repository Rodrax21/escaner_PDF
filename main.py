import sys
import ctypes
import os
import tempfile
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from views.VistaBusqueda import VistaBusqueda
from views.VistaResultados import VistaResultados

from resources import recursos
from logic import AutoUpdater
from logic.Translator import get_translation as T
from logic.Translator import cycle_language

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{T("main_title")} - {AutoUpdater.__version__}")
        self.setFixedSize(750, 500)

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

    def cambiar_a_resultados(self, resultados):
        # Pasamos datos a la segunda vista antes de cambiar
        self.vista_2.mostrar_resultados(resultados)
        self.stack.setCurrentIndex(1)

    def volver_a_inicio(self):
        self.stack.setCurrentIndex(0)

    def centrar_ventana(self):
        # Centrar ventana en la pantalla principal
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = screen_geometry.center().x() - self.width() // 2
        y = screen_geometry.center().y() - self.height() // 2
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_I:  # Tecla 'i'
            nuevo_idioma = cycle_language()
            print(f"Idioma cambiado a: {nuevo_idioma}")
            self.vista_1.set_language()
            self.vista_2.set_language()
            self.setWindowTitle(f"{T("main_title")} - {AutoUpdater.__version__}")

    def limpiar_temporales_antiguos(self):
        temp_root = os.path.join(tempfile.gettempdir(), "scanner_pdf_temp")
        os.makedirs(temp_root, exist_ok=True)  # Asegura que exista

        for nombre in os.listdir(temp_root):
            path = os.path.join(temp_root, nombre)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                print(f"No se pudo borrar {path}: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/Antodrogas.ico"))

    # Forzar el cambio del ícono en la barra de tareas 
    if os.name == 'nt': # Solo pasa este if si la computadora que lo ejecuta es de Windows)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"mi_aplicacion.unica.id")

    ventana = MainWindow()
    ventana.centrar_ventana()
    ventana.show()
    ventana.limpiar_temporales_antiguos()
    AutoUpdater.comprobar_actualizaciones(parent=ventana)
    sys.exit(app.exec_())