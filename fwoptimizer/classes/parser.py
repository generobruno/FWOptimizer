"""_summary_
"""

import re
from ..utils.aliasDict import AliasDefaultDict

class Parser:
    """_summary_
    """
    
    def __init__(self, syntaxTable):
        """_summary_

        Args:clear
        
            syntaxTable (_type_): _description_
        """
        self.syntaxTable = self.preprocess_syntax_table(syntaxTable)
        self.rules = {}

    def preprocess_syntax_table(self, syntaxTable):
        """_summary_

        Args:
            syntaxTable (_type_): _description_

        Returns:
            _type_: _description_
        """
        preprocessed_table = {}
        for table, table_ops in syntaxTable.items(): # Create Dict for each Table
            preprocessed_table[table] = AliasDefaultDict(dict)
            for rule_type, rule_options in table_ops.items():  # Create Dict for each type of op
                preprocessed_table[table][rule_type] = AliasDefaultDict(dict)
                for option_set in rule_options: # Create alias and assign values
                    regex = rule_options[option_set]
                    aliases = [alias.strip() for alias in option_set.split('|')]
                    for alias in aliases:   # Assign Value to all aliases
                        preprocessed_table[table][rule_type][alias] = regex
                        #print(f'{table},{rule_type},{alias} = {preprocessed_table[table][rule_type][alias]}')
        return preprocessed_table

    def parse(self, file_path):
        """_summary_

        Args:
            file_path (_type_): _description_
        """
        with open(file_path, 'r') as file:
            current_table = None
            current_chain = None
            current_rule = {}
            line_num = 0

            for line in file:                              # Parse Line-by-Line
                line_num += 1
                line = line.strip()

                if line.startswith('*'):
                    current_table = line[1:]
                    self.rules[current_table] = {}                  # Current Table Level {'CURRENT_TABLE': {'chain': [rules]}}
                elif line.startswith(':'):
                    current_chain = line.split()[0][1:] 
                    current_rule = {}
                    self.rules[current_table][current_chain] = []   # Current Chain Level {'table': {'CURRENT_CHAIN': [rules]}}
                elif line.startswith('['): #TODO Revisar que hacer con politicas default
                    current_rule = {}
                elif line == 'COMMIT':                              # End of File
                    current_table = None
                    current_chain = None
                    break
                else:                                               # Parsing Rule Options
                    current_rule = self.parse_options(line, line_num, current_table)

                    if current_rule:
                        self.rules[current_table][current_chain].append(current_rule)
                        
    def parse_options(self, line, line_num, current_table):
        """_summary_

        Args:
            line (_type_): _description_
            line_num (_type_): _description_
            current_table (_type_): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        current_rule = {}
        option_pattern = r'-\w+(?=\s*\S)|--\w+'
        option_value_pairs = re.findall(fr'({option_pattern})(?:\s*(\S+))?', line)

        for option, value in option_value_pairs:
            found_match = False
            # Get Regex of option
            regex = self.syntaxTable[current_table]['RuleOperations'][option]
            if regex:
                if regex is None: # TODO Revisar -> cambiar valor de opciones que son None
                    current_rule[option] = None
                    found_match = True
                    continue
                else:
                    if value is not None:
                        match = re.match(regex, value)
                        if match:
                            current_rule[option] = match.group()
                            found_match = True
                            continue
                        else:   # Value does not follow regex
                            print(f"Warning: Value '{value}' does not match the expected format for option '{option}' in line: {line}")
                            raise ValueError(f"Syntax Error in line {line_num}")
                    else:       # Value needed after option
                        print(f"Warning: Option '{option}' requires a value in line: {line}")
                        raise ValueError(f"Syntax Error in line {line_num}")

            if not found_match and option not in ["-A", "-I", "-D", "-R"]:  # Option not recognized or is a Table Op
                print(f"Warning (line {line_num}): Unrecognized option '{option}' in line: {line}")
                continue

        return current_rule

    def get_rules(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.rules