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


class MicrophoneRecorder(object):
    def __init__(self, rate=4000, chunksize=1024):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        atexit.register(self.close)

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames

    def start(self):
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()


class BBL_Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Widgets App")
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox())
        button = QPushButton('USE MICROPHONE!', self)
        layout.addWidget(button)
        layout.addWidget(QLabel())
        layout.addWidget(QLineEdit())

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        button.clicked.connect(self.on_click)


    def handleNewData(self):
        pass

    @pyqtSlot()
    def on_click(self):
        print('USE MIC!')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BBL_Form()
    window.show()
    app.exec()
