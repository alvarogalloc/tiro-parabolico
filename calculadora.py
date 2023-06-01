from typing import Dict, List
from solver import Solver
import math


from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QPushButton,
    QLabel,
    QGridLayout,
    QWidget,
    QCheckBox,
)
from pathlib import Path

from PyQt6.QtGui import (
    QDoubleValidator,
    QFont,
)
from PyQt6 import (
    QtWidgets,
)
        
from submitbutton import SubmitButton


class NewWindow(QtWidgets.QMainWindow):
    def __init__(self, text):
        super().__init__()

        label = QtWidgets.QLabel(text, self)
        label.setWordWrap(True)
        label.setFont(QFont("Arial", 16))

        self.setCentralWidget(label)
        self.resize(400, 200)
        label.setMinimumSize(400, 200)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QtWidgets.QMainWindow):
    valores_solver: Dict[str, float] = {}
    ventana_de_ayuda: NewWindow
    solver: Solver
    line_inputs: List[QLineEdit] = []

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Capicalc")
        # crea una lista vacía para despues rellanarla con los valores de entrada
        layout = QGridLayout()
        ingresa_dato = QLabel("Valores de Entrada", self)
        salida_dato = QLabel("Valores de Salida", self)
        ingresa_dato.setFont(QFont("Arial", 16))
        salida_dato.setFont(QFont("Arial", 16))
        layout.addWidget(ingresa_dato, 0, 1)
        layout.addWidget(salida_dato, 0, 4)

        self.action_button = SubmitButton()
        self.action_button.clicked.connect(self.calcular)
        valores_solver_names = [
            "Variable t",
            "Gravedad (g m/s^2)",
            "Altura Inicial (h0 metros)",
            "Altura Final (hf metros)",
            # "Constante del Resorte (k)",
            # "Masa del Balon (m)",
        ]

        def puede_calcular() -> bool:
            # regresa true si todos los valores ya fueron ingresados
            n_valores_necesitados = len(valores_solver_names)
            n_valores_dados = len(self.valores_solver)
            return n_valores_dados == n_valores_necesitados

        def cambiar_valor_solver(text, el):
            #if text is empty, remove the key from the Dict
            if not text:
                del self.valores_solver[el]
                return
            
            self.valores_solver[el] = float(text)
            if puede_calcular():
                self.action_button.setDisabled(False)
            else:
                self.action_button.setDisabled(True)

        grid_row = 0
        for element in valores_solver_names:
            grid_row += 1
            layout.addWidget(QLabel(f"{element}"), grid_row, 0)
            widget = QLineEdit()  # crea un widget QLineEdit
            self.line_inputs.append(widget)
            widget.setValidator(QDoubleValidator())  # solo aceptar numeros
            widget.textEdited.connect(
                lambda w=widget, el=element: cambiar_valor_solver(w, el)
            )  # Es lo que hace que se actialize cada que cambias de qlineedit
            layout.addWidget(widget, grid_row, 1)  # agrega el widget al layout

        # output_names = [
        #     # "Angulo (θ)",
        #     # "Compresión del resorte (Xc)",
        #     "Velocidad inicial (Vo)",
        # ]
        # for m in range(3):
        layout.addWidget(QLabel("Velocidad inicial (Vo)"), 1, 3)
        self.widget_velocidad_inicial = QLabel("")
        layout.addWidget(self.widget_velocidad_inicial, 1, 4)

        check = QCheckBox()
        layout.addWidget(check, 8, 0)
        check.setText("Auto")

        restart_button = QPushButton("Resetear")
        restart_button.clicked.connect(lambda : self.reset())
        layout.addWidget(restart_button, 7, 0)

        layout.addWidget(self.action_button, 7, 1, 1, 2)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        boton_ayuda = QPushButton("Ayuda", self)
        boton_ayuda.clicked.connect(self.abrir_ventana_de_ayuda)
        layout.addWidget(boton_ayuda, 0, 0)


    def reset(self):
        for input in self.line_inputs:
            input.setText("")
    # Abre la ventana de ayuda
    def abrir_ventana_de_ayuda(self):
        text = """En la primer columna de datos tendras que introducir
        los valores de entrada que indica cada uno y del lado derecho saldran
        los resultados. Para empezar a calcular presiona el boton de calcular.
        Para quitar todos los valores en resetear.
        Presiona Auto para hacer los calculos Automaticamente"""
        text = text.replace("\n", "").replace("  ", "")
        self.ventana_de_ayuda = NewWindow(text)
        self.ventana_de_ayuda.show()

    def calcular(self):
        if len(self.valores_solver) > 4:
            values = list(self.valores_solver.values())
            self.solver = Solver(values[0], values[1], values[2], values[3])
            self.widget_velocidad_inicial.setText(str(math.sqrt(self.solver._computeVsquared())))

    # Set the central widget of the Window. Widget will expand
    # to take up all the space in the window by default.
    #
app = QApplication([])
app.setStyleSheet(Path('style.css').read_text())

window = MainWindow()
window.show()

app.exec()
