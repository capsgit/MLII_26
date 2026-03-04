import tkinter as tk


def log_event(event):
    """Allgemeine Event-Logger-Funktion"""
    print(
        f"Event: {event.type} | Widget: {event.widget} | Keysym: {event.keysym if hasattr(event, 'keysym') else ''} | Num: {getattr(event, 'num', '')} | State: {event.state} | x={event.x}, y={event.y}")


root = tk.Tk()
root.title("Tkinter Event Tester")
root.geometry("400x300")

label = tk.Label(root, text="Drücke Tasten oder benutze die Maus\n(alles wird im Terminal ausgegeben)",
                 font=("Arial", 12), justify="center")
label.pack(expand=True, fill="both")

# Alle relevanten Eventtypen binden
events = [
    "<Key>", "<KeyRelease>",
    "<Button-1>", "<Button-2>", "<Button-3>",
    "<Double-Button-1>", "<Triple-Button-1>",
    "<ButtonRelease-1>", "<B1-Motion>", "<B2-Motion>", "<B3-Motion>",
    "<Motion>", "<Enter>", "<Leave>", "<MouseWheel>",
    "<FocusIn>", "<FocusOut>",
    "<Configure>", "<Destroy>",
]

for ev in events:
    root.bind_all(ev, log_event)

root.mainloop()
