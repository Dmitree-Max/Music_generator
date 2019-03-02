from midiutil.MidiFile import MIDIFile
from optparse import OptionParser
import io

import generator
import writting_functions
import interface
import player


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="out.mid")
options, remainder = parser.parse_args()
file = options.filename


# 1 here is number of tracks
MyMIDI = MIDIFile(1)
# Tracks are numbered from zero
# Times are measured in beats
track = 0
time = 0
MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 120)


mode = interface.choose_working_mode()
melody_length = interface.correct_int_input("number of notes:")
common_threads_number = interface.correct_int_input("note flows:")
accord_thread_number = interface.correct_int_input("accord flows:")
full_melody = generator.generate(common_threads_number, accord_thread_number, melody_length)

temp = io.BytesIO()
writting_functions.write_music(full_melody, MyMIDI)
MyMIDI.writeFile(temp)
temp.seek(0)

if mode == 'p' or mode == 'P':
    print("play without saving")
    player.play(temp)
elif mode == 's' or mode == 'S':
    with open(file, "wb") as binfile:
        binfile.write(temp.getvalue())
elif mode == 'b' or mode == 'B':
    with open(file, "wb") as binfile:
        player.play(temp)
        temp.seek(0)
        binfile.write(temp.getvalue())
else:
        print("incorrect mode")

