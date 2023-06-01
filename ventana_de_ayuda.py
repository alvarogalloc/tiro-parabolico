from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QFont

class VentanaDeAyuda(QMainWindow):
    def __init__(self):
        super().__init__()
        text = """En la primer columna de datos tendras que introducir
        los valores de entrada que indica cada uno y del lado derecho saldran
        los resultados. Para empezar a calcular presiona el boton de calcular.
        Para quitar todos los valores en resetear.
        Presiona Auto para hacer los calculos Automaticamente"""
        text = text.replace("\n", "").replace("  ", "")
        label = QLabel(text, self)
        label.setWordWrap(True)
        label.setFont(QFont("Arial", 16))

        self.setCentralWidget(label)
        self.resize(400, 200)
        label.setMinimumSize(400, 200)
