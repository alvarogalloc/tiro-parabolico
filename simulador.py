import numpy as np
import matplotlib.pyplot as plt
from test import Solver  # Importa tu clase Solver desde el archivo correspondiente

# Crea una instancia de Solver con los valores de configuración
solver = Solver()

# Calcula los resultados y posiciones
resultados = solver._formuliniV()

# Graficar las trayectorias para diferentes ángulos
for resultado in resultados:
    angulo = resultado[0]
    velocidad = resultado[2]
    radianes = angulo * np.pi / 180
    velocidad_x = velocidad * np.cos(radianes)
    velocidad_y = velocidad * np.sin(radianes)
    tiempo_total = solver.l / velocidad_x
    tiempo = np.linspace(0, tiempo_total, 100)  # Crear un arreglo de tiempos

    # Calcular las posiciones en función del tiempo
    posicion_x = velocidad_x * tiempo
    posicion_y = velocidad_y * tiempo - (0.5 * solver.g * tiempo ** 2)

    # Graficar la trayectoria
    plt.plot(posicion_x, posicion_y, label=f'Ángulo: {angulo}°')

# Configurar el gráfico
plt.xlabel('Posición en X (metros)')
plt.ylabel('Posición en Y (metros)')
plt.legend()
plt.grid()

# Mostrar el gráfico
plt.show()