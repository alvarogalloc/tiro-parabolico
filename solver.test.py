from solver import Solver
import math

vart = 1.18
gravity = 9.81
initial_height = 10
final_height = 0

solver = Solver(
    varT=vart,
    gravity=gravity,
    initial_height=initial_height,
    final_height=final_height,
)
print(f"vart: {vart}")
print(f"gravity: {gravity}")
print(f"initial_height: {initial_height}")
print(f"final_height: {final_height}")
print(f"Target Longitude: {solver._computeL()}")

# make a function that recieves a description and a function
print(
    f"""
    initial velocity: {math.sqrt(solver._computeVsquared())} 
    angle: {solver.angle()}
    """
)
