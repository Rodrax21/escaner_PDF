# views/VistaCarga.py
from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from resources import recursos  # Asegúrate de que este recurso esté definido en tu archivo .qrc

class VistaCarga(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setModal(True)
        self.resize(300, 200)

        self.setWindowTitle("Procesando...")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.movie = QMovie(":/loading.gif")
        self.label.setMovie(self.movie)
        self.label.setAlignment(Qt.AlignCenter)
        self.movie.start()

    def centrar_en_ventana_principal(self):
        if self.parent():
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            x = screen_geometry.center().x() - self.width() // 2
            y = screen_geometry.center().y() - self.height() // 2
            self.move(x, y)

