class TEMPORALS:
    __slots__ = ['sequences']

    def __init__(self, sequencesList=None):
        self.sequences = sequencesList

    def getSequences(self):
        return ', '.join('[{}]'.format(seq.getInstants()) for seq in self.sequences)

    def numSequences(self):
        return len(self.sequences)

    def __str__(self):
        return "{}{{{}}}".format("", self.getSequences())
