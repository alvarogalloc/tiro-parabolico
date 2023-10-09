import numpy as np
import json

class Solver:
    def __init__(self, config_file="test.json"):
        # Carga la configuración desde el archivo JSON
        with open(config_file, 'r') as file:
            config_data = json.load(file)
        
        self.m = config_data["m"]
        self.g = abs(config_data["g"])
        self.l = config_data["l"]
        self.hi = config_data["hi"]
        self.hf = config_data["hf"]
        self.k = config_data["k"]
        self.Xr = None
        self.used_ang = None
        self.min_ang = 0
        self.resultados_formuliniV = self._formuliniV()

    def _formuliniV(self):
        resultados = []
        for ang in range(self.min_ang, 90):
            try:
                denominator = (((self.hf - self.hi) - self.l * np.tan(np.radians(ang))) * (-2 * np.cos(np.radians(ang)) ** 2))
                if denominator == 0 or denominator < 0:
                    continue  # Salta divisiones por cero o negativas
                solution = ((self.g * self.l ** 2) / denominator)
                velocidad = np.sqrt(solution)
                if solution > 0:
                    self.used_ang = ang
                    self.Xr = np.sqrt(self.m * solution / self.k)
                    if self.Xr > 1:
                        continue  # Salta soluciones donde self.Xr sea mayor que 1
                    self.Xr = max(0, min(1, self.Xr))
                    resultados.append([self.used_ang, self.Xr, velocidad])
            except ZeroDivisionError:
                continue
    
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

        # Calcula la posición en incrementos de 0.05 segundos
            tiempo = 0.0
            while tiempo <= tiempo_total:
                posicion_y = velocidad_y * tiempo + (-self.g * tiempo ** 2 / 2)
                posicion_x = velocidad_x * tiempo
                posiciones.append([angulo,[posicion_x, posicion_y]])
                tiempo += 0.001

        return posiciones
   

# Ejemplo de uso

solver = Solver()
solutions_list = solver._posicion_pelota()
solutions_list2 = solver._formuliniV()
for resultados in solutions_list2:
    print(resultados)
# print("Posiciones:")
# for posicion in solutions_list:
#     print(posicion)