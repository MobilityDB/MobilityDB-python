class TEMPORALS:
    __slots__ = ['sequences']
    Duration = 4

    def __init__(self, sequencesList=None):
        if isinstance(sequencesList, list):
            self.sequences = sequencesList.copy()

    def getSequences(self):
        if isinstance(self.sequences, list) and len(self.sequences) > 0:
            return ', '.join('[{}]'.format(seq.getInstants()) for seq in self.sequences)
        else:
            return []

    def numSequences(self):
        return len(self.sequences)

    def __str__(self):
        return "{}{{{}}}".format("", self.getSequences())
