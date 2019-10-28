from bdateutil.parser import parse
from postgis import Point
from .temporal import TEMPORAL


class TEMPORALINST(TEMPORAL):
    __slots__ = ['value', 'time']
    Duration = 1

    def __init__(self, value=None, time=None):
        self.value = value
        self.time = time

    def __str__(self):
        return "'{}{}'".format(self.value.__str__() + "@", self.time.__str__())
