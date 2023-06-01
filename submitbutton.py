from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton


class SubmitButton(QPushButton):
    def __init__(self):
        super().__init__("START")
        self.setObjectName('SubmitButton')
        self.setDisabled(False)
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
        self.setGraphicsEffect(QGraphicsDropShadowEffect())
        
    def onrelease(self):
        self.setGraphicsEffect(self.getshadow())
