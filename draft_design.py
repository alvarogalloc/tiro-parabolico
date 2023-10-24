import os
from pathlib import Path
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QRegularExpression, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QWidget,
    QCheckBox,
    QPushButton,
    QLineEdit,
    QVBoxLayout,
)
from PyQt6.QtGui import  QDoubleValidator, QRegularExpressionValidator, QIcon, QAction


from test import Solver

basedir = os.path.dirname(__file__)

def restringir_input(widget, aceptar_negativos=False):
    input_validator = QDoubleValidator()
    input_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
    if not aceptar_negativos:
        input_validator.setBottom(0)
    widget.setValidator(input_validator)
            

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capicalc")
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.keyPressEvent = self.close_on_esc
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        svg_path = os.path.join(current_dir, 'res', 'ayuda.svg')

        layout_principal = QGridLayout(central_widget)
        layout_principal.setColumnStretch(0, 1)
        layout_principal.setColumnStretch(1, 2)
        layout_principal.setColumnStretch(2, 3)
        lado_izquierdo = QGridLayout()
        lado_derecho = QGridLayout()

        for layout in [lado_izquierdo, lado_derecho]:
            layout.setContentsMargins(0,0,0,0)

        
        boton_ayuda = QtWidgets.QToolButton()
        boton_ayuda.setStyleSheet("background-color: transparent; border: none; margin-left: 40px; margin-right: 40px;")
        boton_ayuda.setIconSize(QSize(40,40))
        etiqueta_ayuda = QLabel("Ayuda")
        etiqueta_ayuda.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout_boton_ayuda = QVBoxLayout()
        layout_boton_ayuda.addWidget(boton_ayuda)
        layout_boton_ayuda.addWidget(etiqueta_ayuda)
        layout_boton_ayuda.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout_boton_ayuda.setContentsMargins(0, 0, 0, 0)
        widget_boton_ayuda = QWidget()
        widget_boton_ayuda.setLayout(layout_boton_ayuda)
        boton_ayuda.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        
        boton_reset = QPushButton("Resetear")
        boton_calcular = QPushButton("Calcular")
        self.checkbox = QCheckBox("Auto")
        label_entrada = QLabel("Valores de Entrada")
        label_salida = QLabel("Valores de Salida")
        self.line_edits = []
        output_nombres = [
            "Ángulo (θ)",
            "Compresión del resorte (Xc)",
        ]
        entrada_nombres = [
            "Masa Balón",
            "Gravedad",
            "Constante",
            "Altura Final",
            "Altura Inicial",
            "Distancia Horizontal"
        ]
        
        placeholders = [
            "Kilogramos",
            "metros/segundos^2",
            "Newton/metros",
            "metros",
            "metros",
            "metros",
        ]

        label_entrada.setObjectName("label_entrada")
        label_salida.setObjectName("label_salida")

        layout_principal.addWidget(label_entrada, 0, 1)
        layout_principal.addWidget(label_salida, 0, 2)
        layout_principal.addWidget(boton_ayuda, 0, 0)

        lado_izquierdo.addWidget(self.checkbox, 10, 1)
        lado_izquierdo.addWidget(boton_reset, 9, 1)
        lado_izquierdo.addWidget(boton_calcular, 9, 2)

        layout_principal.addLayout(lado_izquierdo, 1, 1)
        layout_principal.addLayout(lado_derecho, 1, 2)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_entrada.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_salida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_row = 0
        boton_calcular.clicked.connect(self.on_click_button)
        boton_reset.clicked.connect(self.resetear)
        
        self.checkbox.stateChanged.connect(self.calculo_auto)
        
        boton_ayuda.setDefaultAction(QAction(QIcon(svg_path), "Ayuda", self))

        
        for n in range(len(entrada_nombres)):
            grid_row += 1
            lado_izquierdo.addWidget(QLabel(f"{entrada_nombres[n]}"), grid_row, 1)
            entrada = QLineEdit()
            self.line_edits.append(entrada)
            lado_izquierdo.addWidget(entrada, grid_row, 2)
            entrada.setPlaceholderText(placeholders[n])
            if n not in [3,4]:
                restringir_input(entrada)
            else:
                restringir_input(entrada, True)

        self.labels_salida = []
        self.salidas = []

        # obstaculo en x y y
        def hacer_input_obstaculo (): 
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
            return container_obstaculo
            
        lado_izquierdo.addWidget(QLabel("Obstáculo"), grid_row + 1, 1)
        lado_izquierdo.addWidget(hacer_input_obstaculo(), grid_row + 1, 2)

        for m in range(len(output_nombres)):
            titulos = QLabel(output_nombres[m])
            self.labels_salida.append(titulos)
            titulos.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            lado_derecho.addWidget(titulos)
            self.salida = QLabel()
            self.salida.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.salidas.append(self.salida)
            lado_derecho.addWidget(self.salida)

        for entrada in self.line_edits:
                entrada.textChanged.connect(self.calculo_auto)
                
    def obtener_valores(self):
        valores = []
        for lineEdit in self.line_edits:
            texto = lineEdit.text()
            try:
                numero = float(texto)
                valores.append(numero)
            except ValueError:
                print(f"No se pudo convertir a número: {texto}")

        return valores 
    
    def on_click_button(self):
        if all(lineEdit.text() for lineEdit in self.line_edits):
            valores = self.obtener_valores()
            try:
                self.solucion = Solver(valores)._posicion_pelota()
                for m in range(len(self.solucion)):
                    self.salidas[m].setText(str(self.solucion[m]))
            except IndexError:
                self.mostrar_error_en_salida("Valores no válidos")
        else:
            print("Asegúrate de que todos los campos estén completos.")
            
    def mostrar_error_en_salida(self, mensaje):
        for salida in self.salidas:
            salida.setText(mensaje)

            
    def resetear(self):
        for lineEdits in self.line_edits:
            lineEdits.clear()
        for salida in self.salidas:
            salida.clear()
        
    def calculo_auto(self):
        if all(lineEdit.text() for lineEdit in self.line_edits):
            if self.checkbox.isChecked():
                self.on_click_button()
        else:
            self.mostrar_error_en_salida("")
                           
    
    def close_on_esc(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
   


if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(Path(os.path.join(basedir, "style.css")).read_text())

    window = VentanaPrincipal()
    window.show()

    app.exec()

