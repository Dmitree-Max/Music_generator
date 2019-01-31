
from midiutil.MidiFile import MIDIFile
import random
import sys
import pygame


# we expect input mode

# work with input arguments
arr = sys.argv[:]
if len(arr) > 1:
    file = arr[1]
else:
    file = "out.mid"


# choose working mode
try:
    mode = input("""Press 
P - play 
S - safe 
B - both
""")

except EOFError:
    print("Обработали исключение EOFError")


# 1 here is number of tracks
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero
# Times are measured in beats
track = 0
time = 0

MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 120)
random.seed()
binfile = open(file, 'wb')


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
    print("writing sequence")
    order = 0
    for arg in args:
        write_note(switch(arg), order, 100)
        order = order + 1


# now we expect list here
def write_sequence_ac(args):
    order = 0
    for arg in args:
        write_accord(switch(arg), order)
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
    if first_step == 0:
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
        if value == 0:
            return
        if isinstance(value, str):
            write_accord(value, order)
            return
        track = 0
        channel = 0
        time = order
        duration = 1
        MyMIDI.addNote(track, channel, value, time, duration, volume)


def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


def ful_music_play(music_file):
    print("playing music")
    # pick a midi music file you have ...
    # (if not in working folder use full path)
    freq = 10100  # audio CD quality
    # So, here was 44100 but it gain very strange messages, but music was in better quality
    # ALSA lib pcm.c:7963:(snd_pcm_recover) under run occurred
    bitsize = -16  # unsigned 16 bit
    channels = 2  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)
    try:
        play_music(music_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit


if mode == 's' or mode == 'S':
    write_sequence(make_music_rand())
    MyMIDI.writeFile(binfile)
    binfile.close()
elif mode == 'b' or mode == 'B':
    write_sequence(make_music_rand())
    MyMIDI.writeFile(binfile)
    binfile.close()
    ful_music_play(file)
elif mode == 'p' or mode == 'P':
    print("play without saving")

else:
    print("incorrect mode")

