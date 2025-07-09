import pickle
import os
import random

Q_FILE = "q_table.pkl"

class ReinforcementLearner:
    """Simple reinforcement learning framework using a Q-table."""

    def __init__(self):
        self.q_table = self.load_q_table()
        self.pnl_history = {}

    def load_q_table(self):
        if os.path.exists(Q_FILE):
            try:
                with open(Q_FILE, "rb") as f:
                    return pickle.load(f)
            except Exception:
                return {}
        return {}

    def save_q_table(self):
        with open(Q_FILE, "wb") as f:
            pickle.dump(self.q_table, f)

    def update(self, strategy_name: str, pnl: float):
        """Update Q value for a strategy based on profit/loss."""
        self.pnl_history.setdefault(strategy_name, []).append(pnl)
        reward = pnl
        self.q_table[strategy_name] = self.q_table.get(strategy_name, 0.0) + reward
        self.save_q_table()

    def recommend(self):
        """Return a strategy weighted by learned Q values."""
        if not self.q_table:
            return None
        strategies, values = zip(*self.q_table.items())
        total = sum(max(v, 0.0) for v in values)
        if total <= 0:
            return random.choice(strategies)
        weights = [max(v, 0.0) / total for v in values]
        return random.choices(strategies, weights=weights, k=1)[0]
