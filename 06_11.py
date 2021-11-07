# import packages #########################################################################################

import sys
import pyaudio
import datetime
import pandas as pd
import numpy as np
import keyboard
#import simpleaudio
import msvcrt
import wave
import time
import glob
from psychopy import core
import multiprocessing
import random as rd
import time
from pydub import AudioSegment
from pydub.playback import play
import threading
from multiprocessing import Process
from playsound import playsound
from timeit import default_timer as timer
from datetime import timedelta, datetime

# for reaction time ##############################################################

def impressed(): # m pressed
    time_of_m_pressed = timer()
    print("m pressed")
    return time_of_m_pressed, "m"

def unimpressed(): # q pressed
    time_of_q_pressed = timer()
    print("q pressed")
    return time_of_q_pressed, "q"

# demographics #######################################################################

subject_ID = str(input("Enter Subject ID: "))

subject_Age = str(input("Enter Subject Age: "))

#curr_date = datetime.datetime.today().strftime('%y%m%d')

# load audio files & RSVP#################################################################

all_files = glob.glob("./audiofiles/babble/*.wav")

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
numbers = ['2', '3', '4', '5', '6', '7', '8', '9']

# empty lists to load answers into
chosen_audio_files = []
keyboard_responses = []
rsvp_list = []
rsvp_response = []
#reaction_time = []

# define hot keys
keyboard.add_hotkey("m", lambda: impressed())
keyboard.add_hotkey("q", lambda: unimpressed())

for i in range(2): # set number of trials here

    selected_file = rd.choices(all_files, weights=(40,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4), k=1)
    chosen_audio_files.append(selected_file)
    print(all_files[0])
    print(selected_file[0])
    audio_ax = AudioSegment.from_wav(selected_file[0])

    # rsvp task ###############################################################################

    chosen_numbers = rd.choices(numbers, k = 2)
    chosen_letters = rd.choices(alphabet, k = 28)

    joinedlist = chosen_numbers + chosen_letters
    rd.shuffle(joinedlist)
    print(joinedlist)
    rsvp_list.append(chosen_numbers)

    # threading ##########################################################
    start = timer()

    def audio_ax_cpt():
        play(audio_ax)

    ax_response: str = ""

    def keyboard():
        #print("Does the audio match the target?")
        global ax_response
        ax_response = str(input("Does the audio match the target?"))
        return(ax_response)
    print(ax_response)
    keyboard_responses.append(ax_response)

    def rsvp():
        for x in joinedlist:
            print(x)
            time.sleep(0.083) # seconds in between the letters

    audio_thread = threading.Thread(name='audio_ax_cpt', target=audio_ax_cpt) # thread for audio
    keyboard_thread = threading.Thread(target=keyboard, args=()) # thread for audio-keyboard-response
    rsvp_thread = threading.Thread(name='rsvp', target=rsvp) # thread for visual rsvp

    audio_thread.start()
    keyboard_thread.start()
    rsvp_thread.start()

    audio_thread.join()
    keyboard_thread.join()
    rsvp_thread.join()

    # ask for rsvp input after threading finished ####################################################################
    rsvp_keyboard_response = str(input("Which numbers were there?"))
    rsvp_response.append(rsvp_keyboard_response)

# build output file ###############################################################################################
#name output file path
output_path = 'C:/Users/mirik/Documents/Science/'
save_name = subject_ID + '.csv'
save_file = output_path + save_name

trial_1_audio = chosen_audio_files[0]
trial_2_audio = chosen_audio_files[1]
trial_1_keyboard = keyboard_responses[0]
trial_2_keyboard = keyboard_responses[1]
trial_1_rsvp_list = rsvp_list[0]
trial_2_rsvp_list = rsvp_list[1]
trial_1_rsvp_response = rsvp_response[0]
print(trial_1_keyboard)
trial_2_rsvp_response = rsvp_response[1]
#trial_1_reaction_time = time_impressed[0]
#trial_2_reaction_time = time_impressed[1]

output_file = pd.DataFrame({'Subject_ID' : [subject_ID],
                            'Subject_Age' : [subject_Age],
                           # 'Date': [curr_date],
                            'Response1': [trial_1_keyboard],
                            'Response2': [trial_2_keyboard],
                            'Audio1': [trial_1_audio],
                            'Audio2': [trial_2_audio],
                            'rsvp1_list': [trial_1_rsvp_list],
                            'rsvp2_list': [trial_2_rsvp_list],
                            'rsvp1_response': [trial_1_rsvp_response],
                            'rsvp2_response': [trial_2_rsvp_response]
                            #'reaction_time_1': [trial_1_reaction_time],
                            #'reaction_time_2': [trial_2_reaction_time]

                            })
print(output_file)

# save out csv file
try:
    output_file.to_csv(save_file, index=False)
except:
    print("DEBUG: ERROR SAVING FILE. NOT COMPLETED")