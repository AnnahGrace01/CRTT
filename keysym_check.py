import tkinter as tk

root = tk.Tk()
root.title("KeySym Check")

t = tk.StringVar(value="None")
l = tk.Label(root, textvariable=t)
l.pack()

def check_keysym(e):
	print(vars(e))
	t.set(e.keysym)

root.bind("<KeyPress>", check_keysym)
root.mainloop()