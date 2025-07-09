"""TODO: Add module description for reinforcement_learner."""

import random
from typing import Iterable, List

import numpy as np


class SimpleTradingEnv:
    """Tiny trading environment for PPO demos."""

    def __init__(self, prices: List[float]):
        self.prices = prices
        self.index = 0
        self.position = 0  # -1 short, 0 flat, 1 long

    def reset(self):
        self.index = 0
        self.position = 0
        return np.array([self.prices[self.index]], dtype=np.float32)

    def step(self, action: int):
        """Take an action and return obs, reward, done, info."""
        prev_price = self.prices[self.index]
        self.index += 1
        done = self.index >= len(self.prices) - 1
        cur_price = self.prices[self.index]
        reward = 0.0
        if action == 1:  # long
            reward = cur_price - prev_price
            self.position = 1
        elif action == 2:  # short
            reward = prev_price - cur_price
            self.position = -1
        obs = np.array([cur_price], dtype=np.float32)
        return obs, reward, done, {}


def train_ppo(prices: Iterable[float], timesteps: int = 1000):
    """Train a PPO agent on price data. Requires stable-baselines3."""
    try:
        from stable_baselines3 import PPO
        from stable_baselines3.common.vec_env import DummyVecEnv
    except Exception:
        print("[WARN] stable_baselines3 not installed. Skipping RL training.")
        return None

    env = DummyVecEnv([lambda: SimpleTradingEnv(list(prices))])
    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=timesteps)
    return model


def offline_rl(logged_actions: List[tuple]):
    """Very small offline RL placeholder using action log."""
    if not logged_actions:
        return {}
    action_counts = {0: 0, 1: 0, 2: 0}
    for _, action in logged_actions:
        action_counts[action] += 1
    total = sum(action_counts.values())
    policy = {k: v / total for k, v in action_counts.items() if total}
    return policy


if __name__ == "__main__":
    data = [random.uniform(10, 15) for _ in range(50)]
    train_ppo(data, timesteps=100)
    logs = [(p, random.choice([0, 1, 2])) for p in data]
    print("Offline policy", offline_rl(logs))
