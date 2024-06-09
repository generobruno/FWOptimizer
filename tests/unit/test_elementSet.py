"""_summary_
"""

from fwoptimizer.utils.elementSet import *


def test_registry():
    """_summary_
    """

    expectedRegistred = ['ElementSet', 'DirSet', 'ProtSet']
    
    for i in expectedRegistred:

        assert i in ElementSetRegistry.getRegistry()


def test_createElementSet():
    """
    sumary
    """

    dir = ElementSet.createElementSet('DirSet', ['0.0.10.0/24'])
    prot = ElementSet.createElementSet('ProtSet', ['TCP'])

    assert isinstance(dir, DirSet)
    assert isinstance(prot, ProtSet)

    dcomp1 = DirSet(['0.0.10.0/24'])
    dcomp2 = DirSet(['0.0.11.0/24'])

    assert dir == dcomp1
    assert dir != dcomp2

    pcomp1 = ProtSet(['TCP'])
    pcomp2 = ProtSet(['UDP'])

    assert prot == pcomp1
    assert prot != pcomp2

    

    