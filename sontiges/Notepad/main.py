import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import settings

class DatabaseManager:
    def __init__(self):
        pass


class SettingsDialog:
    pass


class NotepadApp:
    def __init__(self, root):
        root.title("Notepad -")
        root.geometry("400x400")
        root.protocol("WM_DELETE_WINDOW", self.beenden)
        self.root = root

        # variables
        self.wordwrap = None
        self.filename = None
        self.textchanged = None

        # iniciar metodo
        self.menue_erstellen()
        self.einstellungen_laden()
        self.textfeld_erstellen()
        self.kontextmenue = self.kontext_menue_erstellen()
        self.einstellungen_anwenden()


    def menue_erstellen(self):
        # menu principal
        self.hauptmenue = tk.Menu(self.root)
        self.root.config(menu = self.hauptmenue)

        # menu Datos
        self.dateimenue = tk.Menu( self.hauptmenue, tearoff=0)
        self.hauptmenue.add_cascade(label="Datei", menu=self.dateimenue)
        self.dateimenue.add_command(label="Neu", command=self.datei_neu)
        self.dateimenue.add_command(label="Öffnen", command=self.datei_oeffen)
        self.dateimenue.add_command(label="Speichern", command=self.datei_speichern)
        self.dateimenue.add_command(label="Speichern unter", command=self.datei_speichern_unter)
        self.dateimenue.add_separator()
        self.dateimenue.add_command(label="Beenden", command=self.beenden)

        # menu editar
        self.bearbeitenmenue = tk.Menu(self.hauptmenue, tearoff=0)
        self.hauptmenue.add_cascade(label="Bearbeiten", menu=self.bearbeitenmenue)
        self.bearbeitenmenue.add_command(label="Kopieren", command=self.kopieren)
        self.bearbeitenmenue.add_command(label="Einfügen", command=self.einfuegen)
        self.bearbeitenmenue.add_separator()
        self.bearbeitenmenue.add_command(label="Einstellugen", command=self.einstellugen_zeigen)

        # menu ayuda
        self.hilfmenue = tk.Menu(self.hauptmenue, tearoff=0)
        self.hauptmenue.add_cascade(label="Hilfe", menu=self.hilfmenue)
        self.hilfmenue.add_command(label="Über Notepad", command=self.ueber)

    def kontext_menue_erstellen(self):
        kontextmenue = tk.Menu(self.root, tearoff=0)
        kontextmenue.add_command(label="Kopieren", accelerator="Alt+c", command=self.kopieren)
        kontextmenue.add_command(label="Einfügen", accelerator="Alt+v", command=self.einfuegen)

        self.root.bind("<Button-3>", lambda e: kontextmenue.tk_popup(e.x_root, e.y_root))
        return kontextmenue

    def ueber(self):
        pass

    def kopieren(self, event=None):
        """ global selected_text
        hilfe_text = """""
        try:
            selected_text = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return "break"

        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)

        return "break"

    def einfuegen(self, event=None):
        try:
            clip = self.root.clipboard_get()
        except tk.TclError:
            return "break"  # clipboard vacío o no-texto

        # Si hay selección, la reemplaza
        try:
            self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass

        self.text.insert(tk.INSERT, clip)
        return "break"

    def datei_speichern_unter(self):
        self.filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=(("Textdateien", "*.txt"),
                                                                ("Alle Dateien", "*.*")))
        if not self.filename:
            return

        self.datei_schreiben()

    def datei_speichern(self):
        if not self.filename:
            self.datei_speichern_unter()
        else:
            self.datei_schreiben()

    def datei_schreiben(self):
        try:
            with open(self.filename, "w") as file:
                text = self.text.get("1.0", tk.END)
                file.write(text)
            self.root.title(f"Notepad - {self.filename}")
            self.textchanged = False        # para interne variable
            self.text.edit_modified(False)  # para tkinter -> signal "text geädert" wird zurück gezetzt
            print("Datei gespeichert")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {e}")

    def datei_neu(self):
        if self.textchanged:
            if not messagebox.askyesno("Atencion!", "quiere guardar cambios antes de crear un nuevo archivo?"):
                return

        self.text.delete("1.0", tk.END)
        self.root.title("Notepad -")

    def datei_oeffen(self, file=None):
        if not file:
            self.filename = filedialog.askopenfilename(defaultextension="*.txt",  filetypes=(("Textdateien", "*.txt"), ("Alle Dateien", "*.*")))
            if not self.filename:
                return
        else:
            self.filename = file

        try:
            with open(self.filename, "r") as file:
                text = file.read()
                self.text.edit_modified(False)  # disable "modified" bevor man den content anfasst
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, text)
                self.root.title(f"Notepad - {self.filename}")
                self.textchanged = False
                self.text.edit_modified(False) # clean erneut am ende
                self.textchanged = False       # clean erneut am ende

        except Exception as e:
            messagebox.showerror("Fehler!", f"Fehler: {e}")

    def beenden(self):
        if messagebox.askokcancel("Beenden?", "Soll das Programm wirklich beendet werden?"):
            if self.textchanged:
                if messagebox.askyesno("save?", "quiere guardar cambios antes de salir?"):
                    self.datei_speichern()

            self.root.quit()
            self.root.destroy()

    def einstellungen_laden(self):
        """Lädt die Einstellungen aus der Datenbank."""
        einstellungen_dict = settings.einstellungen_laden()

        self.TEXT_FONT = einstellungen_dict['schriftart']
        self.TEXT_SIZE = einstellungen_dict['schriftgroesse']
        self.TEXT_COLOR = einstellungen_dict['textfarbe']
        self.BACKGROUND_COLOR = einstellungen_dict['hintergrundfarbe']
        self.seitenumbruch = einstellungen_dict['seitenumbruch']

        # Umbruch einstellen:
        if self.seitenumbruch:
            self.wordwrap = "word"
        else:
            self.wordwrap = "none"

    def einstellungen_anwenden(self):
        if not hasattr(self, "text"):
            return

        self.text.config(
            font=(self.TEXT_FONT, self.TEXT_SIZE),
            fg=self.TEXT_COLOR,
            bg=self.BACKGROUND_COLOR,
            wrap="word" if self.seitenumbruch else "none"
        )

        # Mostrar/ocultar scrollbarh solo si existe (cuando wrap=none la tendrás)
        if hasattr(self, "scrollbarh"):
            if self.seitenumbruch:
                self.scrollbarh.pack_forget()
            else:
                self.scrollbarh.pack(side="bottom", fill="x")

    def einstellugen_zeigen(self):
        def on_settings_saved():
            prev_seitenumbruch = self.seitenumbruch
            prev_wordwrap = self.wordwrap

            self.einstellungen_laden()

            # Si cambió el modo wrap, reconstruir widgets (crea/quita scrollbarh)
            if self.seitenumbruch != prev_seitenumbruch or self.wordwrap != prev_wordwrap:
                self.textfeld_neu_aufbauen()
            else:
                self.einstellungen_anwenden()

        einstellungs_fenster = settings.Settings(self.root, callback=on_settings_saved)
        print("SETTING", einstellungs_fenster.aktuelle_einstellungen)

    def on_text_change(self, event):
        if self.text.edit_modified(): # nur wenn es wircklich als "modified" markiert ist
            self.textchanged = True
            self.text.edit_modified(False) # reset flag

    def textfeld_erstellen(self):
        if self.wordwrap == "none":
            # Testfeld mit Scrollbars erstellen:
            self.text_frame = tk.Frame(self.root)
            self.text_frame.pack(pady=5, padx=5, expand=True, fill="both")

            self.scrollbarv = tk.Scrollbar(self.text_frame, orient="vertical")
            self.scrollbarh = tk.Scrollbar(self.text_frame, orient="horizontal")

            self.scrollbarv.pack(side="right", fill="y")
            self.scrollbarh.pack(side="bottom", fill="x")

            self.text = tk.Text(self.text_frame,
                                wrap= self.wordwrap, # möglich: "none", "word", "char""
                                yscrollcommand=self.scrollbarv.set,
                                xscrollcommand=self.scrollbarh.set)

            self.text.pack(expand=True, fill="both")
            self.text.bind("<<Modified>>", self.on_text_change)

            self.scrollbarh.config(command=self.text.xview)
            self.scrollbarv.config(command=self.text.yview)

        else:
            # Textfeld ohne Scrollbars erstellen:
            self.text_frame = tk.Frame(self.root)
            self.text_frame.pack(pady=5, padx=5, expand=True, fill="both")

            self.scrollbarv = tk.Scrollbar(self.text_frame, orient="vertical")

            self.scrollbarv.pack(side="right", fill="y")

            self.text = tk.Text(self.text_frame,
                                wrap=self.wordwrap,  # möglich: "none", "word", "char""
                                yscrollcommand=self.scrollbarv.set)

            self.text.pack(expand=True, fill="both")
            self.text.bind("<<Modified>>", self.on_text_change)

            self.scrollbarv.config(command=self.text.yview)

    def textfeld_neu_aufbauen(self):
        # guardar contenido
        content = self.text.get("1.0", "end-1c")

        # guardar scroll vertical (si hay)
        y_first = self.text.yview()[0] if hasattr(self, "text") else 0.0

        # destruir el frame completo (se lleva scrollbars y text)
        if hasattr(self, "text_frame"):
            self.text_frame.destroy()

        # crear otra vez según self.wordwrap (que viene de settings)
        self.textfeld_erstellen()

        # restaurar contenido y scroll
        self.text.insert("1.0", content)
        self.text.yview_moveto(y_first)

        # aplicar font/color/bg (por si acaso)
        self.einstellungen_anwenden()


if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.bind_all("<Alt-c>", app.kopieren)
    root.bind_all("<Alt-C>", app.kopieren)
    root.bind_all("<Alt-v>", app.einfuegen)
    root.bind_all("<Alt-V>", app.einfuegen)

    # si ese argv mayor a 1 entonces abrir
    if len(sys.argv) > 1:
        app.datei_oeffen(sys.argv[1])
    root.mainloop()
    #main()