# a class that recieves all the values entered in the inputs and outputs results

# TODO, might reorganize all values in a structure (dataclass)
import math


class Solver:
    def __init__(self, varT, gravity, h0, hf, spring_constant, mass):
        self.varT = varT
        # Cambio el valor negativo de la gravedad a positivo
        self.gravity = abs(gravity)
        self.h0 = h0
        self.hf = hf
        self.spring_constant = spring_constant
        self.mass = mass
        # precompute L
        self.L = self._computeL()
        self.used_angle = None

        # el simulador cuando la altura inicial es 0, no permite angulos menores
        # a 25
        # sera 0 si la altura inicial no es cero, de otra manera sera 25
        self.min_angle = 0 if h0 != 0 else 1

    def _computeL(self):
        return (12 * self.varT ** 3) + (5 * self.varT ** 2) + (3 * self.varT) + 10

    def _computeVsquared(self):
        # by default None
        solution = math.nan
        angle = None
        for angle in range(self.min_angle, 90):
            try:
                solution = (self.L ** 2 * self.gravity) / (
                    2
                    * math.cos(math.radians(angle)) ** 2
                    * ((self.hf - self.h0) - self.L * math.tan(math.radians(angle)))
                )
                # hacer que el resultado se pueda probar en el simulador
                # print(f"{angle} {solution}")
                # no estoy seguro pero parece que al darnos numeros negativos
                # significa que es una respuesta real.
                # hacer que el resultado se pueda probar en el simulador
                # (el maximo en el simulador es 30)
                if solution < 0:
                    break
            except ZeroDivisionError:
                continue

            # if not a solution just go to the next iteration

        self.used_angle = angle
        return abs(solution)

    def angle(self):
        if self.used_angle is None:
            self._computeVsquared()
        return self.used_angle

    ## TODO: we need the new constraints to
    ## calculate the angle and the spring compression
    def spring_compression(self):
        solution = self._computeVsquared()
        # spring cannt be compressed more than 1 metre
        Xc = math.sqrt(self.mass * solution / self.spring_constant)
        if Xc > 1:
            self.min_angle += 1
            Xc = self.spring_compression()
        return Xc

    def velocidad_inicial(self):
        solution = self._computeVsquared()
        return math.sqrt(solution)
