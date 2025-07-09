from stable_baselines3 import PPO


def train(env):
    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=10000)
    model.save("rl_model")
