import random
 <<<<<<< 274wyc-codex/add-upgrades-to-main.py-with-new-features
from typing import Any

MODELS = ["RandomForest", "GradientBoosted", "LSTM", "BERT"]
DEFAULT_WEIGHTS = {
    "RandomForest": 1.0,
    "GradientBoosted": 1.0,
    "LSTM": 1.0,
    "BERT": 1.0,
}


def model_predict(model: str, features: Any) -> float:
    """Dummy probability prediction for model."""
    return random.random()


def weighted_ensemble_predict(features: Any = None, regime: str | None = None,
                              performance: dict | None = None) -> tuple[int, float]:
    """Return ensemble vote and confidence."""
    weights = DEFAULT_WEIGHTS.copy()
    if regime == "CHOP":
        weights["RandomForest"] *= 1.5
    elif regime == "BULL":
        weights["LSTM"] *= 1.5
    if performance:
        for m, w in performance.items():
            if m in weights:
                weights[m] *= w

    probs = {m: model_predict(m, features) for m in MODELS}
    weighted_sum = sum(probs[m] * weights[m] for m in MODELS)
    total_weight = sum(weights.values())
    confidence = weighted_sum / total_weight if total_weight else 0.0
    pred = 1 if confidence >= 0.5 else 0
    return pred, confidence


if __name__ == "__main__":
    pred, conf = weighted_ensemble_predict()
    print(f"Ensemble prediction: {pred} (confidence {conf:.2f})")
=======
import random
from typing import Any

MODELS = ["RandomForest", "XGBoost", "LSTM", "BERT"]


def model_predict(model: str, features: Any) -> int:
    """Dummy prediction for model."""
    return random.choice([0, 1])


def ensemble_predict(features: Any = None) -> int:
    votes = [model_predict(m, features) for m in MODELS]
    avg = sum(votes) / len(votes)
    return 1 if avg >= 0.5 else 0


if __name__ == "__main__":
    print("Ensemble prediction:", ensemble_predict())
 >>>>>>> main
