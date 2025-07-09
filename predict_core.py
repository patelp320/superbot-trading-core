# predict_core.py — placeholder for prediction logic

import logging; logging.basicConfig(level=logging.INFO)
from datetime import datetime, timezone
import random
from ai_modules.news_sentiment_ai import load_scores
from ai_modules.multi_model_ensemble import weighted_ensemble_predict
from ai_modules.macro_trend_ai import current_regime

def predict():
    regime = current_regime()
    print(f"[{datetime.now(timezone.utc)}] Market regime: {regime}")
    gap_signal = random.random() > 0.8
    mean_revert_signal = random.random() > 0.7
    vote, confidence = weighted_ensemble_predict(regime=regime)
    sentiment = load_scores()

    avoid_trade = any(v < -0.5 for v in sentiment.values())

    if gap_signal:
        print(f"[{datetime.now(timezone.utc)}] 📈 Gap-and-Go signal detected")
    if mean_revert_signal:
        print(f"[{datetime.now(timezone.utc)}] 🔻 Mean reversion short signal")
    if vote:
        print(f"[{datetime.now(timezone.utc)}] 🧠 Ensemble vote suggests entry; confidence {confidence:.2f}")

    level = "✅ High" if confidence >= 0.9 else "🟡 Medium" if confidence >= 0.7 else "⚠️ Low"
    print(f"[{datetime.now(timezone.utc)}] {level} confidence {confidence:.2f}")
    if confidence < 0.7:
        print(f"[{datetime.now(timezone.utc)}] Skipping trade")
        return
    if avoid_trade:
        print(f"[{datetime.now(timezone.utc)}] 🚩 Negative news detected. Avoiding trades")
    if not any([gap_signal, mean_revert_signal, vote]) or avoid_trade:
        print(f"[{datetime.now(timezone.utc)}] 🔮 Running basic prediction logic...")

if __name__ == "__main__":
    predict()
