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

ruleset = None
field_list = None
fdds = {}

def parse_file():
    try:
        global ruleset
        filename = input("Enter the filename to parse: ")
        # Select Parse Strategy
        iptables_strat = parser.IpTablesParser() # TODO Set parse strat
        # Create Parser Object
        parser_obj = parser.Parser(iptables_strat)
        # Parse File
        ruleset = parser_obj.parse(filename)
        print("File parsed successfully.")
    except Exception as e:
        print(f'Could not parse file. {e}')

def display_rules():
    try:
        if not ruleset:
            print("No ruleset parsed yet. Please parse a file first.")
            return
        table = input("Enter table name: ")
        chain = input("Enter chain name: ")

        print(ruleset[table][chain])
    except Exception as e:
        print(f'Could not Display rules: {e}')

def add_field_list():
    try:
        global field_list
        config_file = input("Enter config file path: ")
        # Create FieldList Object
        field_list = FieldList()
        # Load Config
        field_list.loadConfig(config_file)
        print("Field list added successfully.")
    except Exception as e:
        print(f'Could not add FieldList. {e}')

def generate_fdds():
    try:
        global fdds, ruleset, field_list
        if not ruleset or not field_list:
            print("Ruleset or field list not set. Please parse a file and add field list first.")
            return
        
        for table in ruleset.getTables():
            fdds[table] = {}
            for chain in ruleset[table].getChains():
                if len(ruleset[table][chain].getRules()) != 0: 
                    fdd = FDD(field_list)
                    fdd.genFDD(ruleset[table][chain])
                    fdds[table][chain] = fdd

        print("FDDs generated successfully.")
    except Exception as e:
        print(f'Could not generate FDD. {e}')

def compile_fdd():
    if not fdds:
        print("No FDDs generated yet. Please generate FDDs first.")
        return
    
    table = input("Enter table name: ")
    chain = input("Enter chain name: ")
    # Execute Reduction and Marking
    if table in fdds and chain in fdds[table]:
        fdds[table][chain].reduction()
        fdds[table][chain].marking()
        print(f"FDD for {table}/{chain} compiled successfully.")
    else:
        print(f"FDD for {table}/{chain} not found.")

def generate_optimized_ruleset():
    if not fdds:
        print("No FDDs generated yet. Please generate FDDs first.")
        return
    
    table = input("Enter table name: ")
    chain = input("Enter chain name: ")
    if table in fdds and chain in fdds[table]:
        optimized_ruleset = fdds[table][chain].firewallGen()
        print("Optimized ruleset generated:")
        print(optimized_ruleset)
    else:
        print(f"FDD for {table}/{chain} not found.")

def print_fdd():
    if not fdds:
        print("No FDDs generated yet. Please generate FDDs first.")
        return
    
    table = input("Enter table name: ")
    chain = input("Enter chain name: ")
    if table in fdds and chain in fdds[table]:
        name = input("Enter output file name: ")
        format = input("Enter output format (default: svg): ") or 'svg'
        fdds[table][chain].printFDD(name, format)
        print(f"FDD for {table}/{chain} printed to {name}.{format}")
    else:
        print(f"FDD for {table}/{chain} not found.")

if __name__ == '__main__':
    commands = {
        "parse": parse_file,
        "display": display_rules,
        "addfields": add_field_list,
        "generate": generate_fdds,
        "compile": compile_fdd,
        "optimize": generate_optimized_ruleset,
        "print": print_fdd
    }

    while True:
        command = input("\n--- Insert a command: ").strip().lower()
        if command == "exit":
            break
        elif command == "help":
            print("Available commands are: " + ", ".join(commands.keys()))
        elif command in commands:
            commands[command]()
        else:
            print("Invalid command, type \"help\" for more information.")

if __name__ == '__main2__':

    iptables_strat = parser.IpTablesParser()
    parser = parser.Parser(iptables_strat)
    rules_parsed = parser.parse("./.example_set_C.txt")

    chain1 = rules_parsed['filter']['INPUT']
    print("Chain1:")
    for rule in chain1:
        print(rule)

    fieldList = FieldList()
    fieldList.loadConfig("fwoptimizer/configs/fdd_config.toml")

    rules_parsed = parser.parse("./.example_set_D.txt")

    chain2 = rules_parsed['filter']['INPUT']
    print("Chain2:")
    for rule in chain2:
        print(rule)

    # fdd = FDD(fieldList)
    # fdd.genFDD(chain1)
    # #fdd.printFDD("FDD", 'svg')

    # fdd.reduction()
    # #fdd.printFDD("reducedFDD")
    
    # fdd.marking()
    # #fdd.printFDD("MarkedFDD", 'svg')
    
    # firewall_chain = fdd.firewallGen()
    # firewall_chain.setDefaultDecision("DROP") 

    #print(firewall_chain)

    comparator = ChainComparator(fieldList)
    comparator.setChain1FromChain(chain1)
    comparator.setChain2FromChain(chain2)
    print(f"{comparator}")
    print(f"\nLa comparacion entre chain1 y chain2 da: {comparator.areEquivalents()}")