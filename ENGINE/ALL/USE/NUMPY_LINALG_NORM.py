import numpy as np

# https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html
# https://www.geeksforgeeks.org/find-a-matrix-or-vector-norm-using-numpy/
# Calculate length/distance of the vector/matrix

# initialize vector
vec = np.arange(10)
# compute norm of vector
vec_norm = np.linalg.norm(vec)

print("Vector norm:")
print(vec_norm)