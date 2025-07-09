import tkinter as tk
from tkinter import ttk, messagebox

class TradingGUI:
    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("Superbot Trade Dashboard")
        self.trade_data = []
        self.build_ui()
        self.load_mock_trades()

    def build_ui(self):
        columns = ("Symbol", "Type", "Strategy", "Confidence", "Reason")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.build_trade_controls()

    def load_mock_trades(self):
        self.tree.delete(*self.tree.get_children())
        self.trade_data = [
            {
                "symbol": "TSLA",
                "type": "Options",
                "strategy": "CSP",
                "confidence": 0.92,
                "reason": "High IV + Strong base support"
            },
            {
                "symbol": "GFAI",
                "type": "Penny",
                "strategy": "Gap & Go",
                "confidence": 0.88,
                "reason": "Low float + news catalyst"
            },
            {
                "symbol": "NVDA",
                "type": "Options",
                "strategy": "Iron Condor",
                "confidence": 0.79,
                "reason": "Range-bound with low vega"
            },
            {
                "symbol": "COSM",
                "type": "Penny",
                "strategy": "VWAP Reclaim",
                "confidence": 0.85,
                "reason": "Volume surge + trend flip"
            },
        ]

        for trade in self.trade_data:
            self.tree.insert("", "end", values=(
                trade["symbol"],
                trade["type"],
                trade["strategy"],
                f"{int(trade['confidence'] * 100)}%",
                trade["reason"]
            ))

    def build_trade_controls(self):
        control_frame = tk.LabelFrame(self.root, text="⚙️ Controls & Actions", padx=10, pady=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        self.mode = tk.StringVar(value="Paper")
        tk.Label(control_frame, text="Mode:").pack(side="left")
        tk.OptionMenu(control_frame, self.mode, "Paper", "Live").pack(side="left", padx=5)

        tk.Button(control_frame, text="📤 Execute Selected Trade", command=self.execute_selected).pack(side="left", padx=10)
        tk.Button(control_frame, text="🔁 Reconnect Broker", command=self.reconnect_broker).pack(side="left")

    def execute_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a trade first.")
            return
        values = self.tree.item(selected[0])["values"]
        symbol, ttype, strat, conf, reason = values
        mode = self.mode.get()
        print(f"Executing {strat} on {symbol} in {mode} mode.")
        messagebox.showinfo("Trade Executed", f"{symbol} → {strat} trade sent in {mode} mode.")

    def reconnect_broker(self):
        print("🔌 Reconnecting to broker...")
        messagebox.showinfo("Reconnect", "✅ Broker reconnected.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TradingGUI()
    app.run()
