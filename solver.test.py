from solver import Solver
import math

vart = 0.746
gravity = 9.81
initial_height = 1
final_height = 0

solver = Solver(
    varT=vart,
    gravity=gravity,
    h0=initial_height,
    hf=final_height,
    spring_constant=0,
    mass=0,
)
print(f"vart: {vart}")
print(f"gravity: {gravity}")
print(f"initial_height: {initial_height}")
print(f"final_height: {final_height}")
print(f"Target Longitude: {solver._computeL()}")

# make a function that recieves a description and a function
print(
    f"""
    initial velocity: {solver.velocidad_inicial()} 
    angle: {solver.angle()}
    """
)
