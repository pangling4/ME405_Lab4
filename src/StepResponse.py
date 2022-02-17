"""!
@file StepResponse.py
 Test program to communicate with nucleo board through
 serial USB connection. Asks user to input proportional
 gain to be used and plots the RC circuit's step response
 vs time data.

@author Jonathan Cederquist
@author Tim Jain
@author Philip Pang

@date   2-Feb-2022
"""

import serial
from matplotlib import pyplot as pp
from matplotlib.ticker import(MultipleLocator)
import math
while True:
    
    try:
        # initialize data arrays to plot
        timeList = []
        positionList = []
        badVals = []
    
        # open serial communication
        with serial.Serial ('COM3', 115200, timeout = 1) as s_port:
            
            # prompts user for Kp, and codes string into a byte
            kp = bytes(input("Run step response? [Press 'Enter']"), 'utf-8')
            # writes user specified Kp to serial communication and "enters"
            s_port.write(b'\r')
    
            # motor choice functionality does not exist yet
            # motor = bytes(input("Specify which motor to run [1,2]: "), 'utf-8')
            # s_port.write(motor, b'\r')
            
            # need to read first line in advance because that's where the enter command input is
            s_port.readline()
            
            while s_port.inWaiting==0:
                pass
            
            print(s_port.inWaiting)
            
            # infinite loop 
            while s_port.inWaiting != 0:
                try:
                    line = s_port.readline().strip(b'\r\n').split(b' ')
                    val1 = line[0].decode()
                    val2 = line[1].decode()
                    
                    timeList.append(float(val1))
                    positionList.append(float(val2))
                    # print to track progress and trace errors
                    print(line)
                    
                # stops data collection when readline takes in the
                # line that prompts for an Kp input
                except ValueError:
                    badVals.append(line)
                    
                except IndexError:
                    break
    
        print("Data Collection Complete")
    
        lastVal = positionList[-1]
        lastTime = timeList[-1]
        
        valArray = [lastVal, lastVal]
        timeArray = [0, lastTime]
        
        #Voltage at 1 time constant
        V = lastVal*(1-math.exp(-1))
        print('The voltage at one time constant is: ', V, ' volts')
        #Voltage array for plotting time constant voltage
        tauVArray = [V, V]
        
        vArray = len(positionList)*[V]
        newArray = []
        for i in range(len(positionList)):
            newArray.append(abs(positionList[i]-vArray[i]))
        mimiVal = min(newArray)
        tauIndex = newArray.index(mimiVal)
        tauTime = timeList[tauIndex]
        print('The time constant is at t=: ', tauTime, ' s')
        tauTArray = [tauTime, tauTime]
        tauVertical = [0, V]
        # PLOTTING
        fig, plt = pp.subplots()
        plt.plot(timeList, positionList)
        plt.set(xlabel = "Time [ms]", ylabel = "Voltage")
        plt.set(title = "RC Circuit Step Response")
        # Create minor ticks on Voltage axis
        plt.yaxis.set_minor_locator(MultipleLocator(0.1))
        
        plt.plot(timeArray, valArray)
        plt.plot(timeArray, tauVArray)
        plt.plot(tauTArray, tauVertical)
        # set y limits of plot in radians
        V_new = format(V, '.2f')
        plt.set_ylim(0,4)
        label = f"({tauTime},{V_new})"
        plt.annotate(label, # this is the text
        (tauTime,V), # these are the coordinates to position the label
        textcoords="offset points", # how to position the text
        xytext=(0,10), # distance from text to points (x,y)
        ha='center') # horizontal alignment can be left, right or center
        # display plot
        pp.show()
    
    except KeyboardInterrupt:
        break

print('\nGoodbye')
