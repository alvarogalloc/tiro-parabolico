import tkinter as tk

def nombredesanchez():
    return 'mateo'

def mandarMsg(msg):
    print(msg)

def multiplicaldosnumelos(x, y):
    return x * y

def main():
    sanchez = nombredesanchez()
    mandarMsg("hola")
    resultado = multiplicaldosnumelos(10,20)
    print(f"{sanchez} saco el resultado y es {resultado}")

if __name__ == "__main__":
    main()
