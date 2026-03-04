import tkinter as tk
from tkinter import ttk

def main():

    # --------------------------ROOT / VENTANA-----------------------------
    # creacion de la ventana principal, con titulo y dimensiones
    root = tk.Tk()
    root.title("Einfaches TKInter-Fenster")
    root.geometry("700x300+50+50")

    # ---------------------------------------------WIDGETS-----------------------------------
    cuz_font = ("Roboto", 32, "bold")


    # Label--------------------------------------------------------------------
    # Widget erstellen:
    #label = tk.Label(root, text="hey hey hey!!!!", bg="orange", fg="white", bd="25", font=cuz_font)
    label = ttk.Label(root, text="hey hey hey!!!!", font=cuz_font, background="orange", foreground="white")
    # Das Label-Widget wird gepackt (pack() ist ein einfacher Layout-Manager)
    label.pack()

    # Entry---------------------------------------------------------------------
    #entrada = tk.Entry(root, bd="10", relief="solid" , cursor="xterm", bg="white", border="3", justify="center", width=100)
    entrada = ttk.Entry(root,justify="center", width=100)
    entrada.pack(pady=5)

    def on_button_click():
        input_text = entrada.get()
        print(input_text)

    # Button---------------------------------------------------------------------
    #submit = tk.Button(root, text="Submit", bg="green", fg="white", bd="3", activebackground="grey", activeforeground="black", disabledforeground="red", width="300", relief="groove", command=on_button_click)
    submit = ttk.Button(root, text="Submit", command=on_button_click)
    submit.pack(pady=15)
    #-----------------------MAINLOOP--------------------------------------
    root.mainloop()



if __name__ == "__main__":
    main()
