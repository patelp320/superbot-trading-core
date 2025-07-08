# predict_core.py — placeholder for prediction logic

from datetime import datetime
import random
from ai_modules.news_sentiment_ai import load_scores
 <<<<<<< 274wyc-codex/add-upgrades-to-main.py-with-new-features
from ai_modules.multi_model_ensemble import weighted_ensemble_predict
=======
from ai_modules.multi_model_ensemble import ensemble_predict
 >>>>>>> main
from ai_modules.macro_trend_ai import current_regime

def predict():
    regime = current_regime()
    print(f"[{datetime.utcnow()}] Market regime: {regime}")
    gap_signal = random.random() > 0.8
    mean_revert_signal = random.random() > 0.7
 <<<<<<< 274wyc-codex/add-upgrades-to-main.py-with-new-features
    vote, confidence = weighted_ensemble_predict(regime=regime)
=======
    vote = ensemble_predict()
 >>>>>>> main
    sentiment = load_scores()

    avoid_trade = any(v < -0.5 for v in sentiment.values())

    if gap_signal:
        print(f"[{datetime.utcnow()}] 📈 Gap-and-Go signal detected")
    if mean_revert_signal:
        print(f"[{datetime.utcnow()}] 🔻 Mean reversion short signal")
    if vote:
 <<<<<<< 274wyc-codex/add-upgrades-to-main.py-with-new-features
        print(f"[{datetime.utcnow()}] 🧠 Ensemble vote suggests entry; confidence {confidence:.2f}")
    if confidence < 0.7:
        print(f"[{datetime.utcnow()}] ⚠️ Low confidence {confidence:.2f}. Skipping trade")
        return
=======
        print(f"[{datetime.utcnow()}] 🧠 Ensemble vote suggests entry")
 >>>>>>> main
    if avoid_trade:
        print(f"[{datetime.utcnow()}] 🚩 Negative news detected. Avoiding trades")
    if not any([gap_signal, mean_revert_signal, vote]) or avoid_trade:
        print(f"[{datetime.utcnow()}] 🔮 Running basic prediction logic...")

if __name__ == "__main__":
    predict()
