import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QPushButton, QFileDialog, QWidget, QVBoxLayout, QSpinBox, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
# from scipy.signal import convolve


def convolution(x, y, canal1, canal2):
    try:
        x = x[canal1]
        y = y[canal2]
        x_len = len(x)
        y_len = len(y)
        result = []
        for i in range(y_len + x_len - 1):
            res = 0
            for j in range((i + 1)):
                if j < x_len and i - j < y_len:
                    res += x.values[j] * y.values[i - j]
            result.append(res)
        return result
    except:
        print("Error in convolution function — check if you selected the right channels")
        return []


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1000, 1000)
        self.setWindowTitle('Convolution')
        self.initUI()
        self.iff1 = False
        self.iff2 = False
        self.canal1 = 0
        self.canal2 = 0

    def initUI(self):
        self.btn1 = QPushButton('Select CSV File 1', self)
        self.btn1.move(20, 100)
        self.btn1.clicked.connect(self.showDialog1)
        self.btn2 = QPushButton('Select CSV File 2', self)
        self.btn2.move(20, 100)
        self.btn2.clicked.connect(self.showDialog2)
        self.btn3 = QPushButton('Convolution', self)
        self.btn3.move(20, 100)
        self.btn3.clicked.connect(self.getconvoluction)
        self.btn4 = QPushButton('Save convolution to file', self)
        self.btn4.move(20, 100)
        self.btn4.clicked.connect(self.save_to_file)
        self.btn5 = QPushButton('Clear', self)
        self.btn5.move(20, 100)
        self.btn5.clicked.connect(self.empty)

        self.spinBox1 = QSpinBox()
        self.spinBox1.setMinimum(0)
        self.spinBox1.setMaximum(100)
        self.spinBox1.setValue(0)
        self.spinBox1.setSingleStep(1)
        self.spinBox1.valueChanged.connect(self.setCanal1)
        self.spinBox2 = QSpinBox()
        self.spinBox2.setMinimum(0)
        self.spinBox2.setMaximum(100)
        self.spinBox2.setValue(0)
        self.spinBox2.setSingleStep(1)
        self.spinBox2.valueChanged.connect(self.setCanal2)

        self.fig1 = Figure()
        self.ax1 = self.fig1.add_subplot(111)
        self.fig2 = Figure()
        self.ax2 = self.fig2.add_subplot(111)
        self.fig3 = Figure()
        self.ax3 = self.fig3.add_subplot(111)
        self.canvas1 = FigureCanvas(self.fig1)
        self.canvas2 = FigureCanvas(self.fig2)
        self.canvas3 = FigureCanvas(self.fig3)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn1)
        self.layout.addWidget(QLabel("Canal: "))
        self.layout.addWidget(self.spinBox1)
        self.layout.addWidget(self.btn2)
        self.layout.addWidget(QLabel("Canal: "))
        self.layout.addWidget(self.spinBox2)

        self.layout.addWidget(self.btn3)
        self.layout.addWidget(self.btn4)
        self.layout.addWidget(self.btn5)
        self.ax1.plot([])
        self.ax2.plot([])
        self.ax3.plot([])
        self.layout.addWidget(self.canvas1)
        self.layout.addWidget(self.canvas2)
        self.layout.addWidget(self.canvas3)
        self.setLayout(self.layout)

    def showSignal(self, ax, sig, canvas, canal, sig_num):

        try:
            ax.clear()
            ax.plot(sig[canal])
            if sig_num == 0:
                ax.set_title(f'Signal 1: {self.fileName1.split("/")[-1]}; channel {self.canal1}')
            elif sig_num == 1:
                ax.set_title(f'Signal 2: {self.fileName2.split("/")[-1]}; channel {self.canal2}')

            canvas.draw()
        except:
            print("Canal not found")

    def showDialog1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName1, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv)",
                                                        options=options)
        if self.fileName1:
            self.sig1 = pd.read_csv(self.fileName1, sep=";", header=None)
            self.showSignal(self.ax1, self.sig1, self.canvas1, self.canal1, 0)

            self.iff1 = True

    def showDialog2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName2, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv)",
                                                        options=options)
        if self.fileName2:
            self.sig2 = pd.read_csv(self.fileName2, sep=";", header=None)
            self.showSignal(self.ax2, self.sig2, self.canvas2, self.canal2, 1)
            self.iff2 = True

    def getconvoluction(self):
        try:
            if not self.iff1 or not self.iff2:
                raise Exception("Not enough signals")
            else:
                self.conv = convolution(self.sig1, self.sig2, self.canal1, self.canal2)
                self.ax3.clear()
                self.ax3.plot(self.conv)
                self.ax3.set_title(f'Convolution for signal 1: {self.fileName1.split("/")[-1]}; channel {self.canal1} '
                                   f'and signal 2: {self.fileName2.split("/")[-1]}; channel {self.canal2}')
                self.canvas3.draw()
        except Exception as e:
            print(str(e))

    def empty(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
        self.iff1 = False
        self.iff2 = False
        self.fileName1 = ""
        self.fileName2 = ""
        self.sig1 = []
        self.sig2 = []

    def setCanal1(self, value):
        self.canal1 = value
        self.showSignal(self.ax1, self.sig1, self.canvas1, self.canal1, 0)

    def setCanal2(self, value):
        self.canal2 = value
        self.showSignal(self.ax2, self.sig2, self.canvas2, self.canal2, 1)

    def save_to_file(self):
    # save canvas to file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        result_file, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "", "CSV Files (*.csv)",
                                                    options=options)
        if result_file:
            with open(result_file, 'w') as f:
                for i in range(len(self.conv)):
                    f.write(str(self.conv[i]) + '\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
