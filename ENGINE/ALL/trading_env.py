import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class TradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=10,shape=(1,16), dtype=np.float32)
        self.seed()
        self.money = 10000
        self.state = None

    def step(self, action):
      err_msg = "%r (%s) invalid" % (action, type(action))
      assert self.action_space.contains(action), err_msg

      self.state = (1,2,3,4,self.money)
      done = bool(
        self.money <= 0
      )

      reward = 0
      if not done:
        reward = 1.0

      return np.array(self.state), reward, done, {}


    def reset(self):
      return np.array(self.state)

    def render(self, mode='human', close=False):
      pass

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
