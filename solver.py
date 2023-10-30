import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Solver:
    def __init__(self, valores):
        self.valores_entrada = valores
        self.m = self.valores_entrada[0]
        # agarrar valor absoluto
        self.g = np.abs(self.valores_entrada[1])
        self.k = self.valores_entrada[2]
        self.hi = self.valores_entrada[4]
        self.hf = self.valores_entrada[3]
        self.l = self.valores_entrada[5]
        self.coor_x = self.valores_entrada[6]
        self.coor_y = self.valores_entrada[7]
        self.Xr = None
        self.used_ang = None
        self.min_ang = -90
        self.resultados_formulaV = self._formulaV()

    def _formulaV(self):
        resultados = []
        for ang in range(self.min_ang, 90):
            denominator = ((self.hf - self.hi) - self.l * np.tan(np.radians(ang))) * (
                -2 * np.cos(np.radians(ang)) ** 2
            )
            if denominator == 0 or denominator < 0:
                continue  # Salta divisiones por cero o negativas
            solution = (self.g * self.l ** 2) / denominator
            velocidad = np.sqrt(solution)
            if solution > 0:
                self.used_ang = ang
                self.Xr = np.sqrt(self.m * solution / self.k)
                if self.Xr > 1:
                    continue  # Salta soluciones donde self.Xr sea mayor que 1
                self.Xr = max(0, min(1, self.Xr))
                resultados.append([self.used_ang, self.Xr, velocidad])

        return resultados

    def create_plot_widget(self, posiciones_x, posiciones_y, empty = False):
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        # ax.figure.set_figwidth
        ax.figure.set_facecolor("#f3f3f3")
        ax.patch.set_alpha(0.5)
        ax.set_facecolor("#f3f3f3")
        ax.grid()
        ax.axis("equal")
        if not empty:
            ax.plot(posiciones_x, posiciones_y)
            if self.coor_x <= self.l:
                ax.scatter(self.coor_x, self.coor_y, 6, color="red")
        canvas.draw()
        plt.close(figure)
        return canvas

    def _posicion_pelota(self):
        posiciones = []  # Lista para almacenar las posiciones en función del tiempo
        widget_of_the_plot = None

        for resultado in self.resultados_formulaV:
            angulo = resultado[0]
            velocidad = resultado[2]
            radianes = angulo * np.pi / 180
            velocidad_x = velocidad * np.cos(radianes)
            velocidad_y = velocidad * np.sin(radianes)
            tiempo_total = self.l / velocidad_x
            Xr = resultado[1]

            # Calcula la posición en incrementos de 0.02 segundos
            tiempo_values = np.arange(0, tiempo_total + 0.02, 0.02)

            # Posiciones en x y y
            posiciones_y = self.hi + velocidad_y * tiempo_values - (self.g * tiempo_values**2 / 2)
            posiciones_x = velocidad_x * tiempo_values

            # Distancias del obstáculo a cada punto de la trayectoria
            distances = np.sqrt((posiciones_x - self.coor_x)**2 + (posiciones_y - self.coor_y)**2)

            # encuentra el primer punto donde la distancia es menor o igual a 2, que es el radio del obstáculo
            obstacle_index = np.where(distances <= 2)[0]

            # si no encontró un obstáculo, guarda el ángulo y la compresión funcional
            if not obstacle_index.size > 0 and Xr > 0:
                Xr = Xr * 100
                Xr = round(Xr, 1)
                posiciones.append([angulo, Xr])
                widget_of_the_plot = self.create_plot_widget(posiciones_x, posiciones_y)
                break

        # que regrese un angulo y compresion funcional ademas de la grafica del disparo
        return (
            [posiciones[0][0], posiciones[0][1], widget_of_the_plot]
            if posiciones
            else []
        )

