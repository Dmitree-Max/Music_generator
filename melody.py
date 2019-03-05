class Melody(object):
    def __init__(self, melody_type):
        """
        constructor, note_seq initialized like an empty list
        melody_type(int): type of our melody,where 0 is common, 1 is accord
        :return: 
        """
        self.melody_type = melody_type
        self.note_sequence = list()

    def add_note(self, note):
        """
        This functions add note into list: note sequence
        :param note: (int) number of note in human numeration
        :return: none
        """
        self.note_sequence.append(note)

