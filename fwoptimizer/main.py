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

    #print("TESTING...")

    #! Parse Instruction Set
    iptables_strat = parser.IpTablesParser()
    parser = parser.Parser(iptables_strat)
    rules_parsed = parser.parse("./example_set.txt")

    #print("\nRule Set:")
    #rules_parsed.printAll()

    print("\nOnly INPUT in filter")
    # Tambien se puede acceder como: rules_parsed.tables['filter'].chains['INPUT']
    for rule in rules_parsed['filter']['INPUT']:
        print(rule)

    #print(f'\nTotal Number of Tables: {len(rules_parsed.getTables())}')
    #print(f'Total Number of Chains: {rules_parsed.numberOfChains()}')
    #print(f'Total Number of Rules: {len(rules_parsed)}\n')

    fieldList = FieldList()
    fieldList.loadConfig("fwoptimizer/configs/fdd_config.toml")

    chain = rules_parsed['filter']['INPUT']

    #print(f'\nEFFECTIVE PART:\n{chain[4].getEffectivePart(chain, fieldList)}\n')
    #exit(0)
 
    # chain_2 = rules_parsed['filter']['OUTPUT']
    # equivalence, diff_rules_1, diff_rules_2, diff_1, diff_2 = chain.isEquivalent(chain_2, fieldList)
    # print(f'EQUIVALENT: {equivalence}\n')
    # print('DIFF_RULES_1:')
    # print("\n".join(str(i) for i in diff_rules_1))
    # print('DIFF_RULES_2:')
    # print("\n".join(str(i) for i in diff_rules_2))
    # print()
    # print('DIFF_1:')
    # print("\n".join(str(i) for i in diff_1))
    # print('DIFF_2:')
    # print("\n".join(str(i) for i in diff_2))
    # exit(0)

    fdd = FDD(fieldList)
    fdd.genFDD(chain)
    #fdd.printFDD("FDD", 'svg')

    print("\nREDUCING:")
    fdd.reduction()
    #fdd.printFDD("reducedFDD")
    
    print("\nMARKING:")
    fdd.marking()
    #fdd.printFDD("MarkedFDD", 'svg')
    
    print("\nCREATING RULES:")
    firewall_chain = fdd.firewallGen() #TODO Crear nuevo RuleSet con las chains y tablas modificadas
    print("\nRULES CREATION FINISHED")
    print(firewall_chain)
    
    #print('\nSIMPLIFYING RULES:')
    #firewall_chain.simplifyRules()
    #print(firewall_chain)
    
    print("\nCREATING RULES FILE...")
    # Create RuleSet and Table to add the test chain
    testTable = rules.Table("testTable")
    firewall_chain.setDefaultDecision("DROP")
    testTable.addChain(firewall_chain)
    testRuleSet = rules.RuleSet()
    testRuleSet.addTable(testTable)
    # Create rules file according to parser strategy
    print(parser.compose(testRuleSet))