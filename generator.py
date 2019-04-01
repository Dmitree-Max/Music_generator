import random
import melody


random.seed()


def generate(note_threads_number, accord_threads_number, length, tonality, positivity, tempo):
    """
    this function produces melody which contains set of melodies: common, and accord-melodies
    :param note_threads_number: (int)how many flows of common melodies do we want
    :param accord_threads_number: (int)how many flows of accord-melodies do we want
    :param length: (int)how many notes should be in the melody
    :param tonality: (list) it list of allowed sounds
    :param positivity: (int) 0 or 1 0-major, 1-minor
    :param tempo: (int) speed of melody, more tempo -> more speed
    :return: (list of Melody) all the melodies which music contains
    """
    melody_sequence = list()
    patternise_number = 3
    main_melody = create_melody_core(tonality, positivity, length // 2 ** (patternise_number - tempo - 1) + 1, 2 ** (patternise_number - tempo))

    for _ in range(0, patternise_number):
        main_melody = double_notes(tonality, main_melody, positivity)

    # cut melody
    new_main_melody = melody.Melody(0)
    for time in main_melody.note_sequence:
        if time < length:
            new_main_melody.note_sequence[time] = main_melody.note_sequence[time]
    main_melody = new_main_melody

    melody_sequence.append(main_melody)
    accord_duration = 2
    note_duration = 1
    for _ in range(0, accord_threads_number):
        i = 0
        this_accord_melody = melody.Melody(1)
        while i * accord_duration < length:
            a = main_melody.note_sequence[i].sounds[0]
            current_cluster = get_cluster(tonality, accord_duration, 80, positivity, a)
            if type(current_cluster) == int:
                previous = this_accord_melody.last_cluster()
                if type(previous) != int:
                    previous.duration = previous.duration + accord_duration
            else:
                this_accord_melody.add_cluster(i * accord_duration, current_cluster)
            i += 1
        melody_sequence.append(this_accord_melody)

    for _ in range(0, note_threads_number):
        this_melody = generate_background_melody(tonality, positivity)
        i = 0
        while i < length:
            a = this_melody.note_sequence[i % 8].sounds[0]
            current_cluster = melody.Cluster(note_duration, 70)
            current_cluster.add_note(a)
            this_melody.add_cluster(i * note_duration, current_cluster)
            i += 1

        melody_sequence.append(this_melody)
    return melody_sequence


def generate_background_melody(tonality, positivity):
    """
    generates 8-note melody, with fourth note - dominanta, and the eight note - tonika and other notes from two accords
    :param tonality: (list of int) all allowed notes
    :param positivity: (0 or 1) 0 - minor, 1 - major
    :return: melody which contents 8 notes
    """
    this_melody = melody.Melody(0)

    sounds_list = []
    for _ in range(0, 2):
        accord = 0
        while type(accord) == int:
            first_step = random.randint(60, 71)
            while first_step % 12 not in tonality:
                first_step = random.randint(60, 71)
            accord = get_cluster(tonality, 1, 100, positivity, first_step)
        for i in range(0, 3):
            sounds_list.append(accord.sounds[i])

    random.shuffle(sounds_list)
    for i in range(0, 8):
        if i == 7:
            note = tonality[0] + 5 * 12
        elif i == 3:
            note = tonality[4] + 5 * 12
        else:
            note = sounds_list[0]
            sounds_list.pop(0)

        current_cluster = melody.Cluster(1, 100)
        current_cluster.add_note(note)
        this_melody.add_cluster(i, current_cluster)
    return this_melody


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


def get_next_note(tonality, positivity, previous_note):
    """
    returns note which is in pattern(next tonality note or next accord note) with previous note
    :param tonality: (list of int) all allowed notes
    :param positivity: (0 or 1) 0 - minor, 1 - major
    :param previous_note: (int) number of previous note in midi code
    :return: (int) number of note in midi code
    """
    chance = random.randint(0, 1)
    direction = random.randint(-1, 1)
    if chance == 0:
        return tonality[(tonality.index(previous_note % 12) + 1 * direction) % len(tonality)] + 60
    elif (previous_note + (3 + positivity) * direction) % 12 in tonality:
        return previous_note + (3 + positivity) * direction
    else:
        return tonality[(tonality.index(previous_note % 12) + 1 * direction) % len(tonality)] + 60


def create_melody_core(tonality, positivity, length, note_duration):
    """
    creates a melody with certain length using patterns
    :param tonality: (list of int) all allowed notes
    :param positivity: (0 or 1) 0 - minor, 1 - major
    :param length: (int) length of melody
    :param note_duration: (int) duration of all notes in melody
    :return: (Melody) created melody
    """
    this_melody = melody.Melody(0)
    previous_note = random.randint(60, 72)
    while previous_note % 12 not in tonality:
        previous_note = random.randint(60, 72)
    for i in range(0, length):
        current_cluster = melody.Cluster(note_duration, 100)
        current_cluster.add_note(previous_note)
        this_melody.add_cluster(i * note_duration, current_cluster)
        current_note = get_next_note(tonality, positivity, previous_note)
        previous_note = current_note

    return this_melody


def double_notes(tonality, current_melody, positivity):
    """
    change all notes in melody with pairs of notes with half duration and same time, records it in new melody
    :param tonality: (list of int) all allowed notes
    :param positivity: (0 or 1) 0 - minor, 1 - major
    :param current_melody: (Melody) melody we should rebuild
    :return: (Melody) new melody made on the base of current melody
    """
    new_melody = melody.Melody(0)
    for time in current_melody.note_sequence:
        cluster = current_melody.note_sequence[time]
        first_cluster = melody.Cluster(cluster.duration / 2, cluster.volume)
        second_cluster = melody.Cluster(cluster.duration / 2, cluster.volume)
        first_cluster.add_note(cluster.sounds[0])
        second_cluster.add_note(get_next_note(tonality, positivity, cluster.sounds[0]))
        new_melody.note_sequence[time] = first_cluster
        new_melody.note_sequence[time + cluster.duration / 2] = second_cluster
    return new_melody
