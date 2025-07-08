
def size_position(capital: float, risk: float, confidence: float) -> float:
    kelly = (confidence - (1 - confidence)) / risk
    return capital * max(0.0, min(kelly, 0.05))
