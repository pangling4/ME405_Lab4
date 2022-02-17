"""!
@file main.py
This file executes a step input for an RC circuit and subsequently reads
data of the circuit's step response using the Nucleo board's built-in ADC.
A timer interrupt is used to take data at accurate and precise time intervals.
    
@author Jonathan Cederquist
@author Tim Jain
@author Philip Pang

@date   Last Modified 2/16/22
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
## @brief ADC input pin
adc = pyb.ADC(pyb.Pin.board.PC0)

## @brief Queue to store step response data
ADC_data = task_share.Queue('h', 2000, thread_protect = False, name = "ADC_data")

## @brief Counter to turn off interrupt function after specificed time
count = 0

## @brief Maximum number of data points to collect
MAX_data = 2000

#v_ref = adc.read_vref()

# setup timer (this will be used as interrupt)

## @brief Timer 1 used for internal interrupt
tim1 = pyb.Timer (1, freq=1000)

# interrupt call back function
def read_ADC(which_timer):
    '''!
    Callback function which saves the current ADC value to a queue
    @param which_timer The timer which triggers the interrupt
    '''
    # designate count as a 'global' variable so it can be modified internally
    global count
    ADC_data.put(adc.read(), in_ISR = True)
    count += 1
    # end interrupt when # of collected data points reaches 'MAX_data'
    if count > MAX_data:
        tim1.callback(None)

# Step-response output setup
## @brief Output pin to run step response
out_PC1 = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP)

# code below runs step response test for RC circuit in a while True loop
if __name__ == "__main__":        
    while True:
        
        # Clear queue of data
        ADC_data.clear()
        
        # Reset data point counter and reset output pin to low
        count = 0 
        out_PC1.low()
        
        # Pause program until user presses enter
        input("Run step response? [Press 'Enter']")
        
        # Set callback function on timer interrupt service routine
        tim1.callback(read_ADC)
        
        # Read first data point before step response is executed
        ADC_data.get()
       
        # Send 3.3V through PC1
        out_PC1.high()
        
        # Print however many data points were recorded, designated by 'MAX_data'
        for i in range(1, MAX_data):
            # Only read data from queue if there is data
            if ADC_data.any():
                print(i, (ADC_data.get()/4095)*3.3)
        print("Done")
        