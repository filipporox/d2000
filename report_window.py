import tkinter as tk
from tkinter import ttk

class ReportWindow(tk.Toplevel):
    def __init__(self, app, df_royalties):
        super().__init__()

        self.title("Report Royalties")
        self.geometry("800x600")

        self.report_table = ttk.Treeview(self)
        self.report_table["columns"] = ("Prodotto", "Reported Royalty", "Percentuale Royalties", "Importo Artista")
        self.report_table.heading("#0", text="Artista")
        self.report_table.heading("Prodotto", text="Prodotto")
        self.report_table.heading("Reported Royalty", text="Reported Royalty")
        self.report_table.heading("Percentuale Royalties", text="Percentuale Royalties")
        self.report_table.heading("Importo Artista", text="Importo Artista")
        self.report_table.pack(fill=tk.BOTH, expand=True)

        for _, row in df_royalties.iterrows():
            self.report_table.insert("", tk.END, text=row["Artista"], values=(
                row["Prodotto"],
                f"€ {row['Reported Royalty']:.2f}",
                row["Percentuale Royalties"],
                f"€ {row['Importo Artista']:.2f}"
            ))

        self.genera_pdf_btn = ttk.Button(self, text="Genera PDF e aggiorna pagamenti", command=lambda: app.genera_pdf_e_aggiorna_pagamenti(row["Artista"], df_royalties))
        self.genera_pdf_btn.pack(side=tk.BOTTOM)
