import numpy as np

#https://www.w3resource.com/numpy/manipulation/unique.php
#return unique values from array if needed with indices
x = np.array([0, 1, 2, 5, 2, 6, 5, 2, 3, 1])
u, indices = np.unique(x, return_inverse=True)
