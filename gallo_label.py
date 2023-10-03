# Librerias de python
import os
from typing import Callable
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
from PyQt6.QtGui import QColor, QIcon, QPainter
from PyQt6.QtWidgets import QToolButton


def new_color(hexstring: str):
    return QColor.fromString(hexstring)


colors = {
    "bg": "#0249a8",
    "white": "#ffffff",
    "btn-start": "#98f71e",
    "btn-restart": "#f73605",
    "input-outline-inactive": "#7f9efa",
}


def colorize_icon(icon, color):
    pixmap = icon.pixmap(icon.actualSize(QSize(50, 50)))
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)


def make_help_button(callback):
    btn = QToolButton()
    btn.setFixedSize(100, 100)
    btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
    btn.setIcon(
        colorize_icon(QIcon(basedir + "/res/ayuda.svg"), new_color(colors["white"]))
    )
    btn.setText("Ayuda")
    btn.setIconSize(QSize(50, 50))


    btn.clicked.connect(callback)

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


def input_styles(padding, font_size):
    return f"""
        border: none;
        border: 3px solid {colors['white']};
        padding: {padding}px;
        font-size: {font_size}px;
        color: {colors['white']};
    """


def make_styled_input(
    label: str,
    placeholder: str,
    font_size: int = 20,
    padding: int = 10,
    on_change=lambda x: x,
) -> tuple[QWidget, Callable[[], str]]:
    div = QWidget()
    div_layout = QGridLayout()
    div_layout.setContentsMargins(0, 0, 0, 0)
    div_layout.setColumnStretch(0, 1)
    div_layout.setColumnStretch(1, 1)
    label_widget = make_title(label, font_size)
    input = QLineEdit()
    input.textChanged.connect(on_change)
    input.setPlaceholderText(placeholder)
    input.setStyleSheet(input_styles(padding, font_size))
    div_layout.addWidget(label_widget, 0, 0)
    div_layout.addWidget(input, 0, 1)
    div.setLayout(div_layout)
    return div, input.text


def make_header(calcular) -> QWidget:
    header_container = QWidget()
    # 20% de la pantalla
    # header_container.setMaximumHeight(int(window_height * 0.2))
    header_container_layout = QGridLayout()
    left_container = QWidget()
    left_container.setLayout(QHBoxLayout())

    help_button = make_help_button(calcular)
    title = make_title("Inputs", 32)
    output_title = make_title("Outputs", 32)

    left_container.layout().addWidget(help_button)
    left_container.layout().addWidget(title)
    header_container_layout.addWidget(left_container, 0, 0)
    header_container_layout.addWidget(output_title, 0, 1)
    header_container.setLayout(header_container_layout)
    return header_container


def make_inputs() -> tuple[QWidget, dict[str, Callable[[], str]]]:
    inputs_container = QWidget()
    # todo
    # 60% de la pantalla
    # inputs_container.setMaximumHeight(int(window_height * 0.6))
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    prompts = [
        "Masa del Balón",
        "Gravedad",
        "Constante del resorte",
        "Altura del suelo al objetivo",
        "Altura del suelo al balón",
        "Distanca horizontal al objetivo",
    ]
    placeholders = ["m", "g", "k", "hf", "h0", "L", "x", "y"]
    getters = {}
    for i in range(len(prompts)):
        # returns the input and the function to get the text at any time
        current_input, get_text = make_styled_input(prompts[i], f"({placeholders[i]})")
        getters[placeholders[i]] = get_text
        layout.addWidget(current_input)

    #  "Coordenadas de un obstáculo (x, y)",
    label_container = QWidget()
    obstacle_layout = QGridLayout()
    obstacle_layout.setContentsMargins(0, 0, 0, 0)
    obstacle_layout.setColumnStretch(0, 1)
    obstacle_layout.setColumnStretch(1, 1)

    label_container.setLayout(obstacle_layout)
    label_container.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
    label = make_title("Coordenadas de un obstáculo", 20)
    label_container.layout().addWidget(label)

    inputs = QWidget()
    obstacle_inputs_layout = QGridLayout()
    obstacle_inputs_layout.setColumnStretch(0, 1)
    obstacle_inputs_layout.setColumnStretch(1, 1)
    obstacle_inputs_layout.setContentsMargins(0, 0, 0, 0)
    x_input = QLineEdit()
    # placeholders[6] = "x"
    getters[placeholders[6]] = x_input.text
    x_input.setStyleSheet(input_styles(10, 20))
    x_input.setPlaceholderText("x:")
    y_input = QLineEdit()
    # placeholders[6] = "y"
    getters[placeholders[7]] = y_input.text
    y_input.setStyleSheet(input_styles(10, 20))
    y_input.setPlaceholderText("y:")
    obstacle_inputs_layout.addWidget(x_input, 0, 0)
    obstacle_inputs_layout.addWidget(y_input, 0, 1)

    inputs.setLayout(obstacle_inputs_layout)
    label_container.layout().addWidget(inputs)
    layout.addWidget(label_container)

    inputs_container.setLayout(layout)
    return inputs_container, getters


def make_outputs():
    outputs_container = QWidget()
    layout = QVBoxLayout()
    layout.setDirection(QVBoxLayout.Direction.TopToBottom)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    labels = ["Ángulo", "Compresión del resorte"]
    results = [1, 2]
    for i in range(2):
        element = QWidget()
        element_layout = QHBoxLayout()
        element_layout.addWidget(make_title(labels[i], 30))
        label = make_title(str(results[i]), 20)
        label.setFixedWidth(200)
        element_layout.addWidget(label)
        element.setLayout(element_layout)
        layout.addWidget(element)
    outputs_container.setLayout(layout)
    return outputs_container


class VentanaPrincipal(QMainWindow):
    root: QWidget
    getters: dict[str, Callable[[], str]]

    def __init__(self):
        # Es como llamar a QMainWindow.__init__()
        super().__init__()
        screen_size = QApplication.primaryScreen().size()
        # Set the size of the main window to the screen resolution.
        self.resize(screen_size)

        self.setWindowTitle("Capicalc")
        self.root = QWidget()
        # center the content and make it 80% of the screen
        root_layout = QVBoxLayout()
        # do not center the content
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.root.setLayout(root_layout)

        self.add_to_root(make_header(self.calcular), False)
        content = QWidget()
        content.setMaximumWidth(int(self.width() * 0.90))
        content_layout = QGridLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.setColumnStretch(0, 1)
        content_layout.setColumnStretch(1, 1)
        inputs, self.getters = make_inputs()
        print(self.getters.keys())
        content_layout.addWidget(inputs, 0, 0)
        content_layout.addWidget(make_outputs(), 0, 1)
        content.setLayout(content_layout)
        self.add_to_root(content, True)

        self.root.setStyleSheet(f"background-color: {colors['bg']};")
        self.setCentralWidget(self.root)

    def add_to_root(self, widget: QWidget, border: bool = False):
        self.root.layout().addWidget(widget)
        if border:
            widget.setStyleSheet("border: 1px solid white;")

    
    def calcular(self):
        print(self.getters['m']())
        


app = QApplication([])
# estilos
# app.setStyleSheet(Path(os.path.join(basedir, "style.css")).read_text())

window = VentanaPrincipal()
window.show()
window.showFullScreen()

app.exec()
