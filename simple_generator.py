
from midiutil.MidiFile import MIDIFile
import random
import pygame
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="out.mid")
options, remainder = parser.parse_args()
file = options.filename


# choose working mode
try:
    mode = input("""
Press 
P - play 
S - safe 
B - both
""")

except EOFError:
    print("Обработали исключение EOFError")
    raise SystemExit


# 1 here is number of tracks
MyMIDI = MIDIFile(1)

# Tracks are numbered from zero
# Times are measured in beats
track = 0
time = 0

MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 120)
random.seed()


# returns list of lists, which are melodies
def make_music_rand():
    seq_seq = []
    seq = [0]
    seq_ac = [1]
    seq_ac2 = [1]
    i = 0
    while i < 21:
        a = random.randint(1, 7)
        seq.append(a)
        i = i + 1

    i = 0
    while i < 21:
        a = random.randint(1, 7)
        seq_ac.append(a)
        i = i + 3

    i = 0
    while i < 21:
        a = random.randint(1, 7)
        seq_ac2.append(a)
        i = i + 3

    seq_seq.append(seq)
    seq_seq.append(seq_ac)
    seq_seq.append(seq_ac2)
    return seq_seq


# we expect list here
def write_sequence(melody):
    print("writing sequence")
    order = 0
    for note_pos in range(1, len(melody)):
        write_note(0, 0, switch(melody[note_pos]), order, 1, 100)
        order = order + 1


# we expect list here
def write_sequence_ac(melody):
    order = 0
    for note_pos in range(1, len(melody)):
        write_accord(0, 0, switch(melody[note_pos]), order, 1, 70)
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
def write_accord(track_name, channel, first_step, order, duration, volume):
    if first_step == 0:
        return

    MyMIDI.addNote(track_name, channel, first_step, order, duration, volume)
    MyMIDI.addNote(track_name, channel, first_step, order+1, duration, volume - 20)
    MyMIDI.addNote(track_name, channel, first_step, order+2, duration, volume - 40)

    MyMIDI.addNote(track_name, channel, first_step+4, order, duration, volume)
    MyMIDI.addNote(track_name, channel, first_step+4, order+1, duration, volume - 20)
    MyMIDI.addNote(track_name, channel, first_step+4, order+2, duration, volume - 40)

    MyMIDI.addNote(track_name, channel, first_step+7, order, duration, volume)
    MyMIDI.addNote(track_name, channel, first_step+7, order+1, duration, volume - 20)
    MyMIDI.addNote(track_name, channel, first_step+7, order+2, duration, volume - 40)


# if the value is zero we write one beat of pause in melody
def write_note(track_name, channel, value, time_n, duration, volume):
        if value == 0:
            return
        if isinstance(value, str):
            write_accord(value, time)
            return

        MyMIDI.addNote(track_name, channel, value, time_n, duration, volume)


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
    channels = 1  # 1 is mono, 2 is stereo
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


def write_full(fl_melody):
    for seq in fl_melody:
        if seq[0] == 0:
            write_sequence(seq)
        if seq[0] == 1:
            write_sequence_ac(seq)


full_melody = make_music_rand()
if mode == 'p' or mode == 'P':
    print("play without saving")
elif mode == 's' or mode == 'S':
    with open(file, "wb") as binfile:
        write_full(full_melody)
        MyMIDI.writeFile(binfile)
elif mode == 'b' or mode == 'B':
    with open(file, "wb") as binfile:
        write_full(full_melody)
        MyMIDI.writeFile(binfile)
        binfile.close()
        ful_music_play(file)

else:
        print("incorrect mode")

