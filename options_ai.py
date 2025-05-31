import os
import pickle
from datetime import datetime

model_dir = "../models"
log_file = "../logs/trades.log"
os.makedirs("../logs", exist_ok=True)

print(f"[{datetime.utcnow()}] 📊 Checking model scores...")

with open(log_file, "a") as log:
    for file in os.listdir(model_dir):
        if file.endswith(".pkl"):
            path = os.path.join(model_dir, file)
            with open(path, "rb") as f:
                model = pickle.load(f)
                score = model["avg_return"] / model["volatility"] if model["volatility"] > 0 else 0
                print(f"{model['ticker']} — Score: {round(score, 3)}")
                
                if score > 0.4:
                    msg = f"[{datetime.utcnow()}] 📈 Consider selling CSP on {model['ticker']} | Alpha Score: {round(score, 3)}\n"
                    log.write(msg)

if __name__ == "__main__":
    print("[OPTIONS AI] Module ready for direct use.")
