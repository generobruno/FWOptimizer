"""_summary_
"""

#TODO REVISAR IMPORTS
from classes import parser, fdd

if __name__ == '__main__':
    
    print("TESTING...")
    
    #! Parse Instruction Set
    iptables_strat = parser.IpTablesParser()
    parser = parser.Parser(iptables_strat)
    rules_parsed = parser.parse("./example_set.txt")

    print("\nRule Set:")
    rules_parsed.print_all()

    print("\nOnly INPUT in filter")
    for rule in rules_parsed['filter']['INPUT']: # Tambien se puede acceder como: rules_parsed.tables['filter'].chains['INPUT']
        print(rule)
        
    print(f'\nTotal Number of Tables: {len(rules_parsed.tables)}')
    print(f'Total Number of Chains: {rules_parsed.number_of_chains()}')
    print(f'Total Number of Rules: {len(rules_parsed)}')
