"""!
@file main.py
This file executes a step input for an RC circuit and subsequently reads
data of the circuit's step response using the Nucleo board's built-in ADC.
A timer interrupt is used to take data at accurate and precise time intervals.
    
@author Jonathan Cederquist
@author Tim Jain
@author Philip Pang

@date   Last Modified 2/10/22
"""

import gc
import pyb
import task_share

import math
import utime

# code to allow for interrupt callbacks to print exception messages
import micropython
micropython.alloc_emergency_exception_buf(100)

# ADC data read-in setup
adc = pyb.ADC(pyb.Pin.board.PC0)
ADC_data = task_share.Queue('h', 1100, thread_protect = False, name = "ADC_data")
count = 0
MAX_data = 2000 # number of data points to collect
#v_ref = adc.read_vref()

# setup timer (this will be used as interrupt)
tim1 = pyb.Timer (1, freq=1000)

# interrupt call back function
def read_ADC(which_timer):
    # designate count as a 'global' variable so it can be modified internally
    global count
    ADC_data.put(adc.read(), in_ISR = True)
    count += 1
    # end interrupt when # of collected data points reaches 'MAX_data'
    if count > MAX_data:
        tim1.callback(None)

# Step-response output setup
out_PC1 = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP)

# code below runs step response test for RC circuit in a while True loop
if __name__ == "__main__":        
    while True:
        ADC_data.clear()
        count = 0 # reset data point counter 
        out_PC1.low()
        
        # pause program until user 
        input("Run step response? [Press 'Enter']")
        # set callback function on timer interrupt service routine
        tim1.callback(read_ADC) 
        # print first data point before step response is executed
        ADC_data.get()
       
        # send 3.3V through PC1
        out_PC1.high()
        
        # print however many data points were recorded, designated by 'MAX_data'
        for i in range(1, MAX_data):
            # only read data from queue if there is data
            if ADC_data.any():
                print(i, (ADC_data.get()/4095)*3.3)
        print("Done")
        