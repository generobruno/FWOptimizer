"""
Tests for the Edge, Node, Level and FDD classes
"""

import pytest
import fwoptimizer.classes.fdd as fdd
from fwoptimizer.classes.firewall import Field


def test_edge():
    """_summary_
    """

    f1 = Field("IPSrc", "DirSet")

    lvl1 = fdd.Level("uno",f1)
    lvl2 = fdd.Level("dos", f1)

    n1 = fdd.Node("a", lvl1)
    n2 = fdd.Node("a", lvl2)

    e1 = fdd.Edge(n1, n2, 1)
    e2 = fdd.Edge(n1, n2, 1)
    e3 = fdd.Edge(n1, n2, 2)
    e4 = e3.replicate()

    assert e1 == e2
    assert e1 != e3
    assert e3 == e4

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

    n3 = fdd.Node("a", lvl1)

    e1.setOrigin(n3)
    e1.autoConnect()

    assert e1 not in n1.getOutgoing()
    assert e1 in n3.getOutgoing()


def test_node():
    """_summary_
    """

    f1 = Field("IPSrc", "DirSet")

    lvl1 = fdd.Level("uno",f1)
    lvl2 = fdd.Level("dos", f1)

    n1 = fdd.Node("a", lvl1)
    n2 = fdd.Node("a", lvl2)

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