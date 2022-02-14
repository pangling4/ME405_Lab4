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
    
        # PLOTTING
        fig, plt = pp.subplots()
        plt.plot(timeList, positionList)
        plt.set(xlabel = "Time [ms]", ylabel = "Voltage")
        plt.set(title = "RC Circuit Step Response")
    
        # set y limits of plot in radians
        plt.set_ylim(0,4)
    
        # display plot
        pp.show()
    
    except KeyboardInterrupt:
        break

print('\nGoodbye')
