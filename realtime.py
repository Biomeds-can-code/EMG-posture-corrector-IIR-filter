#!/usr/bin/python3
"""
Plots both channels of the Attys in two different windows. Requires pyqtgraph.

"""
import iir_filter
import numpy as np
from scipy import signal
import threading
from time import sleep
import sys

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

import numpy as np

import pyattyscomm as c

import emg_analysis

ch1 = c.AttysComm.INDEX_Analogue_channel_1

# create a global QT application object
app = QtGui.QApplication(sys.argv)

# signals to all threads in endless loops that we'd like to run these
running = True

class QtPanningPlot:

    def __init__(self,title):
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle(title)
        self.plt = self.win.addPlot()
        self.plt.setYRange(-1,1)
        self.plt.setXRange(0,500)
        self.curve = self.plt.plot()
        self.data = []
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        self.layout = QtGui.QGridLayout()
        self.win.setLayout(self.layout)
        self.win.show()
        
    def update(self):
        self.data=self.data[-500:]
        if self.data:
            self.curve.setData(np.hstack(self.data))

    def addData(self,d):
        self.data.append(d)


def getDataThread(qtPanningPlot1,qtPanningPlot2):

    #Filtering for 50Hz and DC
    f0 = 48.0
    f1 = 52.0
    fs=250

    sos1 = signal.butter(3, [f0/(fs/2), f1/(fs/2)], 'bandstop', output='sos')
        
    f2 = 0.25
    f3 = 124
    sos2 = signal.butter(3, [f2/(fs/2), f3/(fs/2)], 'bandpass', output='sos')
        
    iir1 = iir_filter.IIR_filter(sos1)
    iir2 = iir_filter.IIR_filter(sos2)
        

    global data 
    i=0
    last=0
    analysis=emg_analysis.emg_analysis()
    start_slouch=0
    state=0
    
    while running:
        # loop as fast as we can to empty the kernel buffer
        while c.hasSampleAvailable():
            sample = c.getSampleFromBuffer()
            sample=sample[ch1]
            sample2= iir1.filter(iir2.filter(sample))
            sample22=analysis.match_filter(sample2)
            qtPanningPlot1.addData(sample)
            qtPanningPlot2.addData(sample22)
            data.append(sample)
            [start_slouch,state]=analysis.detector(sample2,start_slouch,state)
        # let Python do other stuff and sleep a bit
        sleep(0.1)

s = c.AttysScan()
s.scan()
c = s.getAttysComm(0)
if not c:
    print("No Attys connected and/or paired")
    sys.exit()

data=[]


# Let's create two instances of plot windows
qtPanningPlot1 = QtPanningPlot("Unfiltered")
qtPanningPlot2 = QtPanningPlot("Filtered")

# create a thread which gets the data from the USB-DUX
t = threading.Thread(target=getDataThread,args=(qtPanningPlot1,qtPanningPlot2,))

# start data acquisition
c.start()

# start the thread getting the data
t.start()

# showing all the windows
app.exec_()

c.quit()

# Signal the Thread to stop
running = False

# Waiting for the thread to stop
t.join()


print("finished")
