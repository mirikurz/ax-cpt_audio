# import packages #########################################################################################

import sys
import pyaudio
import datetime
import pandas as pd
import numpy as np
import keyboard as kb
#import simpleaudio
import msvcrt
import wave
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
from pynput import keyboard

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
self_keys = []
rsvp_list = []
rsvp_response = []
reaction_time = []
audio_started = False
key_pressed = False

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

    def audio_ax_cpt(): # audio
        play(audio_ax)

    def on_press(key): # keyboard response to audio
        if key == keyboard.Key.esc:
            return False
        try:
            k = key.char
        except:
            k = key.name
        if k in ['m', 'q']:  # keys of interest
            self_keys.append(k)
            print('Key pressed:' + k)
            return False

    def rsvp(): # visual task
        for x in joinedlist:
            print(x)
            time.sleep(0.083) # seconds in between the letters

    audio_thread = threading.Thread(name='audio_ax_cpt', target=audio_ax_cpt) # thread for audio
    listener = keyboard.Listener(on_press=on_press) #  thread for audio-keyboard-response
    rsvp_thread = threading.Thread(name='rsvp', target=rsvp) # thread for visual rsvp

    audio_thread.start()
    audio_started = True
    listener.start()
    if kb.is_pressed('q') or kb.is_pressed('m'):
        key_pressed = True
    rsvp_thread.start()

    # reaction time ######################################################################################

    start_time = 0
    key_time = 0

    if audio_started == True:
        start_time = time.time()
        audio_started = False

    if key_pressed == True:
        key_time = time.time()
        key_pressed = False

    r_t = key_time - start_time
    reaction_time.append(r_t)

    # finish threads ####################################################################################
    audio_thread.join()
    listener.join
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
trial_1_keyboard = self_keys[0]
trial_2_keyboard = self_keys[1]
trial_1_rsvp_list = rsvp_list[0]
trial_2_rsvp_list = rsvp_list[1]
trial_1_rsvp_response = rsvp_response[0]
trial_2_rsvp_response = rsvp_response[1]
trial_1_reaction_time = reaction_time[0]
trial_2_reaction_time = reaction_time[1]

output_file = pd.DataFrame({'Subject_ID' : [subject_ID],
                            'Subject_Age' : [subject_Age],
                            'Response1': [trial_1_keyboard],
                            'Response2': [trial_2_keyboard],
                            'Audio1': [trial_1_audio],
                            'Audio2': [trial_2_audio],
                            'rsvp1_list': [trial_1_rsvp_list],
                            'rsvp2_list': [trial_2_rsvp_list],
                            'rsvp1_response': [trial_1_rsvp_response],
                            'rsvp2_response': [trial_2_rsvp_response],
                            'RT1': [trial_1_reaction_time],
                            'RT2': [trial_2_reaction_time]

                            })
print(output_file)

# save out csv file
try:
    output_file.to_csv(save_file, index=False)
except:
    print("DEBUG: ERROR SAVING FILE. NOT COMPLETED")
