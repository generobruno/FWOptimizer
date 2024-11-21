"""_summary_
"""

import pytest
from fwoptimizer.core.fields import ElementSetRegistry, ElementSet, DirectionSet, ProtocolSet, PortSet
from fwoptimizer.core.rules import Chain, Rule
from fwoptimizer.core.firewall import FieldList
from fwoptimizer.core.fdd import FDD

def test_registry():
    """_summary_
    """

    expectedRegistred = ['ElementSet', 'DirectionSet', 'ProtocolSet', 'PortSet']
    
    for i in expectedRegistred:

        assert i in ElementSetRegistry.getRegistry()


def test_createElementSet():
    """
    sumary
    """

    direction = ElementSet.createElementSet('DirectionSet', ['0.0.10.0/24'])
    protocol = ElementSet.createElementSet('ProtocolSet', ['TCP'])

    assert isinstance(direction, DirectionSet)
    assert isinstance(protocol, ProtocolSet)

    dcomp1 = DirectionSet(['0.0.10.0/24'])
    dcomp2 = DirectionSet(['0.0.11.0/24'])

    assert direction == dcomp1
    assert direction != dcomp2

    pcomp1 = ProtocolSet(['TCP'])
    pcomp2 = ProtocolSet(['UDP'])

    assert protocol == pcomp1
    assert protocol != pcomp2

    direction2 = ElementSet.createElementSet('DirectionSet', [])
    protocol2 = ElementSet.createElementSet('ProtocolSet', [])

    assert direction2.getElementsList() == ['0.0.0.0/0']
    assert sorted(protocol2.getElementsList()) == sorted(['tcp', 'icmp', 'udp'])

    with pytest.raises(ValueError):
        direction3 = ElementSet.createElementSet('ProtocolSet', ['udo'])


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


def test_PortSet():
    """summary
    """
    PortSet.setGroupable(False)

    ports = PortSet(['88', '99'])
    assert ports.getElementsList() == ['88', '99']

    ports2 = PortSet(['88', '89', '90', '99'])
    assert ports2.getElementsList() == ['88', '89', '90', '99']

    ports3 = PortSet(['88:90', '99'])
    assert ports3.getElementsList() == ['88', '89', '90', '99']

    PortSet.setGroupable(True)

    assert ports.getElementsList() == ['88', '99']

    assert ports2.getElementsList() == ['88:90', '99']

    assert ports3.getElementsList() == ['88:90', '99']

    assert ports2 == ports3

    domain = PortSet.getDomain()

    assert domain.getElementsList() == ['0:65535']

    new1 = PortSet(['89:91', '100', '110'])

    new1.add(ports)

    assert new1.getElementsList() == ['88:91', '99:100', '110']

    new2 = PortSet(['90', '120'])
    new3 = PortSet(['200', '300'])

    assert new1.isOverlapping(new2)
    assert not new1.isOverlapping(new3)

    assert not new1.intersectionSet(new2).isEmpty()
    assert new1.intersectionSet(new3).isEmpty()

    assert ports.isSubset(ports2)
    assert not new2.isSubset(ports2)

    assert not new2.isDisjoint(ports2)
    assert new2.isDisjoint(ports)

    assert new1.intersectionSet(new2).getElementsList() == ['90']

    assert new1.unionSet(new2).getElementsList() == ['88:91', '99:100', '110', '120']

    new1.remove(new2)

    assert new1.getElementsList() == ['88:89', '91', '99:100', '110']

    new4 = ports.replicate()

    assert new4.getElementsList() == ['88', '99']