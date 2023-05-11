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
        

class HelpButton(QPushButton):
    def __init__(self, text, callback):
        super().__init__(text)
        self.clicked.connect(self.show_help)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")  

        # layout = QGridLayout()

        # action_button = QPushButton("calcular")
        # input_names = {
        #     0: "Variable t",
        #     1: "Gravedad (g)",
        #     2: "Altura Inicial (h0)",
        #     3: "Altura Final (hf)",
        #     4: "Constante del Resorte (k)",
        # }
        # for n in range(5):
        #     layout.addWidget(QLabel(f"ingresa valor {input_names[n]}"), n+1, 0)
        #     layout.addWidget(QLineEdit(), n+1, 1)

        # layout.addWidget(action_button, 6, 0, 1, 2)
        # widget = QWidget()
        # widget.setLayout(layout)
        button = SubmitButton()
        
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(button)


app = QApplication(sys.argv)
app.setStyleSheet(Path('style.css').read_text())
window = MainWindow()
window.show()

app.exec()
