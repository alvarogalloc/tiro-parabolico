import os

from pathlib import Path
from PyQt6 import QtCore
from PyQt6.QtCore import QLine, QSize, Qt, QPoint
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QWidget,
    QCheckBox,
    QToolTip,
    QPushButton,
    QLineEdit,
)
from PyQt6.QtGui import QDoubleValidator, QIcon, QImage, QPixmap, QCursor


from solver import Solver

basedir = os.path.dirname(__file__)


def restringir_input(widget, aceptar_negativos=False):
    input_validator = QDoubleValidator()
    input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
    if not aceptar_negativos:
        input_validator.setBottom(0)
    widget.setValidator(input_validator)


def widget_con_ayuda(widget, help_msg):
    container = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(widget)
    icon_label = QLabel()
    icon_help = QIcon(os.path.join(basedir, "res/ayuda.svg")).pixmap(QSize(24, 24))
    icon_label.setPixmap(icon_help)
    layout.addWidget(icon_label)
    icon_label.setToolTip(help_msg)
    container.setLayout(layout)
    return container


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capicalc")
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout_principal = QGridLayout(central_widget)
        layout_principal.setColumnStretch(0, 1)
        layout_principal.setColumnStretch(1, 1)
        lado_izquierdo = QGridLayout()
        lado_izquierdo.setColumnStretch(0, 1)
        lado_izquierdo.setColumnStretch(1, 1)
        self.lado_derecho = QGridLayout()
        self.lado_derecho.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for layout in [lado_izquierdo, self.lado_derecho]:
            layout.setContentsMargins(0, 0, 0, 0)

        boton_reset = QPushButton("Resetear")
        boton_calcular = QPushButton("Calcular")
        self.checkbox = QCheckBox("Auto")

        label_entrada = QLabel("Valores de Entrada")
        label_salida = QLabel("Valores de Salida")
        self.line_edits = []
        output_nombres = [
            "Ángulo (θ) ",
            "Compresión del resorte (X)",
        ]
        entrada_nombres = [
            "Masa Balón",
            "Gravedad",
            "Constante",
            "Altura Final",
            "Altura Inicial",
            "Distancia Horizontal",
        ]

        placeholders = [
            "Kilogramos",
            "metros/segundos^2",
            "Newton/metros",
            "metros",
            "metros",
            "metros",
        ]

        help_msgs = [
            "Masa del balón en kilogramos",
            "Gravedad en metros/segundos^2",
            "Que tan fuerte es el resorte en Newton/metros",
            "Altura del objetivo en metros",
            "Altura del cañon en metros",
            "Distancia hacia el objetivo en metros",
        ]

        label_entrada.setObjectName("label_entrada")
        label_salida.setObjectName("label_salida")

        layout_principal.addWidget(
            label_entrada, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_principal.addWidget(
            label_salida, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        lado_izquierdo.addWidget(self.checkbox, 10, 1)
        lado_izquierdo.addWidget(boton_reset, 9, 1)
        lado_izquierdo.addWidget(boton_calcular, 9, 2)

        layout_principal.addLayout(
            lado_izquierdo, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_principal.addLayout(
            self.lado_derecho, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_entrada.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_salida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_row = 0
        boton_calcular.clicked.connect(self.on_click_button)
        boton_reset.clicked.connect(self.resetear)

        self.checkbox.stateChanged.connect(self.calculo_auto)

        for n in range(len(entrada_nombres)):
            grid_row += 1
            lado_izquierdo.addWidget(QLabel(f"{entrada_nombres[n]}"), grid_row, 1)
            entrada = QLineEdit()
            self.line_edits.append(entrada)
            lado_izquierdo.addWidget(
                widget_con_ayuda(entrada, help_msgs[n]), grid_row, 2
            )
            entrada.setPlaceholderText(placeholders[n])
            if n not in [3, 4]:
                restringir_input(entrada)
            else:
                restringir_input(entrada, True)

        self.labels_salida = []
        self.salidas = []

        # obstaculo en x y y
        def hacer_input_obstaculo():
            container_obstaculo = QWidget()
            container_obstaculo_layout = QGridLayout()
            container_obstaculo_layout.setContentsMargins(0, 0, 0, 0)
            entrada_x = QLineEdit()
            entrada_y = QLineEdit()
            entrada_x.setPlaceholderText("x:")
            entrada_y.setPlaceholderText("y:")
            restringir_input(entrada_x)
            restringir_input(entrada_y, True)

            container_obstaculo_layout.addWidget(entrada_x, 0, 0)
            container_obstaculo_layout.addWidget(entrada_y, 0, 1)
            self.line_edits.append(entrada_x)
            self.line_edits.append(entrada_y)
            container_obstaculo.setLayout(container_obstaculo_layout)
            container_obstaculo.setFixedWidth(250)
            return widget_con_ayuda(
                container_obstaculo,
                "Coordenadas de un obstáculo\nen la trayectoria (x,y)",
            )

        lado_izquierdo.addWidget(QLabel("Obstáculo"), grid_row + 1, 1)
        lado_izquierdo.addWidget(hacer_input_obstaculo(), grid_row + 1, 2)

        for m in range(len(output_nombres)):
            titulos = QLabel(output_nombres[m])
            self.labels_salida.append(titulos)
            titulos.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.lado_derecho.addWidget(titulos)
            self.salida = QLabel()
            self.salida.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.salidas.append(self.salida)
            self.lado_derecho.addWidget(self.salida)
            self.salida.setObjectName("salidas")
            titulos.setObjectName("titulos")

        self.lado_derecho.addWidget(Solver.hacer_grafica(None, None, None, True))

        for entrada in self.line_edits:
            entrada.textChanged.connect(self.calculo_auto)

        container_footer = QWidget()
        container_footer.setContentsMargins(0, 0, 0, 0)
        logo_img = QLabel()
        logo_img.setAlignment(Qt.AlignmentFlag.AlignLeft)
        container_footer.setLayout(QHBoxLayout())
        container_footer.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        logo_img.setPixmap(QPixmap(str(Path(os.path.join(basedir, "res/logo.png")))))
        copyright_msg = QLabel(
            "Equipo Capicalc (Mateo Sanchez, Santiago Celis y Álvaro Gallo)"
        )
        copyright_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        copyright_msg.setStyleSheet("font-size:10px")

        container_footer.layout().addWidget(logo_img)
        container_footer.layout().addWidget(copyright_msg)
        layout_principal.addWidget(container_footer)

    def obtener_valores(self):
        valores = []
        for lineEdit in self.line_edits:
            texto = lineEdit.text()
            numero = float(texto)
            valores.append(numero)

        return valores

    def on_click_button(self):
        # si no se tienen todos los inputs validos, hacer shortstop
        if not all(
            lineEdit.text() not in ["", "+", "-"] for lineEdit in self.line_edits
        ):
            return

        valores = self.obtener_valores()
        self.solucion = Solver(valores).solucion()
        if len(self.solucion) == 3:
            self.salidas[0].setText(f"{self.solucion[0]}°")
            self.salidas[1].setText(f"{self.solucion[1]}%")
            # hacer del mismo tamaño del plot_placeholder para que no se mueva
            # quitar el placeholder
            self.lado_derecho.itemAt(4).widget().setParent(None)  # type:ignore
            # añadir la grafica
            self.lado_derecho.addWidget(self.solucion[2])
        else:
            # aqui lo inverso: se quita la grafica y se pone el placeholder
            self.lado_derecho.itemAt(4).widget().setParent(None)  # type:ignore
            self.lado_derecho.addWidget(Solver.hacer_grafica(None, None, None, True))
            self.mostrar_error_en_salida("Valores no válidos")

    def mostrar_error_en_salida(self, mensaje):
        for salida in self.salidas:
            salida.setText(mensaje)

    def resetear(self):
        for lineEdits in self.line_edits:
            lineEdits.clear()
        for salida in self.salidas:
            salida.clear()
        self.lado_derecho.itemAt(4).widget().setParent(None)  # type:ignore
        self.lado_derecho.addWidget(Solver.hacer_grafica(None, None, None, True))

    def calculo_auto(self):
        if self.checkbox.isChecked():
            self.on_click_button()
        else:
            self.mostrar_error_en_salida("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication([])

    app.setStyleSheet(Path(os.path.join(basedir, "style.css")).read_text())
    window = VentanaPrincipal()
    window.show()
    app.exec()
