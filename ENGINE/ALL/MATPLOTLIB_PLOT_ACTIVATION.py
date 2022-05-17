import matplotlib.pyplot as plt

def plotActivation(x,activation):
    points = activation(x)
    plt.plot(x, points)
    plt.axvline(0.0, color='k')
    plt.ylim(-0.1, 1.1)
    plt.xlabel('z')
    plt.ylabel('$\points (z)$')
    plt.yticks([0.0, 0.5, 1.0])
    ax = plt.gca()
    ax.yaxis.grid(True)
    plt.tight_layout()
    plt.show()
