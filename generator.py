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
    seq_seq = []

    j = 0
    while j < note_threads_number:
        i = 0
        this_mel = melody.Melody(0)
        while i < length:
            a = random.randint(1, 7)
            this_mel.note_seq.append(a)
            i = i + 1
        j += 1
        seq_seq.append(this_mel)

    j = 0
    while j < accord_threads_number:
        i = 0
        this_ac_mel = melody.Melody(1)
        while i < length:
            a = random.randint(1, 7)
            this_ac_mel.note_seq.append(a)
            i = i + 3
        j += 1
        seq_seq.append(this_ac_mel)

    return seq_seq
