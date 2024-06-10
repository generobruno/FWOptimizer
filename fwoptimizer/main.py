"""_summary_
"""

import sys
import os

# Add Root Dir to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fwoptimizer.classes import parser

from fwoptimizer.classes import *
from fwoptimizer.utils import *

if __name__ == '__main__':

    print("TESTING...")

    #! Parse Instruction Set
    iptables_strat = parser.IpTablesParser()
    parser = parser.Parser(iptables_strat)
    rules_parsed = parser.parse("./example_set.txt")

    print("\nRule Set:")
    rules_parsed.printAll()

    print("\nOnly INPUT in filter")
    # Tambien se puede acceder como: rules_parsed.tables['filter'].chains['INPUT']
    for rule in rules_parsed['filter']['INPUT']:
        print(rule)

    print(f'\nTotal Number of Tables: {len(rules_parsed.tables)}')
    print(f'Total Number of Chains: {rules_parsed.numberOfChains()}')
    print(f'Total Number of Rules: {len(rules_parsed)}')


    fieldList = FieldList()
    fieldList.loadConfig("fwoptimizer/configs/fdd_config.toml")

    ch = Chain("input")
    ru1 = Rule(1)
    ru1.setPredicate('SrcIP', '100.0.10.0/24')
    ru1.setPredicate('DstIP', '200.0.10.0/28')
    ru1.setPredicate('Protocol', 'TCP')
    ru1.setDecision('ACCEPT')
    ch.addRule(ru1)

    ru2 = Rule(5)
    ru2.setPredicate('SrcIP', '100.0.11.0/16')
    ru2.setPredicate('DstIP', '200.0.11.0')
    ru2.setPredicate('Protocol', 'TCP')
    ru2.setDecision('DROP')
    ch.addRule(ru2)

    ru3 = Rule(6)
    ru3.setPredicate('SrcIP', '100.0.12.0')
    ru3.setPredicate('DstIP', '200.0.12.0')
    ru3.setPredicate('Protocol', 'TCP')
    ru3.setDecision('ACCEPT')
    ch.addRule(ru3)

    print(rules_parsed['filter']['INPUT'])
    print(ch)


    fdd = FDD()
    fdd.genPre(fieldList, rules_parsed['filter']['INPUT'])
    #fdd.genPre(fieldList, ch)
    fdd.printFDD("RESULT")
