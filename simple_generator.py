
from midiutil.MidiFile import MIDIFile
import random


# choose working mode
try:
    mode = input("""Press 
P - play 
S - safe 
B - both
""")

except EOFError:
    print ("Обработали исключение EOFError")


# 1 here is number of tracks
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero
# Times are measured in beats
track = 0
time = 0

MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 120)
random.seed()
binfile = open("out.mid", 'wb')


def make_music_rand():
    seq = []
    seq_ac = []
    i = 0
    while i < 99:
        a = random.randint(1, 7)
        seq.append(a)
        i = i + 1

    i = 0
    while i < 99:
        a = random.randint(1, 7)
        seq_ac.append(a)
        i = i + 3
    write_sequence_ac(seq_ac)
    return seq


# now we expect list here
def write_sequence(args):
    order = 0
    for arg in args:
        write_note(switch(arg), order, 100)
        order = order + 1


# now we expect list here
def write_sequence_ac(args):
    order = 0
    for arg in args:
        write_accord(switch(arg), order)
        print(switch(arg))
        order = order + 3


# it returns number of note in MIDI designations
# https://newt.phys.unsw.edu.au/jw/notes.html        it is link to the description of designations
def switch(x):
    return {
        1: 60,
        2: 62,
        3: 64,
        4: 65,
        5: 67,
        6: 69,
        7: 71,
        8: 'A',
        9: 'B',
        10: 'C',
        11: 'D',
        12: 'E',
        13: 'F',
        14: 'G'
    }.get(x, 0)


# it is happy accord in do-major
def write_accord(first_step, order):
    if (first_step == 0):
        return

    track = 0
    channel = 0
    time = order
    duration = 1
    MyMIDI.addNote(track, channel, first_step, time, duration, 70)
    MyMIDI.addNote(track, channel, first_step, time+1, duration, 60)
    MyMIDI.addNote(track, channel, first_step, time+2, duration, 50)

    MyMIDI.addNote(track, channel, first_step+4, time, duration, 70)
    MyMIDI.addNote(track, channel, first_step+4, time+1, duration, 60)
    MyMIDI.addNote(track, channel, first_step+4, time+2, duration, 50)

    MyMIDI.addNote(track, channel, first_step+7, time, duration, 70)
    MyMIDI.addNote(track, channel, first_step+7, time+1, duration, 60)
    MyMIDI.addNote(track, channel, first_step+7, time+2, duration, 50)


# if the value is zero it will be second without volume
def write_note(value, order, volume):
        if(value == 0):
            return
        if(type(value) == type('A')):
            write_accord(value, order)
            return
        track = 0
        channel = 0
        time = order
        duration = 1
        MyMIDI.addNote(track, channel, value, time, duration, volume)


write_sequence(make_music_rand())
MyMIDI.writeFile(binfile)
binfile.close()
