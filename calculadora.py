import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QLabel,
    QGridLayout,
    QWidget,
    QCheckBox,
)
from PyQt6.QtGui import (
    QFont,
)
from PyQt6 import QtWidgets


# Subclass QMainWindow to customize your application's main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QGridLayout()

        ingresa_dato = QLabel("Valores de Entrada", self)
        salida_dato = QLabel("Valores de Salida", self)
        ingresa_dato.setFont(QFont("Arial", 16))
        salida_dato.setFont(QFont("Arial", 16))
        layout.addWidget(ingresa_dato, 0, 1)
        layout.addWidget(salida_dato, 0, 4)

        action_button = QPushButton("Calcular")
        input_names = {
            0: "Variable t",
            1: "Gravedad (g)",
            2: "Altura Inicial (h0)",
            3: "Altura Final (hf)",
            4: "Constante del Resorte (k)",
            5: "Masa del Balon (m)",
        }
        for n in range(6):
            layout.addWidget(QLabel(f"{input_names[n]}"), n + 1, 0)
            layout.addWidget(QLineEdit(), n + 1, 1)

        output_names = {
            0: "Angulo (θ)",
            1: "Compresión del resorte (Xc)",
            2: "Velocidad inicial (Vo)",
        }
        for m in range(3):
            layout.addWidget(QLabel(f"{output_names[m]}"), m + 1, 3)
            layout.addWidget(QLineEdit(), m + 1, 4)

        check = QCheckBox()
        layout.addWidget(check, 8, 0)
        check.setText("Auto")

        restart_button = QPushButton("Resetear")
        layout.addWidget(restart_button, 7, 0)

        layout.addWidget(action_button, 7, 1, 1, 2)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        boton_ayuda = QPushButton("Ayuda", self)
        boton_ayuda.clicked.connect(self.abrir_ventana)
        layout.addWidget(boton_ayuda, 0, 0)

    def abrir_ventana(self):
        text = """\
                En la primer columna de datos tendras que introducir los\
                volores de entrada que indica cada uno y del lado derecho\
                salgran los resultados. Para empezar a calcular\
                presiona el boton de calcular. Para quitar todos los valores en
                resetear.\
                Presiona Auto para hacer los calculos Automaticamente\
                """
        self.abrir_ventana = NewWindow(text)
        self.abrir_ventana.show()


class NewWindow(QtWidgets.QMainWindow):
    def __init__(self, text):
        super().__init__()

        label = QtWidgets.QLabel(text, self)
        label.setWordWrap(True)
        label.setFont(QFont("Arial", 12))
        label.setContentsMargins(20, 20, 20, 20)
        layout = QtWidgets.QVBoxLayout(self)

        layout.addWidget(label)
        self.resize(400, 200)
        label.setMinimumSize(400, 200)

    # Set the central widget of the Window. Widget will expand
    # to take up all the space in the window by default.
    #


app = QtWidgets.QApplication([])
# app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
