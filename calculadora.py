import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,

    QLineEdit,
    QMainWindow,

    QPushButton,
    QLabel,
    QGridLayout,
    QWidget,
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        layout = QGridLayout()

        action_button = QPushButton("calcular")
        input_names = {
            0: "Variable t",
            1: "Gravedad (g)",
            2:"Altura Inicial (h0)",
            3:"Altura Final (hf)",
            4:"Constante del Resorte (k)",
        }
        for n in range(5):
            layout.addWidget(QLabel(f"ingresa valor {input_names[n]}"), n, 0)
            layout.addWidget(QLineEdit(), n, 1)
        layout.addWidget(action_button, 5, 0, 1, 2)
        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
