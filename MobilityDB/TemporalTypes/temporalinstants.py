from .temporal import TEMPORAL


class TEMPORALINSTANTS:
    __slots__ = ['value']

    def __init__(self, instantsList=None):
        self.value = instantsList

    def __getitem__(self, item):
        return self.value[item]

    def numInstants(self):
        return len(self.value)

    def startInstant(self):
        return self.value[0]

    def endInstant(self):
        return self.value[len(self.value) - 1]

    def getInstants(self):
        return ', '.join('{}'.format(inst.value.__str__() + "@" + inst.time.__str__()) for inst in self.value)
