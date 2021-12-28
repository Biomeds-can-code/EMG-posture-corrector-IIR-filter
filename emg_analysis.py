#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Enables assessment of posture. Allows different methods to notify user of incorrect posture.
'''

import datetime
import time
import iir_filter
import numpy as np
from scipy import signal
import os
import alert


class emg_analysis:

    '''
    This class contains the functions to perform the analysis of an input EMG signal. 
    Intializing the class sets the threshold and sampling frequency of the input signal. 
    Motion of the upper trunk is performed via a match filter. The match filter is a bandpass 
    filter which lets through the frequency of the peak resulting from the extension or 
    flexion of the muscles in the lower back. The result of the match filter is then translated 
    into single detections via the implementation of heuristics in the detector function. 
    '''
    
    def __init__(self):
    
        '''
        Constructor function.
        '''
        
        self.threshold=1e-17 #defined threshold 
        self.fs=250

    def match_filter(self,data):
    
        '''
        The match filter allows the signal at frequencies equal to the frequency of the 
        peak due to the flexion and extension of the trunk through.
    
        Arguments
        ---------
    
        data01: Filtered data from the initial filtering step 
    
    
        Returns 
        -------
    
        y3: Rectified signal containing data for detection 
        '''

        # create a 2nd order order bandpass filter that let's through frequency of motion peaks
        f1 = 0.5
        f2 = 1.5
        sos3 = signal.butter(3, [f1/self.fs*2.0, f2/self.fs*2.0 ], 'bandpass',output='sos')
        iir2 = iir_filter.IIR_filter(sos3)
        
        y3 = []
        y3= iir2.filter(data)
            
        y3=y3*y3 #improve signal to noise ratio of detection 
 
        return y3
        

    def detector(self,data,start_motion,state,start_time):
    
        '''
        The detector function uses the output of the match filter and a defined threshold to notify the user if they are slouching or in a correct position. 
    
        Arguments 
        ---------
    
        data: data after initial filtering
        start_motion: time at which the last recorded slouching/straightening of the trunk was detected
        state: current state (state=1 slouching, state=0 not slouching)
        start_time: time at which the program started 
    
    
        Returns
        -------
    
        start_motion: updated time of last recorded motion (if one was detected)
        state: updated current state (if there was a change)
        '''


        ynew=self.match_filter(data) #match filter output
        time_since_slouch=time.time()-start_motion #calculate time since last detected change in trunk position 
     
        minlen=3 #Minimum length of motion in seconds
        
        if time.time()-start_time<5: #Don't detect anything in the first 5 seconds to let filter settle
            pass 
            
        else:
        
            if ynew>self.threshold and time_since_slouch>minlen: #threshold reached and sufficiend time between last detected trunk motion
                if state==0: #was in not slouched state
                
                    #alert printed in terminal 
                    print('Stop slouching!')
                    print(datetime.datetime.now().time())
                    
                    #audible alert
                    os.system('spd-say "Stop slouching"')
                    
                    #alert printed on popup window
                    sendmessage("--icon=important",'Careful! You are slouching, sit properly!')
                    
                    state=1 #change state to slouching
                    start_motion=time.time() #record time of slouching
                   
		        
                else: #was in slouched state
                
                    #alert printed in terminal 
                    print('Good job! Keep it up!')
                    print(datetime.datetime.now().time())
                    
                    #audible alert 
                    os.system('spd-say "Good job"')
                    
                    #alert printed on popup window 
                    sendmessage("--icon=info",'Correct posture! Keep it up!')
                    
                    state=0 #change state to not slouched 
                    start_motion=time.time() #record time of motion 
                    


            else:
                pass
            
        return start_motion, state

        

        
