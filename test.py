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

    def create_plot_widget(self, posiciones_x, posiciones_y):
        figure = plt.figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        ax.plot(posiciones_x, posiciones_y)
        
        # ax.xlabel("Posición en X (metros)")
        # ax.ylabel("Posición en Y (metros)")
        # ax.title("")
        ax.grid()
        ax.axis("equal")
        canvas.setStyleSheet("background-color:transparent;")
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

            posiciones_x = []
            posiciones_y = []
            # Calcula la posición en incrementos de 0.05 segundos
            tiempo = 0.0
            obstaculo_encontrado = False

            while tiempo <= tiempo_total:
                posicion_y = velocidad_y * tiempo + (-self.g * tiempo ** 2 / 2)
                posicion_x = velocidad_x * tiempo

                # Verifica si la posición está dentro del rango del obstáculo
                if (self.coor_x - 0.5 <= posicion_x <= self.coor_x + 0.5) and (
                    self.coor_y - 0.5 <= posicion_y <= self.coor_y + 0.5
                ):
                    obstaculo_encontrado = True
                    break

                posiciones_x.append(posicion_x)
                posiciones_y.append(posicion_y)
                tiempo += 0.0001

            if not obstaculo_encontrado and Xr > 0:
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

    # Mostrar el gráfico


# Ejemplo de uso
