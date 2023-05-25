import sys  

from PyQt6.QtGui import QColor

from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QLabel,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QWidget,
    QCheckBox,
    QButtonGroup
)
from pathlib import Path

class SubmitButton(QPushButton):
    def __init__(self):
        super().__init__("START")
        self.setObjectName('SubmitButton')
        self.setGraphicsEffect(self.getshadow())
        self.setFixedSize(100, 25)
        self.pressed.connect(self.onpressed)
        self.released.connect(self.onrelease)
    
    def getshadow(self):
        shadow = QGraphicsDropShadowEffect()
        # Set the color of the shadow
        shadow.setColor(QColor(83, 179, 83, 255))
        # Set the offset of the shadow
        shadow.setOffset(0, 3)
        return shadow
    
    def onpressed(self):
        self.setGraphicsEffect(None)
        
    def onrelease(self):
        self.setGraphicsEffect(self.getshadow())
        

from PyQt6.QtGui import (
    QFont,
)
from PyQt6 import (
    QtWidgets,
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QtWidgets.QMainWindow):
        
    def __init__(self):
        super().__init__()
        
    
        self.setWindowTitle("Widgets App")
        self.line_edit = [None] # crea una lista vacía para despues rellanarla con los valores de entrada
    
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
            widget = QLineEdit() # crea un widget QLineEdit
            layout.addWidget(widget, n + 1, 1) # agrega el widget al layout
            self.line_edit.append(widget) # añade el widget a la lista
            widget.editingFinished.connect(lambda w=widget, n=n: self.imprimir_texto(n, w)) #Es lo que hace que se actialize cada que cambias de qlineedit

    
        
        output_names = {
            0: "Angulo (θ)",
            1: "Compresión del resorte (Xc)",
            2: "Velocidad inicial (Vo)",
        }
        reultado_angulo = "hola"
        resultado_resorte = "hola"
        resultado_velocidad = "hola"
        resultados = {
            0: reultado_angulo,
            1: resultado_resorte,
            2: resultado_velocidad,
        }
        for m in range (3):
            layout.addWidget(QLabel(f"{output_names[m]}"), m+1, 3)
            layout.addWidget(QLabel(f"{resultados[m]}"), m+1, 4)
        

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
        
    #Esta es la funcion que hace que se impriman los valores 
    def imprimir_texto(self, n, widget):
        self.line_edit = ["variabel_t", "gravedad", "altura_inicial", "altura_final", "constante", "masa"]
        text = widget.text()
        print(f"{n}: {self.line_edit[n]} - {text}")
    
    #Abre la ventana de ayuda
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

app = QApplication([])
app.setStyleSheet(Path('style.css').read_text())

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


window = MainWindow()
window.show()

app.exec()
