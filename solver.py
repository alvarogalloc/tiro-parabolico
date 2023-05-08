# a class that recieves all the values entered in the inputs and outputs results

# TODO, might reorganize all values in a structure (dataclass)
import math


class Solver:
    def __init__(
        self,
        varT: float,
        gravity: float,
        initial_height: float,
        final_height: float,
        # spring_constant: float,
        # mass: float,
    ) -> None:
        self.varT = varT
        # if given negative gravity,
        # change it to positive
        self.gravity = abs(gravity)
        self.initial_height = initial_height
        self.final_height = final_height

        # not needed for now
        # self.spring_constant = spring_constant
        # self.mass = mass
        self.used_angle = None

        # precompute L
        self.L = self._computeL()

    def _computeL(self):
        return (12 * self.varT ** 3) + (5 * self.varT ** 2) + (3 * self.varT) + 10

    def _computeVsquared(self):
        # by default None
        solution = math.nan
        angle = 0
        for angle in range(90):
            solution = (self.L ** 2 * self.gravity) / (
                2
                * math.cos(angle) ** 2
                * (
                    (self.final_height - self.initial_height)
                    - self.L * math.tan(angle)
                )
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
        # spring cannt be compressed more than 1 metre
        return 
