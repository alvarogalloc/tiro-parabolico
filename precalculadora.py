import math

print("Dame h0 y L")
GRAVITY = -9.81
L = float(input("Ingresa L (metros): "))
H0 = float(input("Ingresa altura inicial (metros): "))
HF = 0
# el modulo math solo acepta el angulo en radianes
ANGLE = math.radians(45)
v = math.sqrt(
    (2 * (L ** 2) * GRAVITY * (math.cos(ANGLE) ** 2))
    / ((HF - H0) - math.tan(ANGLE) * L)
)
# por ahora mejor no iterar el angulo
# for i in range(1,90):
#     print(f"trying {i} as angle")
#     ANGLE = math.radians(i)
#     v = math.sqrt(
#         (2 * (L ** 2) * GRAVITY * (math.cos(ANGLE) ** 2))
#         / ((HF - H0) - math.tan(ANGLE) * L)
#     )

print(f"la velocidad inicial (v0) es igual a: {v}")
