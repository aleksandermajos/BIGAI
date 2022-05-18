import matplotlib.pyplot as plt
import numpy as np

#https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.html#:~:text=pyplot%20is%20a%20state%2Dbased,%2C%200.1)%20y%20%3D%20np.
#

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.plot(x, y, 'o', color='black')
plt.show()