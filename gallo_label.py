# Librerias de python
import os
from PyQt6.QtCore import Qt, QSize

# De Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QToolButton


def make_help_button():
    btn = QToolButton()
    btn.setFixedSize(100, 100)
    btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    btn.setIcon(QIcon("ayuda.svg"))
    btn.setText("Ayuda")
    btn.setIconSize(QSize(50, 50))

    def click_handler():
        print("button clicked")

    btn.clicked.connect(click_handler)

    # style a button
    btn.setStyleSheet(
        """
        border: none;
        color: white;
        font-size: 16px;
        font-weight: bold;
        """
    )
    return btn


# Nuestros Módulos

basedir = os.path.dirname(__file__)


def make_title(text, font_size=16) -> QLabel:
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
    return label


def make_styled_input(
    placeholder: str, font_size: int = 20, padding: int = 10
) -> QLineEdit:
    input = QLineEdit()
    input.setPlaceholderText(placeholder)
    input.setStyleSheet(
        f"""
        border: none;
        background-color: #1f1f1f;
        border-bottom: 2px solid white;
        padding: {padding}px;
        font-size: {font_size}px;
        border-radius: 5px;
        color: white;
        """
    )
    return input


def make_header() -> QWidget:
    header_container = QWidget()
    # 20% de la pantalla
    # header_container.setMaximumHeight(int(window_height * 0.2))
    header_container_layout = QGridLayout()
    left_container = QWidget()
    left_container.setLayout(QHBoxLayout())

    help_button = make_help_button()
    title = make_title("Inputs", 32)
    output_title = make_title("Outputs", 32)

    left_container.layout().addWidget(help_button)
    left_container.layout().addWidget(title)
    header_container_layout.addWidget(left_container, 0, 0)
    header_container_layout.addWidget(output_title, 0, 1)
    header_container.setLayout(header_container_layout)
    return header_container


def make_inputs() -> QWidget:
    inputs_container = QWidget()
    # todo
    # 60% de la pantalla
    # inputs_container.setMaximumHeight(int(window_height * 0.6))
    layout = QVBoxLayout()
    prompts = [
        "Masa del Balón (m)",
        "Gravedad (g)",
        "Constante del resorte (k)",
        "Altura del suelo al objetivo (hf)",
        "Altura del suelo al balón (h0)",
        "Distanca horizontal al objetivo (L)",
    ]
    for prompt in prompts:
        layout.addWidget(make_styled_input(prompt))
    #  "Coordenadas de un obstáculo (x, y)",
    label_container = QWidget()
    label_container.setLayout(QVBoxLayout())
    label_container.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
    label = make_title("Coordenadas de un obstáculo", 16)
    label_container.layout().addWidget(label)
    inputs = QWidget()
    inputs.setLayout(QHBoxLayout())
    inputs.layout().addWidget(make_styled_input("x: ", 16, 3))
    inputs.layout().addWidget(make_styled_input("y: ", 16, 3))
    label_container.layout().addWidget(inputs)
    layout.addWidget(label_container)

    inputs_container.setLayout(layout)
    return inputs_container


class VentanaPrincipal(QMainWindow):
    root: QWidget

    def __init__(self):
        # Es como llamar a QMainWindow.__init__()
        super().__init__()
        self.setWindowTitle("Capicalc")
        self.root = QWidget()
        # center the content and make it 80% of the screen
        root_layout = QVBoxLayout()
        # do not center the content
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.root.setLayout(root_layout)

        self.add_to_root(make_header(), False)
        content = QWidget()
        content_layout = QGridLayout()
        content_layout.addWidget(make_inputs(), 0, 0)
        content_layout.addWidget(make_inputs(), 0, 1)
        content.setLayout(content_layout)
        self.add_to_root(content, False)

        self.setCentralWidget(self.root)

    def add_to_root(self, widget: QWidget, border: bool = False):
        self.root.layout().addWidget(widget)
        if border:
            widget.setStyleSheet("border: 1px solid white;")


app = QApplication([])
# estilos
# app.setStyleSheet(Path(os.path.join(basedir, "style.css")).read_text())

window = VentanaPrincipal()
window.show()
window.showFullScreen()

app.exec()
