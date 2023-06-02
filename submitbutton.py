from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QPushButton


class SubmitButton(QPushButton):
    def __init__(self):
        super().__init__("START")
        self.setObjectName('SubmitButton')
        self.setDisabled(True)
        # self.setGraphicsEffect(self.getshadow())
        # self.setFixedSize(100, 25)
        self.pressed.connect(self.onpressed)
        self.released.connect(self.onrelease)
    
    def getshadow(self):
        shadow = QGraphicsDropShadowEffect()
        # # Set the color of the shadow
        # green = QColor(83, 179, 83, 255)
        # shadow.setColor(green)
        return shadow
    
    def onpressed(self):
        # self.setGraphicsEffect(QGraphicsDropShadowEffect())
        return
        
    def onrelease(self):
        # self.setGraphicsEffect(self.getshadow())
        return
