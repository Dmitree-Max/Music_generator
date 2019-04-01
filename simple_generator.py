from midiutil.MidiFile import MIDIFile
from optparse import OptionParser
import io

import generator
import writting_functions
import interface
import player
import melody


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="out.mid")
options, remainder = parser.parse_args()
file = options.filename


mode = interface.choose_working_mode()
melody_length = interface.correct_int_input("number of notes:")
common_threads_number = interface.correct_int_input("note flows:")
accord_thread_number = interface.correct_int_input("accord flows:")

# argument here is number of tracks
MyMIDI = MIDIFile(common_threads_number + accord_thread_number + 1)
for i in range(0, common_threads_number + accord_thread_number):
    MyMIDI.addTrackName(i, 0, "Sample Track")
    MyMIDI.addTempo(i, 0, 120)


do_major = [0, 2, 4, 5, 7, 9, 11]
sol_minor = [7, 9, 10, 0, 2, 3, 5]

full_melody = generator.generate(common_threads_number, accord_thread_number, melody_length, do_major, positivity=1, tempo=1)
# full_melody = generator.create_melody_core(do_major, 1, melody_length, 2)
melody.print_music(full_melody)


temp = io.BytesIO()
writting_functions.write_music(full_melody, MyMIDI, 0)
temp.seek(0)
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

