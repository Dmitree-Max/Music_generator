import random
import melody


random.seed()


def generate(note_threads_number, accord_threads_number, length):
    """
    this function produces melody which contains set of melodies: common, and accord-melodies
    :param note_threads_number: (int)how many flows of common melodies do we want
    :param accord_threads_number: (int)how many flows of accord-melodies do we want
    :param length: (int)how many notes should be in the melody
    :return: (list of Melody) all the melodies which music contains
    """
    seq_seq = list()

    for _ in range(0, note_threads_number):
        i = 0
        this_melody = melody.Melody(0)
        while i < length:
            a = random.randint(1, 7)
            this_melody.add_note(a)
            i = i + 1
        seq_seq.append(this_melody)

    for _ in range(0, accord_threads_number):
        i = 0
        this_accord_melody = melody.Melody(1)
        while i < length:
            a = random.randint(1, 7)
            this_accord_melody.add_note(a)
            i = i + 3
        seq_seq.append(this_accord_melody)

    return seq_seq
