"""_summary_
"""

import sys
import os
import portion as p

# Add Root Dir to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fwoptimizer.classes import parser

from fwoptimizer.classes import *
from fwoptimizer.utils import *
from fwoptimizer.utils.elementSet import PortSet

# if __name__ == '__main__':

#     print("TESTING...")

#     #! Parse Instruction Set
#     iptables_strat = parser.IpTablesParser()
#     parser = parser.Parser(iptables_strat)
#     rules_parsed = parser.parse("./example_set.txt")

#     print("\nRule Set:")
#     rules_parsed.printAll()

#     print("\nOnly INPUT in filter")
#     # Tambien se puede acceder como: rules_parsed.tables['filter'].chains['INPUT']
#     for rule in rules_parsed['filter']['INPUT']:
#         print(rule)

#     print(f'\nTotal Number of Tables: {len(rules_parsed.getTables())}')
#     print(f'Total Number of Chains: {rules_parsed.numberOfChains()}')
#     print(f'Total Number of Rules: {len(rules_parsed)}\n')

#     fieldList = FieldList()
#     fieldList.loadConfig("fwoptimizer/configs/fdd_config.toml")

#     chain = rules_parsed['filter']['INPUT']

#     fdd = FDD(fieldList)
#     fdd.genFDD(chain)
#     fdd.printFDD("FDD")

#     print("\nREDUCING:")
#     fdd.reduction()
#     #fdd.printFDD("reducedFDD")
    
#     print("\nMARKING:")
#     fdd.marking()
#     fdd.printFDD("MarkedFDD")
    
#     print("\nCREATING RULES:")
#     firewall_chain = fdd.firewallGen() #TODO Crear nuevo RuleSet con las chains y tablas modificadas
#     print(firewall_chain)
    
#     #print('\nSIMPLIFYING RULES:')
#     #firewall_chain.simplifyRules()
#     #print(firewall_chain)
    
#     print("\nCREATING RULES FILE...")
#     # Create RuleSet and Table to add the test chain
#     testTable = rules.Table("testTable")
#     firewall_chain.setDefaultDecision("DROP")
#     testTable.addChain(firewall_chain)
#     testRuleSet = rules.RuleSet()
#     testRuleSet.addTable(testTable)
#     # Create rules file according to parser strategy
#     print(parser.compose(testRuleSet))



# a = p.closed(10, 20)
# b = p.closed(30, 40)
# c = a | b

# print(a)
# print(b)
# print(c)

# print(type(a))
# print(type(c))

# d = p.closed(12, 15)
# e = p.closed(29, 31)

# print(d in c)
# print(e in c)

# print(list(c))

# f = p.closed(100,100)
# print(list(f))
# print(100 in f)
# print(list(f | c))

a = PortSet(['15', '17', '20:30'])

PortSet.setGroupable(False)
print(a.getElementsList())
PortSet.setGroupable(True)
print(a.getElementsList())

b = PortSet(['14', '25:35'])

print(b.getElementsList())

print()

print(PortSet.getDomain())
print(PortSet.getDomainList())

c = PortSet.getDomain()

c.remove(b)

print(c.getElementsList())

ports2 = PortSet(['88', '89', '90', '99'])
print(ports2.getElementsList())

