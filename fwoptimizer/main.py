"""_summary_
"""

#TODO REVISAR IMPORTS
from classes import parser, rules

if __name__ == '__main__':
    
    print("TESTING...")
    
    #! Parse Instruction Set
    iptables_strat = parser.IpTablesParser()
    parser = parser.Parser(iptables_strat)
    rules_parsed = parser.parse("./example_set.txt")

    print("\nRule Set:")
    for table in rules_parsed:
        for chain in rules_parsed[table]:
            print(f'{table} - {chain}:')
            for rule in rules_parsed[table][chain]:
                print(rule)

    #! Create Rules from list
    rule_factory = rules.RuleFactory()
    rules = {}
    
    for table in rules_parsed:
        for chain in rules_parsed[table]:
            rules[(table, chain)] = (rule_factory.create_rules(rules_parsed[table][chain]))
        
    print("\nRules Obtained:")        
    for (table, chain), chain_rules in rules.items():
        print(f"{table} - {chain}:")
        for rule in chain_rules:
           print(rule)
    print()
    
    print(rules[('filter', 'INPUT')])