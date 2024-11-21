
import pytest

from fwoptimizer.core.comparator import ChainComparator
from fwoptimizer.core.firewall import FieldList
from fwoptimizer.core.rules import Rule, Chain


def test_pseudoRule_difference1():
    """_summary_
    """

    fieldList = FieldList()
    fieldList.loadConfig("tests/test_fdd_config.toml")

    rule = Rule(0)
    rule.setDecision("ACCEPT")
    rule.setPredicate("SrcIP", ["128.0.0.0/1"])
    rule.setPredicate("DstIP", ["0.0.0.0/1"])
    rule.setPredicate("Protocol", ["icmp"])

    r1 = ChainComparator.PseudoRule()
    r1.fillFromRule(rule, fieldList)

    rule = Rule(1)
    rule.setDecision("ACCEPT")
    rule.setPredicate("SrcIP", ["0.0.0.0/0"])
    rule.setPredicate("DstIP", ["0.0.0.0/0"])
    rule.setPredicate("Protocol", ["icmp", "tcp", "udp"])

    r2 = ChainComparator.PseudoRule()
    r2.fillFromRule(rule, fieldList)

    res = r2.difference(r1, fieldList)

    expected_res = []

    aux = Rule(1)
    aux.setDecision("ACCEPT")
    aux.setPredicate("SrcIP", ["0.0.0.0/1"])
    aux.setPredicate("DstIP", ["0.0.0.0/0"])
    aux.setPredicate("Protocol", ["icmp", "tcp", "udp"])
    expected_res.append(ChainComparator.PseudoRule())
    expected_res[0].fillFromRule(aux, fieldList)

    aux = Rule(1)
    aux.setDecision("ACCEPT")
    aux.setPredicate("SrcIP", ["0.0.0.0/0"])
    aux.setPredicate("DstIP", ["128.0.0.0/1"])
    aux.setPredicate("Protocol", ["icmp", "tcp", "udp"])
    expected_res.append(ChainComparator.PseudoRule())
    expected_res[1].fillFromRule(aux, fieldList)

    aux = Rule(1)
    aux.setDecision("ACCEPT")
    aux.setPredicate("SrcIP", ["0.0.0.0/0"])
    aux.setPredicate("DstIP", ["0.0.0.0/0"])
    aux.setPredicate("Protocol", ["tcp", "udp"])
    expected_res.append(ChainComparator.PseudoRule())
    expected_res[2].fillFromRule(aux, fieldList)

    for i in range(len(res)):

        assert res[i].sameFieldValues(expected_res[i])

def test_pseudoRule_difference2():

    fieldList = FieldList()
    fieldList.loadConfig("tests/test_fdd_config.toml")

    rule = Rule(0)
    rule.setDecision("ACCEPT")
    rule.setPredicate("SrcIP", ["0.0.0.0/1"])
    rule.setPredicate("DstIP", ["0.0.0.0/1"])
    rule.setPredicate("Protocol", ["icmp"])

    r1 = ChainComparator.PseudoRule()
    r1.fillFromRule(rule, fieldList)

    rule = Rule(1)
    rule.setDecision("ACCEPT")
    rule.setPredicate("SrcIP", ["128.0.0.0/1"])
    rule.setPredicate("DstIP", ["128.0.0.0/1"])
    rule.setPredicate("Protocol", ["tcp"])

    r2 = ChainComparator.PseudoRule()
    r2.fillFromRule(rule, fieldList)

    res = r2.difference(r1, fieldList)
    
    assert len(res) == 1 and res[0].sameFieldValues(r2)

def test_pseudoChain():

    """_summary_
    """

    fieldList = FieldList()
    fieldList.loadConfig("tests/test_fdd_config.toml")

    rawChain = Chain("TEST")
    rawChain.setDefaultDecision("DROP")


    rule = Rule(0)
    rule.setDecision("ACCEPT")
    rule.setPredicate("SrcIP", ["128.0.0.0/1"])
    rule.setPredicate("DstIP", ["0.0.0.0/1"])
    rule.setPredicate("Protocol", ["icmp"])
    rawChain.addRule(rule)

    rule = Rule(1)
    rule.setDecision("DROP")
    rule.setPredicate("SrcIP", ["0.0.0.0/0"])
    rule.setPredicate("DstIP", ["0.0.0.0/1"])
    rule.setPredicate("Protocol", ["icmp"])
    rawChain.addRule(rule)

    rule = Rule(2)
    rule.setDecision("ACCEPT")
    rule.setPredicate("SrcIP", ["0.0.0.0/0"])
    rule.setPredicate("DstIP", ["0.0.0.0/1"])
    rule.setPredicate("Protocol", ["icmp", "tcp", "udp"])
    rawChain.addRule(rule)

    print()
    print(rawChain)

    chain = ChainComparator.PseudoChain()
    chain.fillFromChain(rawChain, fieldList)
    print(chain)

    efChain = chain.getEffectiveChain(fieldList)
    print(efChain)
    





