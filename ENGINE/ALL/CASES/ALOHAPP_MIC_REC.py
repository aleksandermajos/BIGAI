import sys
import matplotlib.pyplot as plt
plt.switch_backend('Qt5Agg')
from PyQt5 import QtGui, QtCore, QtWidgets
from ENGINE.ALL.ALOHAPP_MIC_REC import LiveFFTWidget


app = QtWidgets.QApplication(sys.argv)
window = LiveFFTWidget()
sys.exit(app.exec_())