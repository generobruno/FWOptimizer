"""_summary_
"""

from fwoptimizer.utils.elementSet import ElementSetRegistry, ElementSet, DirSet, ProtSet


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

    direction = ElementSet.createElementSet('DirSet', ['0.0.10.0/24'])
    protocol = ElementSet.createElementSet('ProtSet', ['TCP'])

    assert isinstance(direction, DirSet)
    assert isinstance(protocol, ProtSet)

    dcomp1 = DirSet(['0.0.10.0/24'])
    dcomp2 = DirSet(['0.0.11.0/24'])

    assert direction == dcomp1
    assert direction != dcomp2

    pcomp1 = ProtSet(['TCP'])
    pcomp2 = ProtSet(['UDP'])

    assert protocol == pcomp1
    assert protocol != pcomp2

