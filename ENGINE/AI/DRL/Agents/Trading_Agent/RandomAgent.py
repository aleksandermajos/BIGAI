from typing import List
import random
import gym
import Trading_env

class RandomAgent:
    def __init__(self):
        self.total_reward = 0.0
        self.env = gym.make('Trading_env-v0')

    def step(self):
        actions = self.env.action_space
        state, reward, done, _ = self.env.step(self.env.action_space.sample())
        self.total_reward += reward

Agent = RandomAgent()
ruch = Agent.step()