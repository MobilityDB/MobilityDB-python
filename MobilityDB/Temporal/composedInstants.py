class COMPOSEDTEMPORALINST:

    __slots__ = ['instants']
    MAINCLASS = None

    def __init__(self, instantsList=None):
        self.instants = instantsList

    def __getitem__(self, item):
        return self.instants[item]

    def startInstant(self):
        return self.instants[0]

    def endInstant(self):
        return self.instants[len(self.instants) - 1]

    def numInstants(self):
        return len(self.instants)

    def getinstants(self):
        return ', '.join('{}'.format(inst.value.__str__() + "@" + inst.time.__str__()) for inst in self.instants)
