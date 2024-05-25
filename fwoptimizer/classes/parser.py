"""_summary_
"""

import re
from abc import ABC, abstractmethod

from utils.aliasDict import AliasDefaultDict
from classes import rules

import configs.syntaxes as syntaxes

class ParserStrategy(ABC):
    """
    ParserStrategy interface declares operations common to all supported versions
    of some algorithm.
    
    The Parser Context Class uses this interface to call the algorithm defined by
    Concrete Strategies
    """
    
    @abstractmethod
    def parse(self, file) -> rules.RuleSet:
        pass
    
class IpTablesParser(ParserStrategy):
    """
    """
    
    def __init__(self):
        """
        IpTables Parser Strategy
        """
        self.syntaxTable = self.preprocess_syntax_table(syntaxes.iptables)
        self.ruleset = rules.RuleSet()

    def preprocess_syntax_table(self, syntaxTable):
        """
        Process the syntax table to obtain all the posible alias of the
        different options

        Args:
            syntaxTable (dict): Syntax table for iptables

        Returns:
            dict: Processed syntax table
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

    def parse(self, path):
        """Parse the iptables configuration file

        Args:
            path (str): The path to the file to parse

        Returns:
            RuleSet: Parsed ruleset
        """
        with open(path, 'r') as file:
            current_table = None
            current_chain = None
            rule_id = 0

            for line in file:
                line = line.strip()

                if line.startswith('#'):            # Ignore comments
                    continue

                if line.startswith('*'):            # Start of Table
                    current_table = rules.Table(line[1:])
                    self.ruleset.add_table(current_table)
                elif line.startswith(':'):          # Define Chain
                    chain_name = line.split()[0][1:]
                    current_chain = rules.Chain(chain_name)
                    current_table.add_chain(current_chain)
                elif line.startswith('['):  # TODO REVISAR Default Policies
                    continue 
                elif line == 'COMMIT':              # End of Table
                    current_table = None
                    current_chain = None
                else:
                    if line.startswith('-A'):       # Append Rule to Chain
                        chain_name = line.split()[1]
                        current_chain = current_table[chain_name]
                    current_rule = self.parse_options(line, rule_id, current_table.name)
                    if current_rule:                # Parse Rule
                        rule = rules.Rule(rule_id)
                        rule.predicates = {k: v for k, v in current_rule.items() if k != 'decision'}
                        rule.decision = current_rule.get('decision')
                        current_chain.add_rule(rule)
                        rule_id += 1

            return self.ruleset
                        
    def parse_options(self, line, rule_id, current_table):
        """Parse options from a line of the iptables configuration

        Args:
            line (str): The line to parse
            rule_id (int): The rule identifier
            current_table (str): The current table name

        Raises:
            ValueError: If a syntax error is detected

        Returns:
            dict: Parsed rule options
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
                            if option == "-j":
                                if value in ["ACCEPT", "DROP"]:
                                    current_rule['decision'] = value
                                else:
                                    # TODO Modificar para tratar saltos a user_defined tables
                                    pass
                            else:
                                current_rule[option] = match.group()
                                found_match = True
                                continue
                        else:  # Value does not follow regex
                            print(f"Warning: Value '{value}' does not match the expected format for option '{option}' in line: {line}")
                            raise ValueError(f"Syntax Error in line {rule_id}")
                    else:  # Value needed after option
                        print(f"Warning: Option '{option}' requires a value in line: {line}")
                        raise ValueError(f"Syntax Error in line {rule_id}")

            if not found_match and option not in ["-A", "-I", "-D", "-R"]:  # Option not recognized or is a Table Op
                print(f"Warning (line {rule_id}): Unrecognized option '{option}' in line: {line}")
                continue

        return current_rule

    def get_rules(self):
        """
        Get all rules in RuleSet

        Returns:
            RuleSet: Set of RuleSet
        """
        return self.ruleset
    
class Parser:
    """
    The Parser class is used to obtain a RuleSet from a given file,
    which has the format of a given ParserStrategy.
    """
    
    def __init__(self, strategy: ParserStrategy):
        """

        Args:
            strategy (ParserStrategy): _description_
        """
        self.strategy = strategy
        
    def set_strategy(self, strategy: ParserStrategy):
        """

        Args:
            strategy (ParserStrategy): _description_
        """
        self.strategy = strategy
        
    def parse(self, file) -> rules.RuleSet:
        """

        Args:
            file (_type_): _description_

        Returns:
            RuleSet: _description_
        """
        return self.strategy.parse(file)
    