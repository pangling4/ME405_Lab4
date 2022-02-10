"""!
@file main.py
    
    
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

import micropython
micropython.alloc_emergency_exception_buf(100)

# ADC data read-in setup
adc = pyb.ADC(pyb.Pin.board.PA5)
ADC_data = task_share.Queue('h', 1000, thread_protect = False, name = "ADC_data")
count = 0
MAX_data = 100

# interrupt setup
tim1 = pyb.Timer (1, freq=1000)

def read_ADC(which_timer):
    global count
    ADC_data.put(adc.read(), in_ISR = True)
    count += 1
    if count > MAX_data:
        tim1.callback(None)

# Step-response output setup
out_PC1 = pyb.Pin (pyb.Pin.board.PA4, pyb.Pin.OUT_PP)

if __name__ == "__main__":    
    
    while True:
        ADC_data.clear()
        out_PC1.low()
        count = 0
        input("Run step response? [Press 'Enter']")
        tim1.callback(read_ADC)
        print(0, ADC_data.get())
        out_PC1.high()
        start = utime.ticks_ms()
        for i in range(1, MAX_data): # roughly 1000 milliseconds
            if ADC_data.any():
                print(i, ADC_data.get())                
        