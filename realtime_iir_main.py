#!/usr/bin/python3
'''
Plots both channels of the Attys in two different windows. Requires pyqtgraph.
'''
import iir_filter
import numpy as np
from scipy import signal
import threading
import sys
import time
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyattyscomm as c
import emg_analysis

#set channel for data acquisiyion
ch1 = c.AttysComm.INDEX_Analogue_channel_1

# create a global QT application object
app = QtGui.QApplication(sys.argv)

# signals to all threads in endless loops that we'd like to run these
running = True

class QtPanningPlot:

    '''
    
    QtPanningPlot contains the settings for the Qt plots generated. It also contains the add and update functions of new data and sampling frequency label to the plots.
    
    
    '''

    def __init__(self,title,scalel,scaleu):
        self.win = pg.GraphicsLayoutWidget()
        self.win.setWindowTitle(title)
        self.plt = self.win.addPlot()
        self.plt.setLabel('bottom', "Last 500 samples")
        self.plt.setLabel('left', "Amplitude")
        self.scalel=scalel         #plot scaling
        self.scaleu=scaleu
        self.plt.setYRange(self.scalel,self.scaleu)
        self.plt.setXRange(0,500)
        self.curve = self.plt.plot()
        self.data = []
        self.Label = []
        self.fsLabel= pg.TextItem() #Add sampling frequency label
        self.plt.addItem(self.fsLabel)
        self.graph=self.plt.getViewBox()
        self.fsLabel.setParentItem(self.graph)
        self.fsLabel.setPos(10,1)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.timeout.connect(self.updateLabel)
        self.timer.start(100)
        self.layout = QtGui.QGridLayout()
        self.win.setLayout(self.layout)
        self.win.show()
        
    def update(self):
        self.data=self.data[-500:] #only keep last 500 samples
        if self.data:
            self.curve.setData(np.hstack(self.data))
                       
    def updateLabel(self):
        self.Label=self.Label #update sampling frequency label
        self.fsLabel.setText('Sampling Frequency: ' + str(self.Label)+' Hz')
                 
    def addData(self,d):
        self.data.append(d) #add new data to plot
        
    def addLabel(self,fs):
        self.Label=np.round(fs,decimals=2) #add sampling frequency to 2 decimal places


def getDataThread(qtPanningPlot1,qtPanningPlot2):

    '''
    getDataThread is the function on which the main thread acts. It collects the initial filtering of the raw emg data and calls on the EMG analysis to perform the posture detection.
     
     Arguments
     ---------
     
     qtPanningPlot1: instance of unfiltered window
     qtPanningPlot2: instance of filtered window
    
    '''

    scale=2e5 #scaling so amplitude>1
    start_time = time.time() #timestamp at which program started
    
    #Filtering coefficients
    
    #Filtering for 50Hz
    f0 = 48.0
    f1 = 52.0
    fs=250

    sos1 = signal.butter(3, [f0/(fs/2), f1/(fs/2)], 'bandstop', output='sos')
    
    #Filtering for DC, ECG and movement artefacts
  
    f2= 30
    
    sos2= signal.butter(3, [f2/(fs/2)], 'highpass', output='sos')
    
    #create instances of filters with coefficients
    iir1 = iir_filter.IIR_filter(sos1)
    iir2 = iir_filter.IIR_filter(sos2)
        
    analysis = emg_analysis.emg_analysis() #create instance for analysis of EMG signal
    
    #Intializing parameters
    start_motion = 0 #intialize time of detected slouch/correction of position
    state = 0 #start in not slouched state
    sf_time=start_time #initalize time of last time sampling frequency was recorded
    n=0 #initialize index of last sample at which sampling frequency was recorded
    
    while running:
        while c.hasSampleAvailable(): #checking if new sample recorded by attys
            sample = c.getSampleFromBuffer()
            sample=sample[ch1]*scale
            sample2= iir1.filter(iir2.filter(sample)) #perform filtering 
            
            #add new samples to unfiltered and filtered plots
            qtPanningPlot1.addData(sample) 
            qtPanningPlot2.addData(sample2)
           
            data.append(sample) #collect unfiltered data for sampling frequency handler
            
            #Perform detection 
            [start_motion,state]=analysis.detector(sample2,start_motion,state,start_time)
            
            #call handler function
            [sf_time,n]=sampling_frequency_handler(sf_time,data,n)
            
            
def sampling_frequency_handler(sf_time,data,n):

    
        '''
        The sampling_frequency_handler calculates the sampling frequency using the number of data collected in the last 3 seconds.
    
        Arguments
        ---------
        
        sf_time: time of last sampling frequency recording 
        data: data collected so far
        n: number of data samples last time sampling frequency was recorded
    
        Returns 
        -------
    
        n_sample_t: if sampling frequency has been calculated returns time at which operation occured
        nsamples: returns number of samples in data at which the last sampling frequency was calculated 
        '''



        t_since_last=time.time()-sf_time #difference between current time and last time sampling frequency was recorded

        if t_since_last>(3): #if 3 seconds have passed since last time fs was recorded
    
            nsamples=len(data) #calculate how many data in the sample 
            fs=(nsamples-n)/t_since_last #number of new data/time passed
        
            #add most recent sampling rate to plots
            qtPanningPlot1.addLabel(fs)
            qtPanningPlot2.addLabel(fs)
        
            new_sf_time=time.time() #update time at which last fs was calculated 
        
            return [new_sf_time,nsamples]
        
        else:
    
            return [sf_time,n]

    

data=[] #initialize data 

#start attys scanning 
s = c.AttysScan()
s.scan()
c = s.getAttysComm(0)
if not c:
    print("No Attys connected and/or paired")
    sys.exit()


# Instance of unfiltered and filtered data windows and set yaxis limits
qtPanningPlot1 = QtPanningPlot("Unfiltered",1600,3500)
qtPanningPlot2 = QtPanningPlot("Filtered",-300,300)

# create a thread which gets the data from the Attys
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
