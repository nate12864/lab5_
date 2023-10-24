'''This program is made for the fifth lab of the SED 1115 class.
It calculates the time between the first press of a button and the second press (user
presses the second time when they think 15s elapsed) displays the actual time on the
console. This program also uses a log.txt file that records all the tries
A second program exists for the graphing of the data in the log.txt file

Nathan Savard
october 20 2023'''
import time
import machine
import sys

#this function will detect button presses
def press_detect():
    #()->bool

    #set button pin
    button = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)

    #detect button press
    notpressed = True
    while notpressed:
        if button.value == 0:
            #if the button is pressed again withoin 1s, it will not be taken into account as it is either a rebound or 
            #a mistake from the user (clearly not 15s)
            time.sleep(1)
            notpressed = False
    
    #return True once the button is pressed
    return True

#This function will create the I2C object, namely the DS3231 Real Time Clock chip that will calculate the time
def create_I2C_rtc():
    #()->I2C

    #initiate I2C object
    i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))

    return i2c

#This function will add every result in the log.txt file
def log_append_results(actual_time):
    #(float)->None

    #set the file variable
    log_file = "log.txt"

    #turn actual_time in a string to make the log for better readability
    actual_time = str(actual_time)

    #add the time in the log file
    try:
        with open(log_file, 'a') as file:
            file.write(actual_time)
    except:
        print("It would seem that the file is not present in the path, please make sure it is in the same folder as the code.")
        sys.exit()

#This function will start the timer and return the actual time taken before the user clicked the button again
def timer():
    #()->float

    #start taking time from the real time clock chip
    #initiate rtc
    rtc = create_I2C_rtc()

    #the intial time is january 1st, 2000, 00:00:00
    initial_time_for_rtc = bytes([0x00, 0x00, 0x00, 0x01, 0x01, 0x00])
    initial_time_for_substraction = list(initial_time_for_rtc)
    for i in range(len(initial_time_for_substraction)):
        i = int(hex(initial_time_for_substraction[i]))

    #set time to 0 to avoid issues with time conversions with minutes, hours, etc.
    rtc.writeto(0x68, initial_time_for_rtc)
    #detect second button press
    pressed_again = False
    final_time_list_hex = []
    while not pressed_again:
        pressed_again = press_detect()
        if pressed_again:
            #extract the time after the button is pressed for the second time
            final_time_list_hex = rtc.readfrom(0x00, 7)
    
    delta_list = []
    #convert the final time to a list for the calculations
    final_time_list = list(final_time_list_hex)
    #substract intial time to final time to find the delta
    for i in range(len(initial_time_for_substraction)):
        delta_list.append(final_time_list[i] - initial_time_for_substraction[i])

    #calculate final time (seconds, minutes, hours, days)
    final_time = delta_list[0] + delta_list[1]*60 + delta_list[2]*3600 + delta_list[3]*86400
    #months and years
    final_time += delta_list[4]*2628000 + delta_list[5]*31536000

    #return final time
    return final_time

#This function will show the initial messages for the user
def foruser():
    #()->None

    #print initial message for user
    print("This program will evaluate your perception of time.")
    print("Press the button once and press it again when you believe 15s have elasped.")
    print("To view your overall evaluation, use the lab5_II program that will plot your results.")
    print("To end the program, press CTRL + c at the same time, otherwise, the test will keep repeating, allowing you to account for more tries.")
    print("Good luck!")

#This function will show the actual time taken by the user to press the button
def final_display(actual_time):
    #(float)->None

    #display time
    print("The time taken between the two button presses is: " + actual_time + "s")

foruser()

try:
    while True:
        if press_detect():
            actual_time = timer()
            log_append_results(actual_time)
            final_display(actual_time)
            print("\nYou can press the button again if you wish to redo the test. Otherwise, please press CTRL + c or stop running the code.")

except KeyboardInterrupt:
    print("Program ended by user.")