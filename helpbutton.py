from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QGridLayout, QPushButton, QWidget

class HelpButton(QPushButton):
    def __init__(self):
        super().__init__("Ayuda")
        self.setIcon(QIcon("help.png"))
        self.clicked.connect(self.onclick)

    def onclick(self):
        helpwindowlayout = QGridLayout()
        helpwindow = QWidget()



