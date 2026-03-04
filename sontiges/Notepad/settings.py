import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, font, ttk
import sqlite3
from pathlib import Path



class Settings:
    def __init__(self, root, callback=None):

        self.settings = tk.Toplevel(root)
        self.settings.title("Einstellungen")
        self.settings.geometry("640x600")
        self.settings.grab_set()
        # self.settings.protocol("WM_DELETE_WINDOW", self.ende)  # beenden durch X abfangen

        # Einstellungen laden:
        self.aktuelle_einstellungen = einstellungen_laden()

        self.callback = callback
        self.seitenumbruch = tk.BooleanVar(value=self.aktuelle_einstellungen['seitenumbruch'])
        self.schriftart_var = tk.StringVar(value=self.aktuelle_einstellungen['schriftart'])
        self.schriftgroesse_var = tk.IntVar(value=self.aktuelle_einstellungen['schriftgroesse'])
        self.textfarbe = self.aktuelle_einstellungen['textfarbe']
        self.hintergrundfarbe = self.aktuelle_einstellungen['hintergrundfarbe']

        datenbank_erstellen()
        self.erstelle_gui()

    def erstelle_gui(self):
        """Erstellt die Benutzeroberfläche für die Einstellungen."""

        # Hauptframe
        main_frame = tk.Frame(self.settings)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titel
        titel_label = tk.Label(main_frame, text="Einstellungen", font=("Arial", 16, "bold"))
        titel_label.pack(pady=(0, 20))

        # Schriftart-Auswahl
        schrift_frame = tk.LabelFrame(main_frame, text="Schriftart", padx=10, pady=10)
        schrift_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(schrift_frame, text="Schriftfamilie:").grid(row=0, column=0, sticky=tk.W, pady=5)
        schriftarten = list(font.families())
        schriftarten.sort()
        schrift_combo = ttk.Combobox(schrift_frame, textvariable=self.schriftart_var, values=schriftarten, state="readonly")
        schrift_combo.grid(row=0, column=1, sticky=tk.W+tk.E, padx=(10, 0), pady=5)

        tk.Label(schrift_frame, text="Schriftgröße:").grid(row=1, column=0, sticky=tk.W, pady=5)
        groesse_spinbox = tk.Spinbox(schrift_frame, from_=8, to=72, textvariable=self.schriftgroesse_var, width=10)
        groesse_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        schrift_frame.columnconfigure(1, weight=1)

        # Farben-Auswahl
        farben_frame = tk.LabelFrame(main_frame, text="Farben", padx=10, pady=10)
        farben_frame.pack(fill=tk.X, pady=(0, 10))

        # Textfarbe
        tk.Label(farben_frame, text="Textfarbe:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.textfarbe_button = tk.Button(farben_frame, text="Farbe wählen", command=self.textfarbe_waehlen,
                                          bg=self.textfarbe, width=15)
        self.textfarbe_button.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # Hintergrundfarbe
        tk.Label(farben_frame, text="Hintergrundfarbe:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.hintergrund_button = tk.Button(farben_frame, text="Farbe wählen", command=self.hintergrundfarbe_waehlen,
                                            bg=self.hintergrundfarbe, width=15)
        self.hintergrund_button.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # Weitere Einstellungen
        weitere_frame = tk.LabelFrame(main_frame, text="Weitere Optionen", padx=10, pady=10)
        weitere_frame.pack(fill=tk.X, pady=(0, 20))

        # Seitenumbruch Checkbox
        checkbutton = tk.Checkbutton(weitere_frame, text="Seitenumbruch aktivieren", variable=self.seitenumbruch)
        checkbutton.pack(anchor=tk.W)

        # Vorschau
        vorschau_frame = tk.LabelFrame(main_frame, text="Vorschau", padx=10, pady=10)
        vorschau_frame.pack(fill=tk.X, pady=(0, 20))

        self.vorschau_text = tk.Text(vorschau_frame, height=3, width=40)
        self.vorschau_text.pack()
        self.vorschau_text.insert(tk.END, "Dies ist eine Vorschau der gewählten Einstellungen.")
        self.vorschau_aktualisieren()

        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X)

        tk.Button(button_frame, text="Abbrechen", command=self.settings.destroy).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(button_frame, text="Speichern", command=self.einstellungen_speichern).pack(side=tk.RIGHT)
        tk.Button(button_frame, text="Vorschau aktualisieren", command=self.vorschau_aktualisieren).pack(side=tk.LEFT)

    def textfarbe_waehlen(self):
        """Öffnet das Farbwähler Widget für die Textfarbe"""
        farbe = colorchooser.askcolor(color=self.textfarbe, title="Textfarbe wählen")
        if farbe[1]:
            self.textfarbe = farbe[1]
            self.textfarbe_button.config(bg=self.textfarbe)
            self.vorschau_aktualisieren()

    def hintergrundfarbe_waehlen(self):
        """Öffnet das Farbwähler Widget für die Hintergrundfarbe"""
        farbe = colorchooser.askcolor(color=self.textfarbe, title="Hintergrundfarbe wählen")
        if farbe[1]:
            self.hintergrundfarbe = farbe[1]
            self.hintergrund_button.config(bg=self.hintergrundfarbe)
            self.vorschau_aktualisieren()

    def vorschau_aktualisieren(self):
        """Aktualisiert die Vorschau mit den aktuellen Einstellungen"""
        schriftart = self.schriftart_var.get()
        schriftgroesse = self.schriftgroesse_var.get()

        self.vorschau_text.config(font=(schriftart, schriftgroesse))
        self.vorschau_text.config(fg=self.textfarbe)
        self.vorschau_text.config(bg=self.hintergrundfarbe)

    def einstellungen_speichern(self):
        """Speichert die Einstellungen in die Datenbank."""
        conn = sqlite3.connect('nopepad.db')
        cursor = conn.cursor()

        cursor.execute('''
                       UPDATE einstellungen
                       SET schriftart=?,
                           schriftgroesse=?,
                           textfarbe=?,
                           hintergrundfarbe=?,
                           seitenumbruch=?
                       WHERE id = 1
                       ''', (
                           self.schriftart_var.get(),
                           self.schriftgroesse_var.get(),
                           self.textfarbe,
                           self.hintergrundfarbe,
                           self.seitenumbruch.get()
                       ))

        conn.commit()
        conn.close()

        # Callback-Funktion aufrufen, falls vorhanden
        if self.callback:
            self.callback()

        # Bestätigungsmeldung
        messagebox.showinfo("Gespeichert", "Die Einstellungen wurden erfolgreich gespeichert!")
        self.settings.destroy()


