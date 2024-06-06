"""_summary_
"""

from fwoptimizer.classes import parser

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
