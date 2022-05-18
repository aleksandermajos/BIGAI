import numpy as np

# https://numpy.org/doc/stable/reference/generated/numpy.where.html
# (condition, what object, what to do)

a = np.arange(10)
res = np.where(a < 5, a, 10*a)

oko =5