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

    print(f'\nTotal Number of Tables: {len(rules_parsed._tables)}')
    print(f'Total Number of Chains: {rules_parsed.numberOfChains()}')
    print(f'Total Number of Rules: {len(rules_parsed)}\n\n')

    fieldList = FieldList()
    fieldList.loadConfig("fwoptimizer/configs/fdd_config.toml")

    fdd = FDD()
    fdd.genPre(fieldList, rules_parsed['filter']['INPUT'])
    fdd.printFDD("preFDD")

    fdd.sanity()
    fdd.printFDD("SanityFDD")
    
    print("REDUCING:")
    fdd.reduction()
    fdd.printFDD("reducedFDD")
