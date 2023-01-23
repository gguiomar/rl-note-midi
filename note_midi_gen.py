#%%

import numpy as np
import random
import mido
import time


def generate_note_matrix(bpm, rows, columns, n_channels):
    note_matrix = np.zeros((rows, columns, 3), dtype = 'int') # create a 3D matrix with 4 rows, 16 columns, and 3 channels
    pitch_channel = np.random.randint(0, 127, (rows, columns)) # generate random pitch values
    duration_channel = np.full((rows, columns), 60/bpm) # generate duration values based on the tempo
    channel_selector = np.random.randint(0,n_channels,(rows, columns))
    note_matrix[:, :, 0] = pitch_channel # assign pitch values to the first channel
    note_matrix[:, :, 1] = duration_channel # assign duration values to the second channel
    note_matrix[:, :, 2] = channel_selector # channel out
    return note_matrix


def send_note_matrix(note_matrix):
    outport = mido.open_output(name = 'MIDO_OUT', virtual=True)
    for row in note_matrix:
        for note in row:
            msg1 = mido.Message('note_on', channel = note[2], note=note[0], velocity=64)
            msg2 = mido.Message('note_off', channel = note[2], note=note[0], velocity=0)
            outport.send(msg1)
            time.sleep(0.1)
            outport.send(msg2)            

#%%

note_matrix = generate_note_matrix(120, 4, 40, 6)
send_note_matrix(note_matrix)

