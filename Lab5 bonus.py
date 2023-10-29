#This is the bonus assignment for the 5th lab in SED 1115. 
#The goal is to measure the difference in accuracy between the pico oscillator
#and the RTC oscillator using second ticks.

import time
import machine
import matplotlib.pyplot as plt

#This function adds the times in the log files
def addlog(time_pico, time_RTC):
    #(float,float)->None

    #declare file
    file = 'log_file_bonus'

    #add both times in the log file
    with open(file, 'a') as file:
        file.write(time_pico + " " + time_RTC)

#This function gets the time from the RTC
def getRTCtime():
    #()->float

    #initialize the RTC
    rtc = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
    #get the current time
    current_time_hex = rtc.readfrom(0x00, 7)
    #turn the final time into a list
    current_time = list(current_time_hex)
    #turn the current time in a number of seconds (seconds, minutes, hours, days)
    time = current_time[0] + current_time[1]*60 + current_time[2]*3600 + current_time[3]*86400
    #(months and years)
    time += current_time[4]*2628000 + current_time[5]*31536000

    return time

#This single function was created by chatgpt with the prompt "create a plotting function with two lines 
#that will be in function of a file filled like this: file.write(time_pico + " " + time_RTC)"
#It plots the log file
def plot_times_from_file(file_path):
    pico_times = []
    rtc_times = []

    # Read data from the file
    with open(file_path, 'r') as file:
        for line in file:
            time_pico, time_rtc = line.strip().split()  # assuming two space-separated values
            pico_times.append(float(time_pico))
            rtc_times.append(float(time_rtc))

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(pico_times, label='Pico Oscillator', marker='o', markersize=4)
    plt.plot(rtc_times, label='RTC Oscillator', marker='x', markersize=4)
    plt.xlabel('Sample Index')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.title('Pico vs. RTC Oscillator Times')
    plt.grid(True)
    plt.show()

# Usage example:
file_path = 'time_data.txt'  # Replace with your file path
plot_times_from_file(file_path)


try:
    while True:
        #get time from pico
        time_pico = time.time()
        #get time from RTC
        time_rtc = getRTCtime()
        #add result to log every second
        addlog(time_pico, time_rtc)
        time.sleep(1)
except KeyboardInterrupt:
    print("loop ended by user, please refer to the logging file to compare accuracies.")

#initialize answer
answer = None
#ask the user if they want to plot the log file
while answer != 'y' and answer != 'n':
    answer = int(input("Would you like to plot the times to compare accuracies? y/n:  "))
    if answer != 'y' and answer != 'n':
        print("please enter y or n")

if answer == 'y':
    plot_times_from_file('log_file_bonus.txt')