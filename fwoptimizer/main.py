"""_summary_
"""

#TODO REVISAR IMPORTS
from fwoptimizer.classes import Parser
from fwoptimizer.classes import RuleFactory

import configs.syntaxes.iptables_syntax as iptables 

if __name__ == '__main__':
    
    print("TESTING...")
    
    #! Parse Instruction Set
    parser = Parser(iptables.syntaxTable)
    parser.parse("example_set.txt")
    rules_parsed = parser.get_rules()

    print("\nRule Set:")
    for table in rules_parsed:
        for chain in rules_parsed[table]:
            print(f'{table} - {chain}:')
            for rule in rules_parsed[table][chain]:
                print(rule)

    #! Create Rules from list
    rule_factory = RuleFactory()
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