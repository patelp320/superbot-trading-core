import tkinter as tk
from tkinter import messagebox, ttk
from dotenv import load_dotenv, set_key
import os
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

class SuperbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Superbot AI Control Panel")
        self.root.geometry("920x600")
        self.build_ui()

    def build_ui(self):
        # --- Credentials Section ---
        creds = tk.LabelFrame(self.root, text="\ud83d\udd10 Credentials", padx=10, pady=10)
        creds.pack(fill="x", padx=10, pady=5)

        tk.Label(creds, text="Email:").grid(row=0, column=0)
        self.email_entry = tk.Entry(creds, width=30)
        self.email_entry.insert(0, os.getenv("EMAIL_USER", ""))
        self.email_entry.grid(row=0, column=1)

        tk.Label(creds, text="IBKR API Key:").grid(row=0, column=2)
        self.ibkr_entry = tk.Entry(creds, width=30)
        self.ibkr_entry.insert(0, os.getenv("IBKR_KEY", ""))
        self.ibkr_entry.grid(row=0, column=3)

        tk.Button(creds, text="\ud83d\udcbe Save", command=self.save_credentials).grid(row=0, column=4, padx=10)

        # --- Trade Ideas Section ---
        trades = tk.LabelFrame(self.root, text="\ud83d\udccb Trade Ideas", padx=10, pady=10)
        trades.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Symbol", "Type", "Strategy", "Confidence", "Reason")
        self.tree = ttk.Treeview(trades, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140 if col != "Reason" else 260)
        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(trades)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="\ud83d\udd04 Refresh Ideas", command=self.load_mock_trades).pack(side="left", padx=5)
        tk.Button(btn_frame, text="\ud83d\udcc8 Show Equity Curve", command=self.plot_equity).pack(side="left", padx=5)

        self.load_mock_trades()

    def save_credentials(self):
        set_key(ENV_PATH, "EMAIL_USER", self.email_entry.get())
        set_key(ENV_PATH, "IBKR_KEY", self.ibkr_entry.get())
        messagebox.showinfo("Saved", "\u2705 Credentials saved to .env")

    def load_mock_trades(self):
        self.tree.delete(*self.tree.get_children())
        mock_trades = [
            ("TSLA", "Options", "CSP", "92%", "High IV + Strong base support"),
            ("GFAI", "Penny", "Gap & Go", "88%", "Low float + news catalyst"),
            ("NVDA", "Options", "Iron Condor", "79%", "Range-bound w/ low vega"),
            ("COSM", "Penny", "VWAP Reclaim", "85%", "Volume surge + trend flip")
        ]
        for trade in mock_trades:
            self.tree.insert("", "end", values=trade)

    def plot_equity(self):
        fig, ax = plt.subplots(figsize=(6, 3))
        equity = [10000 + sum(random.choices([-150, 100, 250, -200, 50], k=i)) for i in range(1, 21)]
        ax.plot(equity, marker="o")
        ax.set_title("Equity Curve (Simulated)")
        ax.set_ylabel("PnL ($)")
        ax.grid(True)

        top = tk.Toplevel(self.root)
        top.title("\ud83d\udcc8 Equity Curve")
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SuperbotGUI(root)
    root.mainloop()
