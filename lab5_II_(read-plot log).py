'''This program work along the lab5.py program. It reads the log.txt file that contains all the results to the tests
and plots a graph of how many times each result was obtained.

Nathan Savard
october 18 2023'''

import matplotlib.pyplot as plt
import sys
import time

#this function will put the log in a list
def put_file_in_a_list():
    #()->list
    try:
        with open("log.txt", 'r') as file:
            log_list = file.readlines()
        return log_list
    except:
        print("It would seem that there is an issue with reading the file")
        sys.exit()

#This function will find all different occurences in the log and count how many times they each happened
def get_plot_contents(log_list):
    #(list)->dict

    #initialize the occurences list
    new_occurence_list = []
    #initialize the dictionary containing all the unique occurences and how many time they happen
    how_many_occurences_dict = {}
    #put all new occurences in new_occurence_list (they will be unique)
    for time in log_list:
        if time not in new_occurence_list:
            new_occurence_list.append(time)
    #initialize all the occurences in the dictionary at 0
    for occurence in new_occurence_list:
        if occurence not in how_many_occurences_dict:
            how_many_occurences_dict[occurence] = 0
    #count the number of instances for each occurance
    for occurence in log_list:
        how_many_occurences_dict[occurence] += 1

    return how_many_occurences_dict


#This function will create and show the plot
def plot_result(occurences_dict):
    #(dict)->None

    #create the list used for the plot
    num_times_list = list(occurences_dict.values())#y axis

    #construct the plot object
    plt.hist(num_times_list, len(num_times_list), align='mid')

    #add time labels for each occurence (keys in the dict) (the first argument is how many labels there are)
    plt.xticks(range(1, len(occurences_dict) +1 ), occurences_dict.keys())

    #add labels to the plot
    plt.xlabel("Time")
    plt.ylabel("Number of occurences")
    plt.title("Number of times each test result was obtained")

    #announce to the user that the plot will be shown
    print("This plot contains how many times each test result was obtained")

    #give the user time to read the message
    time.sleep(5)

    #show the plot
    plt.show()


#main

log_list = put_file_in_a_list()
results_dict = get_plot_contents(log_list)
plot_result(results_dict)