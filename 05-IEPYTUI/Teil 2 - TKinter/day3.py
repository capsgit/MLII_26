import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog


def zeige_messagebox():
    messagebox.showinfo("Info", "Hallo Welt!")


def oeffne_filedialog():
    dateiname = filedialog.askopenfilename(initialdir="/", title="Bitte wählen Sie eine Datei aus",
                                           filetypes=(("Textdateien", "*.txt"), ("Alle Dateien", "*.*")))

    if dateiname:
        label_dateiname.config(text=dateiname)

    else:
        label_dateiname.config(text="Nichts ausgewählt")


def speichern_filedialog():
    dateiname = filedialog.asksaveasfilename(initialdir="/",
                                             title="Bitte wählen Sie einen Dateinamen aus",
                                             filetypes=(("Textdateien", "*.txt"),
                                                        ("Markdown Dateien", "*.md"),
                                                        ("Alle Dateien", "*.*")),
                                             confirmoverwrite=True  # Frage, ob Datei überschrieben werden soll
                                             )

    if dateiname:
        label_dateiname.config(text=dateiname)
    else:
        label_dateiname.config(text="Nichts ausgewählt")


def frage_nach_eingabe():
    # antwort = None
    antwort = simpledialog.askstring("Eingabe", "Bitte geben Sie etwas ein:")
    if antwort:
        messagebox.showinfo("Ihre Antwort", antwort)


def frage_ja_nein():
    antwort = messagebox.askyesno("Ja/Nein", "Sind Sie sicher?")

    if antwort:
        messagebox.showinfo("Ja", "Danke!")
    else:
        messagebox.showinfo("Nein", "Okay.")


def frage_ja_nein_abbrechen():
    antwort = messagebox.askyesnocancel("Speichern/Überschreiben", "Sind Sie sicher?")
    # Am Beispiel von Dateien:
    if antwort:
        # Vorhandener Dateiname wird verwendet
        messagebox.showinfo("Ja", "Ja wurde ausgewählt, Danke!")

    elif antwort is False:
        # Neuer Dateiname darf ausgewählt werden
        messagebox.showinfo("Nein", "Nein wurde ausgewählt. Okaaaay")

    else:
        # Keine Aktion, zurück
        messagebox.showinfo("Abbruch", "Dialog abgebrochen.")


def zeige_warnung():
    messagebox.showwarning("Warnung", "Bitte beachten Sie, \ndass diese Warnung eine Warnung ist!")


def main():
    global label_dateiname
    root = tk.Tk()
    root.title("Dialoge und Nachrichten")
    root.geometry("300x300")

    btn_messagebox = tk.Button(root, text="Zeige Messagebox", command=zeige_messagebox)
    btn_messagebox.pack()

    btn_filedialog = tk.Button(root, text="Öffne Filedialog", command=oeffne_filedialog)
    btn_filedialog.pack()

    btn_savefiledialog = tk.Button(root, text="Speichern Filedialog", command=speichern_filedialog)
    btn_savefiledialog.pack()

    btn_simpledialog = tk.Button(root, text="Öffne SimpleDialog", command=frage_nach_eingabe)
    btn_simpledialog.pack()

    btn_ja_nein = tk.Button(root, text="Frage Ja/Nein", command=frage_ja_nein)
    btn_ja_nein.pack()

    btn_ja_nein_abbrechen = tk.Button(root, text="Frage Ja/nein/Abbrechen", command=frage_ja_nein_abbrechen)
    btn_ja_nein_abbrechen.pack()

    btn_warning = tk.Button(root, text="Zeige Warnung", command=zeige_warnung)
    btn_warning.pack()

    label_dateiname = tk.Label(root, text="Keine Datei ausgewählt")
    label_dateiname.pack()

    root.mainloop()


if __name__ == "__main__":
    main()

