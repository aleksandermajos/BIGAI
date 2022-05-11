import sys
from PyQt5.QtWidgets import QApplication
from ENGINE.ALL.ALOHAPP_MIC import BBL_Form


app = QApplication(sys.argv)
window = BBL_Form()
window.show()
app.exec()
