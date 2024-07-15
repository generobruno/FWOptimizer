import pytest
from fwoptimizer.classes.parser import IpTablesParser, Parser
from fwoptimizer.classes.firewall import FieldList

def test_chain_equivalence_to_itself():
    # Parse Instruction Set
    iptables_strat = IpTablesParser()
    parser = Parser(iptables_strat)
    rules_parsed = parser.parse("tests/test_set.txt")

    # Load field configuration
    fieldList = FieldList()
    fieldList.loadConfig("fwoptimizer/configs/fdd_config.toml")

    # Get the chain to be tested
    chain = rules_parsed['filter']['INPUT']

    # Check if the chain is equivalent to itself
    #equivalence, diff_rules_1, diff_rules_2, diff_1, diff_2 = chain.isEquivalent(chain, fieldList)

    # Assert that the chain is equivalent to itself
    #assert equivalence, "Chain should be equivalent to itself"
    #assert not diff_rules_1, "There should be no differing rules in the first chain"
    #assert not diff_rules_2, "There should be no differing rules in the second chain"
    #assert not diff_1, "There should be no differing packets in the first chain"
    #assert not diff_2, "There should be no differing packets in the second chain"
