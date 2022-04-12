from ENGINE.AI.DL.ARCHITECTURES.MLP.Perceptron_Numpy import Perceptron
from ENGINE.AI.DL.ARCHITECTURES.MLP.AdalineSGD_Numpy import AdalineSGD
from ENGINE.LANG.PYTHON.SELF.python_environment_check import check_packages
from ENGINE.LANG.PYTHON.VISUALIZATIONS.MATPLOTLIB.plot_decision_regions import plot_decision_regions
from ENGINE.AI.DL.ARCHITECTURES.lincoln.lincoln.layers import Dense
from ENGINE.AI.DL.ARCHITECTURES.lincoln.lincoln.losses import SoftmaxCrossEntropy, MeanSquaredError
from ENGINE.AI.DL.ARCHITECTURES.lincoln.lincoln.optimizers import Optimizer, SGD, SGDMomentum
from ENGINE.AI.DL.ARCHITECTURES.lincoln.lincoln.activations import Sigmoid, Tanh, Linear, ReLU
from ENGINE.AI.DL.ARCHITECTURES.lincoln.lincoln.network import NeuralNetwork
from ENGINE.AI.DL.ARCHITECTURES.lincoln.lincoln.train import Trainer
from ENGINE.AI.DL.ARCHITECTURES.lincoln.lincoln.utils import mnist
from ENGINE.AI.DL.ARCHITECTURES.lincoln.lincoln.utils.np_utils import softmax
import numpy as np