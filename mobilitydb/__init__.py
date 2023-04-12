from .boxes import *
from .main import *
from .temporal import *
from .time import *

__all__ = [
    # boxes
    'TBox', 'STBox',
    # main
    'TBool', 'TBoolInst', 'TBoolInstSet', 'TBoolSeq', 'TBoolSeqSet',
    'TInt', 'TIntInst', 'TIntInstSet', 'TIntSeq', 'TIntSeqSet',
    'TFloat', 'TFloatInst', 'TFloatInstSet', 'TFloatSeq', 'TFloatSeqSet',
    'TText', 'TTextInst', 'TTextInstSet', 'TTextSeq', 'TTextSeqSet',
    'TPointInst', 'TPointInstSet', 'TPointSeq', 'TPointSeqSet',
    'TGeomPoint', 'TGeomPointInst', 'TGeomPointInstSet', 'TGeomPointSeq', 'TGeomPointSeqSet',
    'TGeogPoint', 'TGeogPointInst', 'TGeogPointInstSet', 'TGeogPointSeq', 'TGeogPointSeqSet',
    # temporal
    'Temporal', 'TInstant', 'TemporalInstants', 'TInstantSet', 'TSequence', 'TSequenceSet',
    # time
    'Period', 'TimestampSet', 'PeriodSet'
]

from warnings import warn

warn('The python-mobilitydb package is now deprecated and will no longer be mantained.'
     'Instead, the use of the new PyMEOS package is recommended. Check it out at https://pypi.org/project/pymeos/',
     DeprecationWarning, stacklevel=2)
