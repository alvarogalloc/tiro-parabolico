# a class that recieves all the values entered in the inputs and outputs results

# TODO, might reorganize all values in a structure (dataclass)
import math


class Solver:
    def __init__(self, varT, gravity, h0, hf, spring_constant, mass):
        self.varT = varT
        self.gravity = abs(gravity)  # Cambio el valor negativo de la gravedad a positivo
        self.h0 = h0
        self.hf = hf
        self.spring_constant = spring_constant
        self.mass = mass
        # precompute L
        self.L = self._computeL()
        self.used_angle = None

    def _computeL(self):
        return (12 * self.varT ** 3) + (5 * self.varT ** 2) + (3 * self.varT) + 10

    def _computeVsquared(self):
        # by default None
        solution = math.nan
        angle = None
        for angle in range(90):
            solution = (self.L ** 2 * self.gravity) / (
                2
                * math.cos(math.radians(angle)) ** 2
                * ((self.hf - self.h0) - self.L * math.tan(math.radians(angle)))
            )
            if solution != math.nan:
                break
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
        return Xc
    
    def velocidad_inicial(self):
        solution = self._computeVsquared()
        return math.sqrt(solution)
    
        
