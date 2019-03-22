import random
import melody


random.seed()


def generate(note_threads_number, accord_threads_number, length, tonality, positivity):
    """
    this function produces melody which contains set of melodies: common, and accord-melodies
    :param note_threads_number: (int)how many flows of common melodies do we want
    :param accord_threads_number: (int)how many flows of accord-melodies do we want
    :param length: (int)how many notes should be in the melody
    :param tonality: (list) it list of allowed sounds
    :param positivity: (int) 0 or 1 0-major, 1-minor
    :return: (list of Melody) all the melodies which music contains
    """
    seq_seq = list()

    for _ in range(0, accord_threads_number):
        i = 0
        this_accord_melody = melody.Melody(1)
        while i < length:
            a = random.randint(40, 70)
            current_cluster = get_cluster(tonality, 1, 100, positivity, a)
            if type(current_cluster) == int:
                previous = this_accord_melody.last_cluster()
                if type(previous) != int:
                    previous.set_duration(previous.get_duration() + 1)
            else:
                this_accord_melody.add_cluster(i, current_cluster)
            i = i + 1
        seq_seq.append(this_accord_melody)

    for _ in range(0, note_threads_number):
        i = 0
        this_melody = melody.Melody(0)
        while i < length:
            a = random.randint(30, 70)
            while a % 12 not in tonality:
                a = random.randint(30, 70)
            current_cluster = melody.Cluster(1, 100)
            current_cluster.add_note(a)
            this_melody.add_cluster(i, current_cluster)
            i = i + 1

        seq_seq.append(this_melody)
    return seq_seq


def use_patterns(input_melody):
    new_melody = melody.Melody(0)
    for note in input_melody.note_sequence:
        i = random.randint(0, 2)
        #new_melody.add_note(note)
        #new_melody.add_note(note+i)
    return new_melody


def get_cluster(tonality, duration, volume, positivity, main_note):
    """
    Makes cluster if it is possible or return 0
    :param tonality: (list of int) all notes we can use
    :param duration: (float) duration of accord
    :param volume: (int) volume of accord
    :param positivity: (int) 1 or 0 major or minor
    :param main_note: (int) note from which accord should start in midi codes
    :return: (Cluster) returns 0 if there is no such cluster in this tonality
    """
    output_cluster = melody.Cluster(duration, volume)
    if main_note % 12 in tonality and (main_note + 3 + positivity) % 12 in tonality \
            and (main_note + 7) % 12 in tonality:
        output_cluster.add_note(main_note)
        output_cluster.add_note(main_note + 3 + positivity)
        output_cluster.add_note(main_note + 7)

        return output_cluster

    return 0

