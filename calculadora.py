# Librerias de python
from pathlib import Path
from typing import List

# De Qt
from PyQt6.QtGui import (
    QDoubleValidator,
    QFont,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QWidget,
)

# Nuestros Módulos
from solver import Solver
from submitbutton import BotonCalcular


class VentanaPrincipal(QMainWindow):
    # Miembros de la clase
    solver: Solver
    entradas: List[QLineEdit] = []
    salidas: List[QLabel] = []
    boton_calcular: BotonCalcular
    n_inputs_dados: int = 0
    checkbox: QCheckBox

    def __init__(self):
        # Es como llamar a QMainWindow.__init__()
        # inicializa los miembros que heredamos de esa clase
        super().__init__()
        self.setMaximumWidth(1024)

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
        layout.addWidget(label_salida, 0, 3)

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
            if self.checkbox.isChecked() and self.puede_calcular():
                self.calcular()

        grid_row = 0
        for element in entrada_nombres:
            grid_row += 1
            layout.addWidget(QLabel(f"{element}"), grid_row, 0)
            entrada = QLineEdit()  # crea un widget QLineEdit
            entrada.setMaximumWidth(200)
            self.entradas.append(entrada)
            validador = QDoubleValidator()
            if (
                element == "Constante del Resorte (k)"
                or element == "Masa del Balon (m)"
                or element == "Variable t"
            ):
                validador.setBottom(0.00001)

            validador.setNotation(QDoubleValidator.Notation.StandardNotation)
            entrada.setValidator(validador)  # solo aceptar numeros
            entrada.textEdited.connect(
                actualizar_entrada
            )  # Es lo que hace que se actialize cada que cambias de qlineedit
            layout.addWidget(entrada, grid_row, 1)  # agrega el widget al layout

        output_names = [
            "Angulo (θ)",
            "Compresión del resorte (Xc)",
            # "Velocidad inicial (Vo)",
            # "Distancia del objetivo"
        ]

        for m in range(len(output_names)):
            layout.addWidget(QLabel(output_names[m]), m + 1, 2)
            salida = QLabel()
            self.salidas.append(salida)
            layout.addWidget(salida, m + 1, 3)

        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox, 8, 0)
        self.checkbox.setText("Auto")

        boton_reset = QPushButton("Resetear")
        boton_reset.clicked.connect(lambda: self.reset())
        layout.addWidget(boton_reset, 7, 0)

        layout.addWidget(self.boton_calcular, 7, 1)
        entrada = QWidget()
        entrada.setLayout(layout)

        self.setCentralWidget(entrada)

        boton_ayuda = QPushButton("Ayuda", self)
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        layout.addWidget(boton_ayuda, 0, 0)

        image = QPixmap("res/logo.png").scaled(64*3,64*3)
        image_label = QLabel(self)
        image_label.setPixmap(image)
        # image_label.setFixedSize(image.size())
        # image_label.move(500, 500)
        image_label.setMargin(50)
        # layout.setColumnMinimumWidth(1, 200)
        # layout.setColumnMinimumWidth(2, 200)
        # layout.setColumnMinimumWidth(3, 200)
        text_label = QLabel("CapyCalc\nby Altamira")
        text_label.setObjectName("LogoText")
        layout.addWidget(image_label, 2, 2, 4,3)
        layout.addWidget(text_label, 3, 3)

    def mostrar_ayuda(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Ayuda")
        dlg.setText(
            "En la primer columna de datos tendras que introducir los valores de entrada que indica cada uno y del lado derecho saldran los resultados. Para empezar a calcular presiona el boton de calcular. Para quitar todos los valores en resetear. Presiona Auto para hacer los calculos Automaticamente"
        )
        button = dlg.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")

    def puede_calcular(self) -> bool:
        # Si el numero de datos ingresados es el mismo que los necesitados
        return self.n_inputs_dados == 6

    def reset(self):
        for salida in self.entradas:
            salida.setText("")
        for salida in self.salidas:
            salida.setText("")
        self.boton_calcular.setDisabled(True)

    def calcular(self):
        try:
            varT = float(self.entradas[0].text())
            gravity = float(self.entradas[1].text())
            h0 = float(self.entradas[2].text())
            hf = float(self.entradas[3].text())
            spring_constant = float(self.entradas[4].text())
            mass = float(self.entradas[5].text())
        # when incomplete input
        except ValueError:
            return

        self.solver = Solver(varT, gravity, h0, hf, spring_constant, mass)
        # Calcula los valores de salidas y ponerlos en los labels
        self.salidas[0].setText(str(self.solver.angle()))

        compresion = str(self.solver.spring_compression())
        if compresion == "nan":
            self.salidas[1].setText("El resorte es muy debil")
        else:
            self.salidas[1].setText(compresion)

        # disabled on line 97-98
        # self.salidas[2].setText(str(self.solver.velocidad_inicial()))
        # self.salidas[3].setText(str(self.solver._computeL()))


app = QApplication([])
# estilos
app.setStyleSheet(Path("style.css").read_text())

window = VentanaPrincipal()
window.show()

app.exec()
