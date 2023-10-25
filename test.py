import numpy as np
import json


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
        self.resultados_formuliniV = self._formuliniV()

    def _formuliniV(self):
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

    def _posicion_pelota(self):
        posiciones = []  # Lista para almacenar las posiciones en función del tiempo

        for resultado in self.resultados_formuliniV:
            angulo = resultado[0]
            velocidad = resultado[2]
            radianes = angulo * np.pi / 180
            velocidad_x = velocidad * np.cos(radianes)
            velocidad_y = velocidad * np.sin(radianes)
            tiempo_total = self.l / velocidad_x
            Xr = resultado[1]

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
                    break  # Sale del bucle si la posición está dentro del rango del obstáculo

                tiempo += 0.0001

            if not obstaculo_encontrado and Xr > 0:
                Xr = Xr * 100
                Xr = round(Xr, 1)
                posiciones.append([angulo, Xr])
                break  # Sale del bucle si no se encontró coincidencia
        
        return posiciones[0] if posiciones else []


# Ejemplo de uso
