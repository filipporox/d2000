import tkinter as tk
from tkinter import ttk

class RoyaltiesDovuteWindow(tk.Toplevel):
    def __init__(self, royalties_dovute):
        super().__init__()

        self.title("Royalties Dovute")
        self.geometry("400x300")

        self.royalties_table = ttk.Treeview(self)
        self.royalties_table["columns"] = ("Royalties Dovute",)
        self.royalties_table.heading("#0", text="Artista")
        self.royalties_table.heading("Royalties Dovute", text="Royalties Dovute")
        self.royalties_table.pack(fill=tk.BOTH, expand=True)

        for artista, importo_dovuto in royalties_dovute.items():
            self.royalties_table.insert("", tk.END, text=artista, values=(f"€ {importo_dovuto:.2f}",))
