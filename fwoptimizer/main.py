"""_summary_
"""

import sys
import os
import time

# Add Root Dir to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fwoptimizer.classes import parser
from fwoptimizer.classes import *
from fwoptimizer.utils import *

if __name__ == '__main__':
    total_start_time = time.time()
    execution_times = {}

    #! Parse Instruction Set
    iptables_strat = parser.IpTablesParser()
    parser = parser.Parser(iptables_strat)
    rules_parsed = parser.parse("./example_set.txt")

    print("\nOnly INPUT in filter")
    for rule in rules_parsed['filter']['INPUT']:
        print(rule)

    fieldList = FieldList()
    fieldList.loadConfig("fwoptimizer/configs/fdd_config.toml")

    chain = rules_parsed['filter']['INPUT']

    fdd = FDD(fieldList)
    
    gen_start = time.time()
    fdd.genFDD(chain)
    gen_end = time.time()
    execution_times['genFDD'] = gen_end - gen_start

    print("\nREDUCING:")
    reduction_start = time.time()
    fdd.reduction()
    reduction_end = time.time()
    execution_times['reduction'] = reduction_end - reduction_start
    
    print("\nMARKING:")
    marking_start = time.time()
    fdd.marking()
    marking_end = time.time()
    execution_times['marking'] = marking_end - marking_start
    
    print_start = time.time()
    fdd.printFDD("MarkedFDD", rank_dir='LR', unroll_decisions=True)
    print_end = time.time()
    execution_times['printFDD'] = print_end - print_start
    
    print("\nCREATING RULES:")
    firewall_gen_start = time.time()
    firewall_chain = fdd.firewallGen() #TODO Crear nuevo RuleSet con las chains y tablas modificadas
    firewall_gen_end = time.time()
    execution_times['firewallGen'] = firewall_gen_end - firewall_gen_start
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
    compose_start = time.time()
    composed_rules = parser.compose(testRuleSet)
    compose_end = time.time()
    execution_times['compose'] = compose_end - compose_start
    print(composed_rules)
    
    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time

    # Print all execution times at the end
    print("\nExecution Times:")
    for func, time_taken in execution_times.items():
        print(f"{func}() execution time: {time_taken:.4f} seconds")
    print(f"Total execution time: {total_execution_time:.4f} seconds")