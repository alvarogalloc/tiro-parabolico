import os
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QWidget,
    QCheckBox,
    QPushButton,
    QLineEdit,
)

from test import Solver

basedir = os.path.dirname(__file__)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capicalc")
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.keyPressEvent = self.close_on_esc
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout_principal = QGridLayout(central_widget)
        layout_principal.setColumnStretch(0, 1)
        layout_principal.setColumnStretch(1, 2)
        layout_principal.setColumnStretch(2, 3)
        lado_izquierdo = QGridLayout()
        lado_derecho = QGridLayout()

        boton_ayuda = QPushButton("Ayuda")
        boton_reset = QPushButton("Resetear")
        boton_calcular = QPushButton("Calcular")
        self.checkbox = QCheckBox("Auto")
        label_entrada = QLabel("Valores de Entrada")
        label_salida = QLabel("Valores de Salida")
        output_names = [
            "Ángulo (θ)",
            "Compresión del resorte (Xc)",
        ]
        entrada_nombres = [
            "Masa Balón",
            "Gravedad",
            "Constante",
            "Altura Final",
            "Altura Inicial",
            "Distancia Horizontal",
            "Coordenada x",
            "Coordenada y"
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
        self.line_edits = []

        for element in entrada_nombres:
            grid_row += 1
            lado_izquierdo.addWidget(QLabel(f"{element}"), grid_row, 1)
            entrada = QLineEdit()
            self.line_edits.append(entrada)
            lado_izquierdo.addWidget(entrada, grid_row, 2)

        self.labels_salida = []
        self.salidas = []

        for m in range(len(output_names)):
            titulos = QLabel(output_names[m])
            self.labels_salida.append(titulos)
            titulos.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            lado_derecho.addWidget(titulos)
            salida = QLabel(self.salidas[m] if len(self.salidas) == 2 else '')
            salida.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            lado_derecho.addWidget(salida)

        
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
        valores = self.obtener_valores()
        solucion = Solver(valores)._posicion_pelota()
        print(solucion)
        self.salidas = []
        self.salidas.append(solucion[0]) # angulo
        self.salidas.append(solucion[1]) # compresion

    def close_on_esc(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
   

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(Path(os.path.join(basedir, "style.css")).read_text())

    window = VentanaPrincipal()
    window.show()

    app.exec()

