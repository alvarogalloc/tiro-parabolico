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
        layout_principal.setColumnStretch(1, 1)
        lado_izquierdo = QGridLayout()
        lado_derecho = QGridLayout()
        
        boton_ayuda = QPushButton("Ayuda", self)
        boton_reset = QPushButton("Resetear")
        boton_calcular = QPushButton("Calcular")
        self.checkbox = QCheckBox()
        label_entrada = QLabel("Valores de Entrada")
        label_salida = QLabel("Valores de Salida")
        output_names = [
            "Angulo (θ)",
            "Compresión del resorte (Xc)",
        ]
        entrada_nombres = [
            "Masa Balon",
            "Gravedad",
            "Constante",
            "Altura Final",
            "Altura Incial",
            "Distancia Horizontal",
            "Obstaculo"
        ]
        
        lado_izquierdo.addWidget(label_entrada, 0, 2)
        
        lado_derecho.addWidget(label_salida, 0, 1)
        
        lado_izquierdo.addWidget(boton_ayuda, 0, 0)

        lado_izquierdo.addWidget(self.checkbox, 9, 1)
        self.checkbox.setText("Auto")
        
        lado_izquierdo.addWidget(boton_reset, 8, 1)
        
        lado_izquierdo.addWidget(boton_calcular, 8, 2)

        layout_principal.addLayout(lado_izquierdo, 0, 0)
        layout_principal.addLayout(lado_derecho, 0, 1)
        
        grid_row = 0
        for element in entrada_nombres:
            grid_row += 1
            lado_izquierdo.addWidget(QLabel(f"{element}"), grid_row, 1)
            entrada = QLineEdit()  # crea un widget QLineEdit
            lado_izquierdo.addWidget(entrada, grid_row, 2)  # agrega el widget al layout
        

        for m in range(len(output_names)):
            lado_derecho.addWidget(QLabel(output_names[m]), m + 1, 0)
            salida = QLabel()
            lado_derecho.addWidget(salida, m + 1, 1)
        
    def close_on_esc(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(Path(os.path.join(basedir, "style.css")).read_text())

    window = VentanaPrincipal()
    window.show()

    app.exec()





