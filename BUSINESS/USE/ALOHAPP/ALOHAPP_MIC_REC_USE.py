import sys
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from BUSINESS.USE.ALOHAPP.ALOHAPP_MIC_REC import LiveFFTWidget
plt.switch_backend('Qt5Agg')

app = QtWidgets.QApplication(sys.argv)
window = LiveFFTWidget()
sys.exit(app.exec_())