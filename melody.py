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
        self._duration = duration
        self._volume = volume
        self._sounds = list()

    duration = property()
    volume = property()
    sounds = property()

    @duration.getter
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    def count(self):
        return self._sounds.len()

    @volume.getter
    def volume(self):
        return self._volume

    @sounds.getter
    def sounds(self):
        return self._sounds

    @sounds.setter
    def sounds(self, value):
        self._sounds = value

    def add_note(self, note):
        """
        This functions add note into list: sounds
        :param note: (int) number of note in midi numeration
        :return: none
        """
        self.sounds.append(note)

    def write(self):
        print(self.sounds, self.duration, self._volume)


def merge(main_cluster, second_cluster):
    """
    This function merges two clusters into one, using volume and duration from main cluster. It is recommended to
    use this function with clusters of same duration
    :param main_cluster: (Cluster) Volume and duration are taken from here
    :param second_cluster: (Cluster) Notes from this cluster go into union
    :return: (Cluster) contents sounds from both clusters, but volume and duration from first
    """
    union = Cluster(Cluster.main_cluster.duration, Cluster.get_volume(main_cluster))
    union.set_sounds(Cluster.main_cluster.sounds, Cluster.second_cluster.sounds)
    return union


def print_music(music):
    for melody in music:
        melody.print_melody()
