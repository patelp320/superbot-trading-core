import random
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
