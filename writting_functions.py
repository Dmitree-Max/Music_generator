def write_music(full_melody, midi_file, channel):
    """
    this function takes all melody flows and writes them into file one after another
    if first number is 0 -> it is common melody, 1 -> accord-melody
    :param full_melody: (list of melodies) all flows of melodies that should be written in midi_file
    :param midi_file: (midi file) which should be initialized and open
    :return: none
    """
    track_name = 0
    for melody in full_melody:
        keys_list = list(melody.note_sequence.keys())
        keys_list.sort()
        for time in keys_list:
            write_cluster(track_name, channel, melody.note_sequence[time], midi_file, time)
        track_name += 1


def write_melody_common(_melody, midi_file):
    """
    writes down a common melody in midi file
    :param _melody: (list of int): it should be list of integer in certain interval
    :param midi_file: (midi file) which should be initialized and open
    :return: none
    """
    print("writing sequence")
    for order, note in enumerate(_melody.note_sequence):
        write_note(0, 0, switch(note), order, 1, 100, midi_file)


def write_melody_accord(_melody, midi_file):
    """
    writes down an accord melody in midi file
    :param _melody: (list of int): it should be list of integer in certain interval
    :param midi_file: (midi file) which should be initialized and open
    :return: none
    """
    print("writing sequence ac")
    for order, note in enumerate(_melody.note_sequence):
        write_accord(0, 0, switch(note), 3*order, 1, 70, midi_file)


# it returns number of note in MIDI designations
# https://newt.phys.unsw.edu.au/jw/notes.html        it is link to the description of designations
def switch(x):
    """
    just convert from human numeration into MIDI numeration
    :param x: (int)serial number of the note
    :return: (int)number of mote in midi cod
    """
    return {
        1: 60,
        2: 62,
        3: 64,
        4: 65,
        5: 67,
        6: 69,
        7: 71,
        8: 73,
        9: 75,
        10: 'C',
        11: 'D',
        12: 'E',
        13: 'F',
        14: 'G'
    }.get(x, 0)


# if the value is zero we write one beat of pause in melody
def write_note(track_name, channel, value, time_n, duration, volume, midi_file):
        midi_file.addNote(track_name, channel, value, time_n, duration, volume)


# it is happy accord in do-major
def write_accord(track_name, channel, first_step, order, duration, volume, midi_file):
    """
    this function writes an accord with the rule:
    accord takes 3 slots in a row, volume is decreasing
    :param track_name: (string) track name
    :param channel: (int) number of channel
    :param first_step: (int) first note of the accord in human format
    :param order: (int) position accord should be wrote from
    :param duration: (int) duration of every sound in beats
    :param volume: (int) volume of the first note(100 is normal)
    :param midi_file: (midi file) which should be initialized and open
    :return: none
    """
    if first_step == 0:
        return

    midi_file.addNote(track_name, channel, first_step, order, duration, volume)
    midi_file.addNote(track_name, channel, first_step, order+1, duration, volume - 20)
    midi_file.addNote(track_name, channel, first_step, order+2, duration, volume - 40)

    midi_file.addNote(track_name, channel, first_step+4, order, duration, volume)
    midi_file.addNote(track_name, channel, first_step+4, order+1, duration, volume - 20)
    midi_file.addNote(track_name, channel, first_step+4, order+2, duration, volume - 40)

    midi_file.addNote(track_name, channel, first_step+7, order, duration, volume)
    midi_file.addNote(track_name, channel, first_step+7, order+1, duration, volume - 20)
    midi_file.addNote(track_name, channel, first_step+7, order+2, duration, volume - 40)


def write_cluster(track_name, channel, cluster, mide_file, time):
    """

    :param track_name:
    :param channel:
    :param cluster:
    :param mide_file:
    :param time:
    :return:
    """
    for note in cluster.sounds:
        mide_file.addNote(track_name, channel, note, time, cluster.duration, cluster.volume)


