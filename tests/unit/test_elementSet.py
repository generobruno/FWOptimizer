"""_summary_
"""

import pytest
from fwoptimizer.utils.elementSet import ElementSetRegistry, ElementSet, DirSet, ProtSet
from fwoptimizer.classes.rules import Chain, Rule
from fwoptimizer.classes.firewall import FieldList
from fwoptimizer.classes.fdd import FDD

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

    direction2 = ElementSet.createElementSet('DirSet', [None])
    protocol2 = ElementSet.createElementSet('ProtSet', [None])

    assert direction2.getElementsList() == ['0.0.0.0/0']
    assert sorted(protocol2.getElementsList()) == sorted(['tcp', 'icmp', 'udp'])

    with pytest.raises(ValueError):
        direction3 = ElementSet.createElementSet('ProtSet', ['udo'])


def test_presenseOFPredicateInFieldList():
    """sumary
    """

    chain = Chain("INPUT")
    rule = Rule(1)
    rule.setPredicate('SrcIP', '10.0.0.0/24')
    rule.setPredicate('NoEx', '10.0.0.0/24')
    rule.setDecision('ACCEPT')
    chain.addRule(rule)

    fieldList = FieldList()
    fieldList.loadConfig("tests/test_fdd_config.toml")

    fdd = FDD(fieldList)
    with pytest.raises(TypeError):
        fdd.genFDD(chain)