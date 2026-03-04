import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog


def datei_neu():
    pass


def datei_oeffnen():
    pass


def datei_speichern():
    pass


def pdf_exportieren():
    pass


def kontextmenu_zeigen(event):
    kontextmenu.tk_popup(event.x_root, event.y_root)

def programm_beenden():
    global root

    if messagebox.askyesno("Beenden", "Wollen Sie das Programm wirklich beenden?"):
        root.quit()
        root.destroy()

def main():
    global kontextmenu
    global root
    root = tk.Tk()
    root.title("Dialoge und Nachrichten")
    root.geometry("300x300")

    # Hauptmenü
    hauptmenue = tk.Menu(root)  # Menü erstellen
    root.config(menu=hauptmenue)  # Menü dem Hauptfenster hinzufügen

    # Dateimenü erstellen:
    dateimenue = tk.Menu(hauptmenue, tearoff=0)
    hauptmenue.add_cascade(label="Datei", underline=0,
                           menu=dateimenue)  # D wird unterstrichen (wenn nicht, Alt-Taste drücken)
    dateimenue.add_command(label="Neu", command=datei_neu,
                           accelerator="Ctrl+N")  # Im Menü wird Strg+N als Tastenkombi angegeben.
    dateimenue.add_command(label="Öffnen", command=datei_oeffnen)
    dateimenue.add_command(label="Speichern", command=datei_speichern)



    # "Exportieren"-Menü erstellen:
    export_submenue = tk.Menu(dateimenue, tearoff=0)
    dateimenue.add_cascade(label="Exportieren", menu=export_submenue)
    export_submenue.add_command(label="Als PDF exportieren", command=pdf_exportieren)
    export_submenue.add_command(label="Als TXT exportieren", command=lambda: messagebox.showinfo("Info",
                                                                                                 "Wird in txt export"))

    dateimenue.add_separator()  # Trennstrich wird erstellt
    dateimenue.add_command(label="Beenden 2", command=root.quit)
    dateimenue.add_command(label="Beenden, Bender", command=programm_beenden)


    # Hilfe-Menü erstellen
    hilfe_menue = tk.Menu(hauptmenue, tearoff=0)
    hauptmenue.add_cascade(label="Hilfe", menu=hilfe_menue)
    hilfe_menue.add_command(label="Über",
                            command=lambda: messagebox.showinfo("Info", "Coded by the very \nbest Python Course"))

    # Kontextmenüe erstellen:
    kontextmenu = tk.Menu(root, tearoff=0)
    kontextmenu.add_command(label="Kopieren")  # mit command= müsste dann die entsprechende Funktion aufgerufen werden
    kontextmenu.add_command(label="Einfügen")

    # root.bind("<Button-3>", lambda e: kontextmenu.tk_popup(e.x_root, e.y_root))  # das Popup erscheint bei dem Mauszeiger
    root.bind("<Button-3>", kontextmenu_zeigen)

    info_label = tk.Label(root, text="Rechtsklick für Kontextmenü", justify="center")
    info_label.pack(expand=True,
                    fill="both")  # Sorgt dafür, dass das Label auf die Fenstergröße gezogen wird, damit es in der Mitte bleibt


    root.mainloop()


if __name__ == "__main__":
    main()
