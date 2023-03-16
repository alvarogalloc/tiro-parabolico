import tkinter as tk

root = tk.Tk()
root.title("calculadora pituda")

 root.attributes("-fullscreen", True)
root.geometry("400x400+200+200")
root.resizable(False, False)

frm = tk.Frame(root, padding=10)

button = tk.Button(root, text="Hola")
button.pack()

root.mainloop()
