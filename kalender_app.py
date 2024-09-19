
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('calendar_app.db')
c = conn.cursor()

# Tabelle für die Termine erstellen, falls noch nicht vorhanden
c.execute('''CREATE TABLE IF NOT EXISTS termine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datum TEXT,
    beginn TEXT,
    ende TEXT,
    kunde TEXT,
    ort TEXT,
    terminart TEXT,
    kommentar TEXT,
    bestatigt INTEGER,
    abrechnung TEXT
)''')
conn.commit()

class KalenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalender App")
        self.create_widgets()

    def create_widgets(self):
        # Datum
        tk.Label(self.root, text="Datum auswählen:").grid(row=0, column=0)
        self.datum_entry = tk.Entry(self.root)
        self.datum_entry.grid(row=0, column=1)

        # Beginn Uhrzeit
        tk.Label(self.root, text="Beginn Uhrzeit:").grid(row=1, column=0)
        self.beginn_entry = tk.Entry(self.root)
        self.beginn_entry.grid(row=1, column=1)

        # Ende Uhrzeit
        tk.Label(self.root, text="Ende Uhrzeit:").grid(row=2, column=0)
        self.ende_entry = tk.Entry(self.root)
        self.ende_entry.grid(row=2, column=1)

        # Kunde auswählen
        tk.Label(self.root, text="Kunde:").grid(row=3, column=0)
        self.kunde_var = tk.StringVar(value="WISAG")
        kunde_options = ["WISAG", "Schmid", "KVHessen", "LAUER GmbH", "Umdasch", "Ampega", "Anderer Kunde"]
        self.kunde_menu = ttk.Combobox(self.root, textvariable=self.kunde_var, values=kunde_options)
        self.kunde_menu.grid(row=3, column=1)

        # Ort
        tk.Label(self.root, text="Ort des Termins:").grid(row=4, column=0)
        self.ort_entry = tk.Entry(self.root)
        self.ort_entry.grid(row=4, column=1)

        # Art des Termins
        tk.Label(self.root, text="Art des Termins:").grid(row=5, column=0)
        self.terminart_var = tk.StringVar(value="Besprechung")
        terminart_options = ["Besprechung", "Auftrag"]
        self.terminart_menu = ttk.Combobox(self.root, textvariable=self.terminart_var, values=terminart_options)
        self.terminart_menu.grid(row=5, column=1)

        # Kommentar
        tk.Label(self.root, text="Kommentar:").grid(row=6, column=0)
        self.kommentar_entry = tk.Entry(self.root)
        self.kommentar_entry.grid(row=6, column=1)

        # Bestätigen Button
        self.bestatigt_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Termin bestätigen", variable=self.bestatigt_var).grid(row=7, column=0)

        # Abrechnungsauswahl
        tk.Label(self.root, text="Abrechnung:").grid(row=8, column=0)
        self.abrechnung_var = tk.StringVar(value="Rechnung")
        abrechnung_options = ["Rechnung", "Regiezettel"]
        self.abrechnung_menu = ttk.Combobox(self.root, textvariable=self.abrechnung_var, values=abrechnung_options)
        self.abrechnung_menu.grid(row=8, column=1)

        # Buttons
        tk.Button(self.root, text="Termin speichern", command=self.termin_speichern).grid(row=9, column=0)
        tk.Button(self.root, text="Termine anzeigen", command=self.termine_anzeigen).grid(row=9, column=1)

    # Termin speichern Funktion
    def termin_speichern(self):
        datum = self.datum_entry.get()
        beginn = self.beginn_entry.get()
        ende = self.ende_entry.get()
        kunde = self.kunde_var.get()
        ort = self.ort_entry.get()
        terminart = self.terminart_var.get()
        kommentar = self.kommentar_entry.get()
        bestatigt = 1 if self.bestatigt_var.get() else 0
        abrechnung = self.abrechnung_var.get()

        if datum and beginn and ende and kunde and ort:
            c.execute('''INSERT INTO termine (datum, beginn, ende, kunde, ort, terminart, kommentar, bestatigt, abrechnung) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (datum, beginn, ende, kunde, ort, terminart, kommentar, bestatigt, abrechnung))
            conn.commit()
            messagebox.showinfo("Erfolg", "Termin erfolgreich gespeichert!")
        else:
            messagebox.showwarning("Fehler", "Bitte alle Felder ausfüllen!")

    # Termine anzeigen Funktion
    def termine_anzeigen(self):
        self.anzeige_window = tk.Toplevel(self.root)
        self.anzeige_window.title("Gespeicherte Termine")

        rows = c.execute("SELECT * FROM termine").fetchall()

        for index, row in enumerate(rows):
            tk.Label(self.anzeige_window, text=f"Termin {index+1}: {row[1]} {row[2]} - {row[3]}").grid(row=index, column=0)

# Hauptanwendung starten
root = tk.Tk()
app = KalenderApp(root)
root.mainloop()
