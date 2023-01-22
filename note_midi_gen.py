import numpy as np
import random

def generate_notes(bpm):
    note_matrix = np.zeros((4, 16, 2)) # create a 3D matrix with 4 rows, 16 columns, and 2 channels
    pitch_channel = np.random.randint(0, 127, (4, 16)) # generate random pitch values
    duration_channel = np.full((4, 16), 60/bpm) # generate duration values based on the tempo
    note_matrix[:, :, 0] = pitch_channel # assign pitch values to the first channel
    note_matrix[:, :, 1] = duration_channel # assign duration values to the second channel
    return note_matrix

def send_notes(note_matrix):
    import time
    import rtmidi
    # Create a new MIDI output
    midiout = rtmidi.MidiOut()

    # List available ports
    ports = midiout.get_ports()

    # Open the first available port
    if ports:
        midiout.open_port(0)
    else:
        midiout.open_virtual_port("My virtual output")

    # Send notes
    for track in range(4):
        for i in range(16):
            pitch = note_matrix[track,i,0]
            duration = note_matrix[track,i,1]
            velocity = random.randint(0,127)
            note_on = [0x90 + track, pitch, velocity] # note on message
            note_off = [0x80 + track, pitch, 0] # note off message
            midiout.send_message(note_on)
            time.sleep(duration)
            midiout.send_message(note_off)

    # Close the MIDI port
    del midiout

bpm = 120 # adjust this to your desired tempo
note_matrix = generate_notes(bpm)
send_notes(note_matrix)
