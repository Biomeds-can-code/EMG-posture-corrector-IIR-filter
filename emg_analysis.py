#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 09:08:39 2021

@author: sofiahernandezgelado
"""
import datetime
import time
import iir_filter
import numpy as np
from scipy import signal
import os

class emg_analysis:
    
    def __init__(self):
        
        self.threshold=10e-17
        self.fs=250
        self.i=0
    
    def match_filter(self,data01):

        # create a 2nd order order bandpass filter
        f1 = 0.5
        f2 = 1.5
        sos3 = signal.butter(3, [f1/self.fs*2.0, f2/self.fs*2.0 ], 'bandpass',output='sos')
        b,a = signal.butter(3, [f1/self.fs*2.0, f2/self.fs*2.0 ], 'bandpass')
        iir2 = iir_filter.IIR_filter(sos3)
        
        y3 = []
        y3= iir2.filter(data01)
            
        y3=y3*y3
 
        return y3
        

    def detector(self,data,start_slouch,state):
    
    #state=1 slouching, state=0 not slouching 

        ynew=self.match_filter(data)
        time_since_slouch=time.time()-start_slouch
     
        minlen=3 #Minimum length of motion
        
        if ynew>self.threshold and time_since_slouch>minlen:
        
            if state==0:
                print('Stop slouching!')
                print(datetime.datetime.now().time())
                state=1
                start_slouch=time.time()
                os.system('spd-say "Stop slouching"')
                
            else:
                print('Good job! Keep it up!')
                print(datetime.datetime.now().time())
                state=0
                start_slouch=time.time()
                os.system('spd-say "Good job"')


        else:
          pass
            
        return start_slouch, state

        

        
