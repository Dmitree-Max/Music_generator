class Melody(object):
    def __init__(self, melody_type):
        """
        constructor, note_seq initialized like an empty list
        melody_type(int): type of our melody,where 0 is common, 1 is accord
        :return: 
        """
        self.melody_type = melody_type
        self.note_sequence = dict()

    def add_cluster(self, time, cluster):
        """
        This functions add note into list: note sequence
        :param cluster: (int) number of note in human numeration
        :return: none
        """
        self.note_sequence[time] = cluster

    def last_cluster(self):
        if self.note_sequence:
            all_keys = list(self.note_sequence.keys())
            max_key = max(all_keys)
            return self.note_sequence[max_key]
        return 0

    def print_melody(self):
        list_keys = list(self.note_sequence.keys())
        list_keys.sort()
        for time in list_keys:
            print(time)
            self.note_sequence[time].write()


class Cluster(object):
    def __init__(self, duration, volume):
        """
        constructor, note_seq initialized like an empty list
        melody_type(int): type of our melody,where 0 is common, 1 is accord
        :return:
        """
        self.duration = duration
        self.volume = volume
        self.sounds = list()

    def count(self):
        return self.sounds.len()

    def get_duration(self):
        return self.duration

    def set_duration(self, duration):
        self.duration = duration

    def get_volume(self):
        return self.volume

    def set_sounds(self, sounds_list):
        self.sounds = sounds_list

    def get_sounds(self):
        return self.sounds

    def add_note(self, note):
        """
        This functions add note into list: sounds
        :param note: (int) number of note in midi numeration
        :return: none
        """
        self.sounds.append(note)

    def write(self):
        print(self.sounds, self.duration)


def merge(main_cluster, second_cluster):
    """
    This function merges two clusters into one, using volume and duration from main cluster. It is recommended to
    use this function with clusters of same duration
    :param main_cluster: (Cluster) Volume and duration are taken from here
    :param second_cluster: (Cluster) Notes from this cluster go into union
    :return: (Cluster) contents sounds from both clusters, but volume and duration from first
    """
    union = Cluster(Cluster.get_duration(main_cluster), Cluster.get_volume(main_cluster))
    union.set_sounds(Cluster.get_sounds(main_cluster), Cluster.get_sounds(second_cluster))
    return union


def print_music(music):
    for melody in music:
        melody.print_melody()
