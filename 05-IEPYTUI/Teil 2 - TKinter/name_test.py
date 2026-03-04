import tkinter as tk
from tkinter import ttk

def main():
    # Hauptfenster erstellen:
    root = tk.Tk()
    root.title("Einfaches TKInter-Fenster")
    root.geometry("400x300")

    # Label-Widget erstellen:
    label = tk.Label(root, text="Hallo Welt!")
    label.pack()  # Das Label-Widget wird gepackt (pack() ist ein einfacher Layout-Manager)

    # Eingabe-Feld-Widget erstellen:
    eingabe = ttk.Entry(root)
    eingabe.pack()


    labereflection = tk.Label(root, text="Passwort:")
    eingabepw = ttk.Entry(root, show="*")
    labereflection.pack()
    eingabepw.pack()

    # name =
    button = ttk.Button(
        root,
        # Texto dentro de boton
        text="OK",
        # callback()
        command=lambda:
            print(eingabe.get(), eingabepw.get())
    )

    button.pack()

    check_var = tk.BooleanVar()
    checkbutton = ttk.Checkbutton(root, text="porfavor escoja", variable = check_var)
    checkbutton.pack()

    # Hauptschleife (Mainloop):
    root.mainloop()



if __name__ == "__main__":
    main()
