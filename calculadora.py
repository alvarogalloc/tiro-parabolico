# Librerias de python
from pathlib import Path
from typing import List

# De Qt
from PyQt6.QtGui import (
    QDoubleValidator,
    QFont,
)

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
)

# Nuestros Módulos
from solver import Solver
from submitbutton import BotonCalcular
from ventana_de_ayuda import VentanaDeAyuda


class VentanaPrincipal(QMainWindow):
    # Miembros de la clase
    ventana_de_ayuda: VentanaDeAyuda
    solver: Solver
    entradas: List[QLineEdit] = []
    salidas: List[QLabel] = []
    boton_calcular: BotonCalcular
    n_inputs_dados: int = 0

    def __init__(self):
        # Es como llamar a QMainWindow.__init__()
        # inicializa los miembros que heredamos de esa clase
        super().__init__()

        self.setWindowTitle("Capicalc")
        # crea una lista vacía para despues rellanarla con los valores de entrada
        layout = QGridLayout()
        label_entrada = QLabel("Valores de Entrada", self)
        label_salida = QLabel("Valores de Salida", self)
        label_entrada.setFont(QFont("Arial", 16))
        label_salida.setFont(QFont("Arial", 16))

        # nuestro layout va asi

        # |---|---|---|---|---|
        # |L_E|   |   |   |L_S|
        # |   |   |   |   |   |
        # |---|---|---|---|---|
        layout.addWidget(label_entrada, 0, 1)
        layout.addWidget(label_salida, 0, 4)

        self.boton_calcular = BotonCalcular()
        self.boton_calcular.clicked.connect(self.calcular)

        entrada_nombres = [
            "Variable t",
            "Gravedad (g m/s^2)",
            "Altura Inicial (h0 metros)",
            "Altura Final (hf metros)",
            "Constante del Resorte (k)",
            "Masa del Balon (m)",
        ]

        def actualizar_entrada() -> None:
            self.n_inputs_dados = 0
            for i in self.entradas:
                if i.text():
                    self.n_inputs_dados += 1
            self.boton_calcular.setDisabled(not self.puede_calcular())

        grid_row = 0
        for element in entrada_nombres:
            grid_row += 1
            layout.addWidget(QLabel(f"{element}"), grid_row, 0)
            entrada = QLineEdit()  # crea un widget QLineEdit
            self.entradas.append(entrada)
            validador = QDoubleValidator()
            validador.setNotation(QDoubleValidator.Notation.StandardNotation)
            entrada.setValidator(validador)  # solo aceptar numeros
            entrada.textEdited.connect(
                actualizar_entrada
            )  # Es lo que hace que se actialize cada que cambias de qlineedit
            layout.addWidget(entrada, grid_row, 1)  # agrega el widget al layout

        output_names = [
            "Angulo (θ)",
            "Compresión del resorte (Xc)",
        ]

        for m in range(len(output_names)):
            layout.addWidget(QLabel(output_names[m]), m + 1, 3)
            salida = QLabel()
            self.salidas.append(salida)
            layout.addWidget(salida, m + 1, 4)

        check = QCheckBox()
        layout.addWidget(check, 8, 0)
        check.setText("Auto")

        boton_reset = QPushButton("Resetear")
        boton_reset.clicked.connect(lambda: self.reset())
        layout.addWidget(boton_reset, 7, 0)

        layout.addWidget(self.boton_calcular, 7, 1, 1, 2)
        entrada = QWidget()
        entrada.setLayout(layout)

        self.setCentralWidget(entrada)

        boton_ayuda = QPushButton("Ayuda", self)
        self.ventana_de_ayuda = VentanaDeAyuda()
        boton_ayuda.clicked.connect(self.ventana_de_ayuda.show)
        layout.addWidget(boton_ayuda, 0, 0)

    def puede_calcular(self) -> bool:
        # Si el numero de datos ingresados es el mismo que los necesitados
        return self.n_inputs_dados == 6

    def reset(self):
        for salida in self.entradas:
            salida.setText("")
        for salida in self.salidas:
            salida.setText("")

    def calcular(self):
        self.solver = Solver(
            float(self.entradas[0].text()),
            float(self.entradas[1].text()),
            float(self.entradas[2].text()),
            float(self.entradas[3].text()),
            float(self.entradas[4].text()),
            float(self.entradas[5].text()),
        )
        # Calcula los valores de salidas y ponerlos en los labels
        self.salidas[0].setText(str(self.solver.angle()))
        self.salidas[1].setText(str(self.solver.spring_compression()))


app = QApplication([])
# estilos
app.setStyleSheet(Path("style.css").read_text())

window = VentanaPrincipal()
window.show()

app.exec()