def datenbank_erstellen():
    """Erstellt die Datenbank und Tabelle für Einstellungen falls sie nicht existiert."""
    conn = sqlite3.connect('nopepad.db')
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS einstellungen (
                                                                id INTEGER PRIMARY KEY,
                                                                schriftart TEXT DEFAULT 'Arial',
                                                                schriftgroesse INTEGER DEFAULT 12,
                                                                textfarbe TEXT DEFAULT 'black',
                                                                hintergrundfarbe TEXT DEFAULT 'white',
                                                                seitenumbruch BOOLEAN DEFAULT 0
                   )
                   ''')

    # Standardeinstellungen einfügen, falls keine vorhanden
    cursor.execute('SELECT COUNT(*) FROM einstellungen')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
                       INSERT INTO einstellungen (schriftart, schriftgroesse, textfarbe, hintergrundfarbe, seitenumbruch)
                       VALUES ('Arial', 12, 'black', 'white', 0)
                       ''')

    conn.commit()
    conn.close()


def einstellungen_laden():
    conn = sqlite3.connect('nopepad.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT schriftart, schriftgroesse, textfarbe, hintergrundfarbe, seitenumbruch FROM einstellungen WHERE id = 1""")
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "schriftart": result[0],
            "schriftgroesse": result[1],
            "textfarbe": result[2],
            "hintergrundfarbe": result[3],
            "seitenumbruch": bool(result[4])
        }

    else:
        return {
            "schriftart": "Arial",
            "schriftgroesse": 12,
            "textfarbe": "black",
            "hintergrundfarbe": "white",
            "seitenumbruch": False
        }