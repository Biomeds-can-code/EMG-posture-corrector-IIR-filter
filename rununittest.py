#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Code to run unit test for both 2nd order IIR filter
and chain of 2nd order filters.
'''

import numpy as np
from scipy import signal
import iir_filter

class rununittest:
    
    '''
    This class runs the unit test for a 2nd order IIR filter and a chain of 2nd 
    order filters. The unit test evaluates the results of 50Hz removal using a 
    Butterworth filter. The output of the filter was computed by hand in the 
    function calculate_expected output.
    '''
    
    def __init__(self):

        f0 = 48.0 #lower cutoff frequency
        f1 = 52.0 #upper cutoff frequency
        fs = 250 #sampling frequency
        
        
        self.x=[1,2,3] #test input signal 
        self.sos = signal.butter(2, [f0/(fs/2), f1/(fs/2)], 'bandstop', output='sos') #Filter coefficients
        self.expected_output=self.calculate_expected_output() #Calculate expected output 'by hand'.
    
    
    def calculate_expected_output(self):
    
        '''
        This function calculates 'by hand' the expected output from a 2nd order Butterworh bandstop filter.
        
        Returns
        -------
        
        yout: expected output from input x=[1,2,3]
        
        
        '''
        
        #Calculate by hand the output for the IIR filter using bandstop coefficients of the high level commands
        
        #First 2nd order coefficients
        
        s1=self.sos[0]
        
        b00=s1[0]
        b01=s1[1]
        b02=s1[2]
        a01=s1[4]
        a02=s1[5]
        
        y=np.zeros(len(self.x))      
        
        #compute output 
        y[0]=1*b00
        y[1]=(2+1*-a01)*b00+b01*1
        y[2]=(3+((2+1*-a01)*-a01)+1*-a02)*b00+(2+1*-a01)*b01+1*b02
        
        
        #Second 2nd order coefficients
        xin=y
        
        s2=self.sos[1]
        b10=s2[0]
        b11=s2[1]
        b12=s2[2]
        a11=s2[4]
        a12=s2[5]
        
        #compute ouput
        yout=np.zeros(len(self.x))          
        yout[0]=xin[0]*b10
        yout[1]=(xin[1]+(xin[0]*-a11))*b10+xin[0]*b11
        yout[2]=(xin[2]+(xin[1]+(xin[0]*-a11))*-a11+xin[0]*-a12)*b10+(xin[1]+(xin[0]*-a11))*b11+xin[0]*b12
        
        return yout
                
    
    def test_IIR2_filter(self):
        
        '''
        
        This function computes a unit test for a 2nd Order IIR Filter 
        using bandstop Butterworth filter coefficients and returns a success or failed statement.
        
        '''
        
        
        first_sos= iir_filter.IIR2_filter(self.sos[0]) #obtain coefficients for first 2nd order filter
        second_sos= iir_filter.IIR2_filter(self.sos[1]) #Obtain coefficients for second 2nd order filter 
        
        x2=np.zeros(len(self.x))
        y=np.zeros(len(self.x))
        
        for i in range(len(self.x)) :  
            x2[i]=first_sos.filter(self.x[i]) #First filter signal with coefficients of first filter
            y[i] =second_sos.filter(x2[i]) #Filter output through filter with second coefficients to get bandstop
                       
        if np.array_equal(y,self.expected_output): #compare against expected output
            
            print('Yes! It works!')
            
        else:
            print('Oh no! There is a bug in the code!')
    
    

    def test_IIR_filter(self):
        
       '''
       
       This function computes a unit test for a chain of 2nd Order Filters
       using bandstop Butterworth filter coefficients and returns a success or failed statement.
       
       '''
       
       
       iir1 = iir_filter.IIR_filter(self.sos)
       y2 = np.zeros(len(self.x))
        
       for i in range(len(self.x)):
           y2[i] = iir1.filter((self.x[i])) #filter input signal one by one through chain on 2nd order filters
                         
       if np.array_equal(y2,self.expected_output)==True: #compare against expected output
            
           print('Yes! It works!')
            
       else:
           print('Oh no! There is a bug in the code!')

    
    
trial=rununittest()
print('Starting unit test for iir_filter.IIR2 filter...')
trial.test_IIR2_filter()
print('Starting unit test for iir_filter.IIR filter...')
trial.test_IIR_filter()
