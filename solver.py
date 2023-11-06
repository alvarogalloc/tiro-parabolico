import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as fig
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class Solver:
    def __init__(self):
        # crear plot sin nada, cambiar la figura cada vez que calcule
        self.canvas_plot = FigureCanvas(plt.figure())
        self.hacer_grafica(None, None, True)
        self.distancia_minima_con_el_obstaculo = 1

    def set_valores(self, valores_entrada):
        self.m = valores_entrada[0]
        # agarrar valor absoluto
        self.g = np.abs(valores_entrada[1])
        self.k = valores_entrada[2]
        self.hi = valores_entrada[4]
        self.hf = valores_entrada[3]
        self.l = valores_entrada[5]
        self.coor_x = valores_entrada[6]
        self.coor_y = valores_entrada[7]

        self.Xr = None
        # hacer que solo use angulos positivos cuando el objetivo esta
        # mas alto que el disparador
        if self.hf > self.hi:
            self.min_ang = 0
        else:
            self.min_ang = -90

    def solucion_sin_obstaculo(self, angulo):
        denominator = ((self.hf - self.hi) - self.l * np.tan(np.radians(angulo))) * (
            -2 * np.cos(np.radians(angulo)) ** 2
        )
        if denominator == 0 or denominator < 0:
            return None, None
        solution = (self.g * self.l ** 2) / denominator
        if not solution > 0:
            return None, None
        xr = np.sqrt(self.m * solution / self.k)
        if xr > 1:
            return None, None
        return xr, np.sqrt(solution)

    def hacer_grafica(self, v_inicial, angulo, empty=False):
        # si ya se grafico alguna vez, borrarla
        if self.canvas_plot.figure.axes:
            self.canvas_plot.figure.delaxes(self.canvas_plot.figure.axes[0])
        ax = self.canvas_plot.figure.add_subplot(111)
        self.canvas_plot.figure.set_facecolor("#f3f3f3")
        ax.clear()
        ax.patch.set_alpha(0.5)
        ax.set_facecolor("#f3f3f3")
        ax.grid()
        ax.axis("equal")
        if not empty:
            v_inicial_x = v_inicial * np.cos(np.radians(angulo))
            v_inicial_y = v_inicial * np.sin(np.radians(angulo))
            valores_t = np.linspace(0, self.l / v_inicial_x, 20)
            posiciones_y = (
                self.hi + v_inicial_y * valores_t - (self.g * valores_t ** 2 / 2)
            )
            posiciones_x = v_inicial_x * valores_t

            ax.plot(posiciones_x, posiciones_y)
            if self.coor_x <= self.l:
                # poner un circulo rojo (vision de obstaculo)
                # y en azul su caja de colision
                obstaculo = fig.Circle(
                    (self.coor_x, self.coor_y),
                    self.distancia_minima_con_el_obstaculo,
                    color="red",
                )
                ax.add_patch(obstaculo)
        self.canvas_plot.draw()

    # ahora si se grafica todo el tiro
    def mostrar_tiro(self, v_inicial, angulo):
        v_inicial_x = v_inicial * np.cos(np.radians(angulo))
        v_inicial_y = v_inicial * np.sin(np.radians(angulo))
        valores_t = np.linspace(0, self.l / v_inicial_x, 20)
        posiciones_y = self.hi + v_inicial_y * valores_t - (self.g * valores_t ** 2 / 2)
        posiciones_x = v_inicial_x * valores_t
        plt.plot(posiciones_x, posiciones_y)
        plt.scatter(self.coor_x, self.coor_y, 10, c="red")
        plt.scatter(self.l, self.hf, 10, c="blue")
        plt.show()

    def solucion(self):
        # usar angulo x angulo para quitar calculos innecesarios
        for angulo in range(self.min_ang, 90):
            xr, v_inicial = self.solucion_sin_obstaculo(angulo)
            # en caso de solucion real
            if not (xr and v_inicial):
                continue

            # calcular un minimo valor de t
            # cuando x en t es cercano a coor_x
            v_inicial_x = v_inicial * np.cos(np.radians(angulo))
            v_inicial_y = v_inicial * np.sin(np.radians(angulo))
            min_t = (self.coor_x - self.distancia_minima_con_el_obstaculo) / (
                v_inicial_x
            )
            max_t = (self.coor_x + self.distancia_minima_con_el_obstaculo) / (
                v_inicial_x
            )
            # checar la distancia al obstaculo en este espacio
            # para minimizar iteraciones (1000)
            valores_t = np.linspace(min_t, max_t, 1000)
            posiciones_y = (
                self.hi + v_inicial_y * valores_t - (self.g * valores_t ** 2 / 2)
            )
            posiciones_x = v_inicial_x * valores_t
            distancias_al_obstaculo = np.sqrt(
                (self.coor_x - posiciones_x) ** 2 + (self.coor_y - posiciones_y) ** 2
            )
            tiene_distancias_menores_a_uno = (
                len(
                    np.where(
                        distancias_al_obstaculo < self.distancia_minima_con_el_obstaculo
                    )[0]
                )
                > 0
            )
            if not tiene_distancias_menores_a_uno:
                self.hacer_grafica(np.round(v_inicial, 2), angulo)
                return [angulo, np.round(xr * 100, 2)]
        return []
