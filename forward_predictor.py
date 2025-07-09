import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from sklearn.preprocessing import MinMaxScaler


def train_lstm_predict(file):
    df = pd.read_csv(file)
    data = df["Close"].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(data)

    X, y = [], []
    for i in range(20, len(scaled)-3):
        X.append(scaled[i-20:i])
        y.append(scaled[i:i+3])

    X, y = np.array(X), np.array(y)
    model = Sequential([
        Input(shape=(20, 1)),
        LSTM(50, activation="relu"),
        Dense(3)
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=10, verbose=0)

    latest = scaled[-20:].reshape(1, 20, 1)
    prediction = model.predict(latest)
    result = scaler.inverse_transform(prediction.reshape(-1, 1))

    pd.DataFrame(result, columns=["Predicted"]).to_csv("predicted_prices.csv", index=False)
    print("[LSTM] ✅ Prediction complete.")
