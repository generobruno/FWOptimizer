"""
Tests for the Edge, Node, Level and FDD classes
"""

import fwoptimizer.core.fdd as fdd
from fwoptimizer.core.fdd import Field
from fwoptimizer.core.fields import DirectionSet


def test_edge():
    """_summary_
    """

    f1 = Field("IPSrc", "DirSet")

    lvl1 = fdd.Level(f1)
    lvl2 = fdd.Level(f1)

    n1 = fdd.Node(lvl1)
    n2 = fdd.Node(lvl2)

    e1 = fdd.Edge([1], n1, n2, DirectionSet(['0.0.10.0/24']))
    e2 = fdd.Edge([1], n1, n2, DirectionSet(['0.0.10.0/24']))
    e3 = fdd.Edge([1], n1, n2, DirectionSet(['0.0.11.0/24']))
    e4 = fdd.Edge([2], n1, n2, DirectionSet(['0.0.12.0/24']))
    e5 = e4.replicate()

    assert e1 == e2
    assert e1 != e3
    assert e1 != e4
    assert e4 == e5

    assert e1 not in n1.getOutgoing()
    assert e1 not in n2.getIncoming()

    e1.autoConnect()

    assert e1 not in n2.getOutgoing()
    assert e1 not in n1.getIncoming()
    assert e1 in n1.getOutgoing()
    assert e1 in n2.getIncoming()

    e1.autoDisconnect()

    assert e1 not in n1.getOutgoing()
    assert e1 not in n2.getIncoming()

    n3 = fdd.Node(lvl1)

    e1.setOrigin(n3)
    e1.autoConnect()

    assert e1 not in n1.getOutgoing()
    assert e1 in n3.getOutgoing()

    e5 = fdd.Edge([1], n1, n2, DirectionSet(['0.0.10.0/24']))
    e6 = fdd.Edge([1, 2], n1, n2, DirectionSet(['0.0.10.0/24']))

    assert e5.getId() == [1]
    assert e6.getId() == [1, 2]


def test_node():
    """_summary_
    """

    f1 = Field("IPSrc", "DirSet")

    lvl1 = fdd.Level(f1)
    lvl2 = fdd.Level(f1)

    n1 = fdd.Node(lvl1)
    n2 = fdd.Node(lvl2)

    assert n1 not in lvl1.getNodes()
    assert n2 not in lvl2.getNodes()

    n1.autoConnect()
    n2.autoConnect()

    assert n1 not in lvl2.getNodes()
    assert n2 not in lvl1.getNodes()
    assert n1 in lvl1.getNodes()
    assert n2 in lvl2.getNodes()

    n1.autoDisconnect()
    n2.autoDisconnect()

    assert n1 not in lvl1.getNodes()
    assert n2 not in lvl2.getNodes()

