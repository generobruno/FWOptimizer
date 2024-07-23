"""
Tests for the parser Module
"""

import pytest
from fwoptimizer.classes.parser import IpTablesParser, Parser

# Path to the sample input data file
sample_path = 'tests/test_set.txt'

# Define expected rules
expected_rules = [
    {'chain': 'INPUT', 'source': '1.1.1.0/24', 'destination': '2.2.2.0/24', 'protocol': 'udp', 'decision': 'DROP'},
    {'chain': 'INPUT', 'source': '1.1.1.128/25', 'destination': '3.3.3.0/24', 'protocol': 'tcp', 'decision': 'ACCEPT'},
    {'chain': 'INPUT', 'source': '1.1.1.128/25', 'destination': '3.3.3.0/25', 'protocol': 'udp', 'decision': 'DROP'},
    {'chain': 'INPUT', 'source': '1.1.1.128/25', 'destination': '3.3.3.64/30', 'protocol': 'udp', 'decision': 'ACCEPT'},
    {'chain': 'INPUT', 'source': '1.1.1.128/25', 'destination': '3.3.3.68/30', 'protocol': 'udp', 'decision': 'DROP'}
]

# Test initialization
def test_parser_initialization():
    """_summary_
    """
    # Parse Instruction Set
    iptables_strat = IpTablesParser()
    parser = Parser(iptables_strat)
    rules_parsed = parser.parse(sample_path)

    # Get the chain to be tested
    chain = rules_parsed['filter']['INPUT']

    # Check if the number of rules in the chain matches the expected number
    assert len(chain.getRules()) == len(expected_rules), "Number of rules in the chain does not match expected."
    
    # Compare each rule in the chain with the corresponding expected rule
    for i, rule in enumerate(chain.getRules()):
        assert rule.getOption('SrcIP') == [expected_rules[i]['source']], f"Rule {i} source mismatch."
        assert rule.getOption('DstIP') == [expected_rules[i]['destination']], f"Rule {i} destination mismatch."
        assert rule.getOption('Protocol') == [expected_rules[i]['protocol']], f"Rule {i} protocol mismatch."
        assert rule.getDecision() == expected_rules[i]['decision'], f"Rule {i} decision mismatch."
