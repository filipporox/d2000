import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from report_window import ReportWindow
from royalties_dovute_window import RoyaltiesDovuteWindow
from distributori import importa_dati_fuga, importa_dati_artist_first, importa_dati_universal

class RoyaltiesDovuteWindow(tk.Toplevel):
    def __init__(self, parent, df_royalties_dovute):
        super().__init__(parent)

        self.title("Royalties dovute")
        self.resizable(False, False)

        self.artisti_percentuali = artisti_percentuali

        self.data_tree = ttk.Treeview(self, columns=("Artista", "Royalties Dovute"), show="headings")
        self.data_tree.heading("Artista", text="Artista")
        self.data_tree.heading("Royalties Dovute", text="Royalties Dovute")
        self.data_tree.column("Artista", anchor="w")
        self.data_tree.column("Royalties Dovute", anchor="w")

        for _, row in df_royalties_dovute.iterrows():
            self.data_tree.insert("", "end", values=(row["Artista"], f"€{row['Royalties Dovute']:.2f}"))

        self.data_tree.pack(fill=tk.BOTH, expand=True)

class AppRoyalties(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.df_master = pd.DataFrame()
        self.artisti_percentuali = {}

        
        self.title("Calcolo Royalties")
        self.geometry("600x600")

        self.file_label = ttk.Label(self, text="Seleziona file CSV:")
        self.file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.file_entry = ttk.Entry(self, width=40)
        self.file_entry.grid(row=0, column=1, padx=10, pady=10)

        self.file_btn = ttk.Button(self, text="Sfoglia", command=self.scegli_file)
        self.file_btn.grid(row=0, column=2, padx=10, pady=10)

        self.distributore_label = ttk.Label(self, text="Seleziona distributore:")
        self.distributore_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.semestre_label = ttk.Label(self, text="Semestre:")
        self.semestre_label.grid(row=5, column=0, pady=5, sticky="e")

        self.semestre_combo = ttk.Combobox(self, values=("1", "2"), state="readonly")
        self.semestre_combo.grid(row=5, column=1, pady=5, sticky="w")

        self.distributore_combo = ttk.Combobox(self, values=["Fuga", "Artist First", "Universal"])
        self.distributore_combo.grid(row=1, column=1, padx=10, pady=10)

        self.importa_btn = ttk.Button(self, text="Importa", command=self.importa_dati)
        self.importa_btn.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.genera_report_btn = ttk.Button(self, text="Genera Report", command=self.genera_report)
        self.genera_report_btn.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.mostra_royalties_dovute_btn = ttk.Button(self, text="Mostra Royalties Dovute", command=self.mostra_royalties_dovute)
        self.mostra_royalties_dovute_btn.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.salva_chiudi_button = ttk.Button(self, text="Salva e chiudi", command=self.salva_dati_e_chiudi)
        self.salva_chiudi_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.mostra_royalties_button = ttk.Button(self, text="Mostra royalties dovute", command=self.mostra_royalties_dovute)
        self.mostra_royalties_button.grid(row=5, column=2, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.salva_dati_e_chiudi)

    def scegli_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def importa_dati(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        if self.distributore_var.get() == "Fuga Music":
            self.df_master, self.artisti_percentuali = distributori.importa_dati_fuga(file_path, self.df_master, self.artisti_percentuali)
 
         if not file_path or not distributore:
            messagebox.showerror("Errore", "Seleziona un file CSV e un distributore.")
            return

        if distributore == "Fuga":
            importa_dati_fuga(file_path, self.df_master, self.artisti_percentuali)
        elif distributore == "Artist First":
            importa_dati_artist_first(file_path)
        elif distributore == "Universal":
            importa_dati_universal(file_path)

    def genera_report(self, artisti_percentuali):
        semestre = self.semestre_combo.get()
        if semestre == "":
            messagebox.showerror("Errore", "Seleziona un semestre.")
            return

        # Calcola la data di inizio e fine del semestre selezionato
        anno_corrente = datetime.datetime.now().year
        if semestre == "1":
            start_date = datetime.datetime(anno_corrente, 1, 1)
            end_date = datetime.datetime(anno_corrente, 6, 30)
        elif semestre == "2":
            start_date = datetime.datetime(anno_corrente, 7, 1)
            end_date = datetime.datetime(anno_corrente, 12, 31)

        # Filtra il dataframe master per il semestre selezionato
        df_semestre = df_master[(df_master["Sale Start date"] >= start_date) & (df_master["Sale End date"] <= end_date)]

        # Calcola le royalties per artista e prodotto
        royalties = []
        for artista, percentuale in artisti_percentuali.items():
            df_artista = df_semestre[df_semestre["Product Artist"] == artista]
            for _, row in df_artista.iterrows():
                importo_artista = row["Reported Royalty"] * percentuale / 100
                royalties.append({
                    "Artista": artista,
                    "Prodotto": row["Product Title"],
                    "Reported Royalty": row["Reported Royalty"],
                    "Percentuale Royalties": percentuale,
                    "Importo Artista": importo_artista
                })

        df_royalties = pd.DataFrame(royalties)

        # Mostra il report in una nuova finestra
        report_window = ReportWindow(self, df_royalties)
        report_window.transient(self)
        report_window.grab_set()
        self.wait_window(report_window)


    def salva_dati_e_chiudi(self):
        # Salva il dataframe master in un file CSV
        df_master.to_csv("master_data.csv", index=False)

        # Salva le percentuali degli artisti in un file JSON
        with open("artisti_percentuali.json", "w") as f:
            json.dump(artisti_percentuali, f, ensure_ascii=False)

        # Chiudi l'applicazione
        self.destroy()

    def mostra_royalties_dovute(self):
        # Calcola le royalties dovute ad ogni artista
        royalties = []
        for artista, percentuale in artisti_percentuali.items():
            df_artista = df_master[df_master["Product Artist"] == artista]
            royalties_dovute = df_artista["Reported Royalty"].sum() * percentuale / 100
            royalties.append({"Artista": artista, "Royalties Dovute": royalties_dovute})

        df_royalties_dovute = pd.DataFrame(royalties)

        # Mostra le royalties dovute in una nuova finestra
        royalties_dovute_window = RoyaltiesDovuteWindow(self, df_royalties_dovute)
        royalties_dovute_window.transient(self)
        royalties_dovute_window.grab_set()
        self.wait_window(royalties_dovute_window)

if __name__ == "__main__":
    app = AppRoyalties()
    app.mainloop()
