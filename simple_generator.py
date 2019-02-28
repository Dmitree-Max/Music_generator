
from midiutil.MidiFile import MIDIFile
import random
import pygame.midi
import os
import time
import sys
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", default="out.mid")
options, remainder = parser.parse_args()
file = options.filename


start_time = time.time()

# choose working mode
i = 0
while i < 5:
    try:
        mode = input("""
    Press 
    P - play 
    S - safe 
    B - both
    """)
    except EOFError:
        if i < 4:
            print("EOFError")
            continue
        else:
            print("we ran into System crash")
            sys.exit(-1)
        break
    break
    i += 1


# system output
"""
pygame.midi.init()
print(pygame.midi.get_default_output_id())
print("AAA")
print(pygame.midi.get_device_info(-1))
print(pygame.midi.get_count())
"""

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
def make_music_rand(note_threads_number, accord_threads_number, length):
    """
    this function produces melody which contains set of melodies: common, and accord-melodies
    first argument: how many flows of common melodies do we want
    second argument: how many flows of accord-melodies do we want
    third argument: how many notes should be in the melody
    :return:
    list of list, so in fact it returns list of sequences, each of them has first element 0, if these are notes,
     and 1 if accords!
    """
    seq_seq = []

    j = 0
    while j < note_threads_number:
        i = 0
        seq = [0]
        while i < length:
            a = random.randint(1, 7)
            seq.append(a)
            i = i + 1
        j += 1
        seq_seq.append(seq)

    j = 0
    while j < accord_threads_number:
        i = 0
        seq_ac = [1]
        while i < length:
            a = random.randint(1, 7)
            seq_ac.append(a)
            i = i + 3
        j += 1
        seq_seq.append(seq_ac)

    print(seq_seq)
    return seq_seq


# we expect list here
def write_sequence(melody):
    """
    writes down a common -melody in my_midi file
    """
    print("writing sequence")
    order = 0
    for note_pos in range(1, len(melody)):
        write_note(0, 0, switch(melody[note_pos]), order, 1, 100)
        order = order + 1


# we expect list here
def write_sequence_ac(melody):
    """
    writes down a accord-melody in my_midi file
    """
    print("writing sequence ac")
    order = 0
    for note_pos in range(1, len(melody)):
        write_accord(0, 0, switch(melody[note_pos]), order, 1, 70)
        order = order + 3


# it returns number of note in MIDI designations
# https://newt.phys.unsw.edu.au/jw/notes.html        it is link to the description of designations
def switch(x):
    """
    just convert from human numeration into MIDI numeration
    :param x: serial number of the note
    :return: number of mote in midi cod
    """
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
    """
    this function writes an accord with the rule:
    accord takes 3 slots in a row, volume is decreasing

    """
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
    freq = 40100  # audio CD quality
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
    """
    this function takes all melody flows and writes them into file one after another
    if first number is 0 -> it is common melody, 1 -> accord-melody
    :param fl_melody: list of melodies
    :return: none
    """
    for seq in fl_melody:
        if seq[0] == 0:
            write_sequence(seq)
        if seq[0] == 1:
            write_sequence_ac(seq)


melody_length = 0
while True:
    melody_length_input = input("number of notes:")
    if str.isnumeric(melody_length_input):
        melody_length = int(melody_length_input)
        break
    else:
        print("please write a number")


full_melody = make_music_rand(1, 2, melody_length)
if mode == 'p' or mode == 'P':
    print("play without saving")
    file_mode = os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
    temp = os.open("Tempo.mid", file_mode)
    os.close(temp)
    with open("Tempo.mid", "wb") as temp2:
        write_full(full_melody)
        MyMIDI.writeFile(temp2)
        temp2.close()
        ful_music_play("Tempo.mid")
        os.remove("Tempo.mid")
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

