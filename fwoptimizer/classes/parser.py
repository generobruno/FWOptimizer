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
    
 
class IpTablesParser(ParserStrategy):
    """
    Parser Specific for IpTables
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
        for table, table_ops in syntaxTable.items():  # Create Dict for each Table
            preprocessed_table[table] = AliasDefaultDict(dict)
            for rule_type, rule_options in table_ops.items():  # Create Dict for each type of op
                preprocessed_table[table][rule_type] = AliasDefaultDict(dict)
                if rule_type in ['Extensions', 'MatchModules']:
                    for module_name, options in rule_options.items():
                        preprocessed_table[table][rule_type][module_name] = AliasDefaultDict(dict)
                        for option_set, regex in options.items():
                            aliases = [alias.strip() for alias in option_set.split('|')]
                            for alias in aliases:  # Assign Value to all aliases
                                preprocessed_table[table][rule_type][module_name][alias] = regex
                                #print(f'{table},{rule_type},{module_name},{alias} = {preprocessed_table[table][rule_type][module_name][alias]}')
                else:   # Basic Operations
                    for option_set in rule_options:  # Create alias and assign values
                        regex = rule_options[option_set]
                        aliases = [alias.strip() for alias in option_set.split('|')]
                        for alias in aliases:  # Assign Value to all aliases
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
            line_num = 0

            for line in file:
                line = line.strip()
                line_num = line_num + 1

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
                    current_rule = self.parse_options(line, line_num, current_table.name)
                    if current_rule:                # Parse Rule
                        rule = rules.Rule(rule_id)
                        rule.predicates = {k: v for k, v in current_rule.items() if k != 'decision'}
                        rule.decision = current_rule.get('decision')
                        current_chain.add_rule(rule)
                        rule_id += 1

            return self.ruleset
                        
    def parse_options(self, line, line_num, current_table):
        """Parse options from a line of the iptables configuration

        Args:
            line (str): The line to parse
            line_num (int): Line number in file
            current_table (str): The current table name

        Raises:
            ValueError: If a syntax error is detected

        Returns:
            dict: Parsed rule options
        """
        current_rule = {}
        match_modules = {}  # Store match modules and their options separately
        extension_options = {}  # Store options for the -j extension

        # Tokenize line (considering quoted strings)
        tokens = re.findall(r'\"[^\"]*\"|\S+', line)

        i = 0
        current_prot = None
        current_extension = None

        while i < len(tokens):
            option = tokens[i]
            value = None

            # Check if the token is an option (starts with '-' or '--')
            if option.startswith('-'):
                # Collect the value which might span multiple tokens
                value_parts = []
                i += 1
                while i < len(tokens) and not tokens[i].startswith('-'):
                    value_parts.append(tokens[i])
                    i += 1
                value = ' '.join(value_parts) if value_parts else None
            else:
                i += 1
                continue

            found_match = False

            # Protocol Handling
            if option in ['-p', '--protocol']:
                current_prot = value
                current_rule[option] = value
                continue

            # Match Module Handling
            if option in ['-m', '--match']:
                current_match_module = value
                match_modules[current_match_module] = {}  # Initialize a new match module entry
                #current_rule[option] = value
                continue

            # Jump to target handling
            if option in ['-j', '--jump']:
                current_extension = value
                current_rule['decision'] = value
                continue

            # Select Appropriate Regex
            regex = None
            if match_modules:
                for match_module in reversed(list(match_modules.keys())):
                    regex = self.syntaxTable[current_table]['MatchModules'].get(match_module, {}).get(option)
                    if regex is not None:
                        break
            if regex is None and current_prot:
                regex = self.syntaxTable[current_table]['MatchModules'].get(current_prot, {}).get(option)
            if regex is None and current_extension:
                regex = self.syntaxTable[current_table]['Extensions'].get(current_extension, {}).get(option)
            if regex is None:
                regex = self.syntaxTable[current_table]['BasicOperations'].get(option)

            # Assign Rule Options
            if regex is not None:
                if regex == "NO_VALUE":  # Options with no value (e.g., --log-ip-options)
                    if current_extension:
                        extension_options[option] = None
                    else:
                        current_rule[option] = None
                    found_match = True
                else:
                    if value is not None:
                        match = re.match(regex, value)
                        if match:
                            if current_extension:  # If it's an extension option
                                extension_options[option] = match.group()
                            else:  # Other options
                                if option == "-j":  # Jump to Target
                                    current_rule['decision'] = value
                                else:
                                    # Check if the option belongs to a match module
                                    if match_modules:
                                        match_modules[current_match_module][option] = match.group()
                                    else:
                                        current_rule[option] = match.group()
                            found_match = True
                        else:  # Value does not follow regex
                            print(f"Warning (line {line_num}): Value '{value}' does not match the expected format for option '{option}' in line: {line}")
                            raise ValueError(f"Syntax Error in line {line_num}")
                    else:  # Value needed after option
                        print(f"Warning (line {line_num}): Option '{option}' requires a value in line: {line}")
                        raise ValueError(f"Syntax Error in line {line_num}")

            if not found_match and option not in ["-A", "-I", "-D", "-R"]:  # Option not recognized or is a Table Op
                print(f"Warning (line {line_num}): Unrecognized option '{option}' in line: {line}")
                raise ValueError(f"Syntax Error in line {line_num}")

        # Merge match module options into the main rule
        for match_module, options in match_modules.items():
            current_rule[f'm_{match_module}'] = options

        # Add extension options to the main rule
        if extension_options:
            current_rule['jump_extensions'] = extension_options

        return current_rule


    def get_rules(self):
        """
        Get all rules in RuleSet

        Returns:
            RuleSet: Set of RuleSet
        """
        return self.ruleset
