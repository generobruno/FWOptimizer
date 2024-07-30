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
