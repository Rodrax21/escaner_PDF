from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pathlib import Path

from resources import recursos  # Asegúrate de que este recurso esté definido en tu archivo .qrc

class EtiquetaPDF(QWidget):
    def __init__(self, pdf_path, on_remove_callback):
        super().__init__()
        self.pdf_path = Path(pdf_path)
        self.on_remove_callback = on_remove_callback
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 5, 8, 5)
        layout.setSpacing(10)
        self.setFixedHeight(40)  # Altura fija

        # Icono PDF
        icon_label = QLabel()
        if self.pdf_path.suffix.lower() == ".docx":
            icon_pixmap = QPixmap(":/logo_doc.png")  # Ruta del ícono para Word
        else:
            icon_pixmap = QPixmap(":/logo_pdf.png")   # Ruta del ícono para PDF
        icon_label.setPixmap(icon_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(icon_label)

        print(self.pdf_path)

        # Nombre del archivo
        file_label = QLabel(self.pdf_path.name)
        file_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        layout.addWidget(file_label)

        # Botón de eliminar
        remove_button = QPushButton("✕")
        remove_button.setFixedSize(30, 30)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #ff3b3b;
            }
        """)
        remove_button.clicked.connect(lambda: self.on_remove_callback(self))
        layout.addWidget(remove_button)

        self.setLayout(layout)
        self.setStyleSheet("""
            background-color: #f7f7f7;
            border: 1px solid #ccc;
            border-radius: 8px;
        """)

