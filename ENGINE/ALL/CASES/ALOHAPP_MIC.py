import sys
import pyaudio
import threading
import atexit
import numpy as np
from PyQt5.QtCore import pyqtSlot

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from ENGINE.ALL.ALOHAPP_MIC import BBL_Form


app = QApplication(sys.argv)
window = BBL_Form()
window.show()
app.exec()
