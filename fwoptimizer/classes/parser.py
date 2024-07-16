"""
parser Module
"""

import re
from abc import ABC, abstractmethod

from fwoptimizer.utils.aliasDict import AliasDefaultDict
from fwoptimizer.classes import rules

from fwoptimizer.configs import syntaxes

class ParserStrategy(ABC):
    """
    ParserStrategy interface declares operations common to all supported versions
    of some algorithm.
    
    The Parser Context Class uses this interface to call the algorithm defined by
    Concrete Strategies
    """

    @abstractmethod
    def parse(self, path) -> rules.RuleSet:
        """
        Parse a rule file to obtain a RuleSet

        Args:
            path : File with rules
            
        Returns:
            rules.RuleSet: Set of Rules in the file
        """
        
    @abstractmethod
    def compose(self, ruleSet: rules.RuleSet):
        """
        Parse the RuleSet and obtain a file with rules

        Args:
            ruleSet (rules.RuleSet): Set of Rules

        Returns:
            file: File with rules
        """

class Parser:
    """
    The Parser class is used to obtain a RuleSet from a given file,
    which has the format of a given ParserStrategy.
    """

    def __init__(self, strategy: ParserStrategy):
        """
        Create a new Parser

        Args:
            strategy (ParserStrategy): Parse Strategy
        """
        self._strategy = strategy

    def setStrategy(self, strategy: ParserStrategy):
        """
        Set the parser Strategy

        Args:
            strategy (ParserStrategy): Parse Strategy
        """
        self._strategy = strategy

    def parse(self, path) -> rules.RuleSet:
        """
        Parse File

        Args:
            path: File to parse

        Returns:
            RuleSet: Set of Rules in file
        """
        return self._strategy.parse(path)
    
    def compose(self, ruleSet: rules.RuleSet):
        """
        Parse the RuleSet and obtain a file with rules

        Args:
            ruleSet (rules.RuleSet): Set of Rules

        Returns:
            file: File with rules
        """
        return self._strategy.compose(ruleSet)


class IpTablesParser(ParserStrategy):
    """
    Parser Specific for IpTables
    
    Two tables are necessary to correctly parse the instructions:
        1. Syntax Table: Syntax with information of the options to the format of their values
        2. Fields Format: Relation between options and their corresponding Field Name
    """

    def __init__(self):
        """
        IpTables Parser Strategy
        """
        self._syntaxTable = self._preprocessSyntaxTable(syntaxes.iptables)
        self._ruleSet = rules.RuleSet()

    def parse(self, path):
        """Parse the iptables configuration file

        Args:
            path (str): The path to the file to parse

        Returns:
            RuleSet: Parsed ruleset
        """
        with open(path, 'r', encoding="utf-8") as file:
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
                    self._ruleSet.addTable(current_table)
                elif line.startswith(':'):          # Define Chain #TODO DEFINE CHAIN packet AND byte COUNTERS
                    chain_name = line.split()[0][1:]
                    current_chain = rules.Chain(chain_name)
                    current_table.addChain(current_chain)
                    current_chain.setDefaultDecision(line.split()[1])
                    rule_id = 0 #TODO REVISAR
                elif line == 'COMMIT':              # End of Table
                    current_table = None
                    current_chain = None
                else:
                    if line.startswith('-A'):       # Append Rule to Chain
                        chain_name = line.split()[1]
                        current_chain = current_table[chain_name]
                    current_rule = self._parseOptions(line, line_num, current_table.getName())
                    if current_rule:                # Parse Rule
                        rule = rules.Rule(rule_id)
                        # Set rule predicates and filter -m options
                        [rule.setPredicate(k, v) for k, v in current_rule.items() if k != 'decision' and not k.startswith('-m')] 
                        rule.setDecision(current_rule.get('decision'))
                        current_chain.addRule(rule)
                        rule_id += 1

            return self._ruleSet


    """TODO REVISAR
        1. SrcIP and DstIP: Parece que se puede especificar distintas direcciones simplemente
        por ",". Si no es asi, se puede usar iprange quizas. (para IPs no contiguas, si no usar networks).
        Tambien se puede crear un ipset, pero mejor no definir uno dentro de la herramienta, a menos que 
        ya este definido, en cuyo caso deberia utilizarse.
        2. SrcPort and DstPort: Para multiples puertos se debe usar la opción "-m <protocol>" y despues los
        puertos. Si no son contiguos "--dports a,c,e", si son contiguos "--dports a:e". Creo que "-m multiport"
        es para puertos no contiguos y debe seguir a "-m <protocol>". (y creo que es indistinto dport o dports).
        3. Protocol: Se debe crear una regla distinta para cada protocolo.
    """

    def compose(self, ruleSet: rules.RuleSet):
        """
        Parse the RuleSet and obtain an iptables-save file

        Args:
            ruleSet (rules.RuleSet): Set of Rules

        Returns:
            file: iptables-save file with rules
        """
        iptables_save_lines = []

        for table in ruleSet.getTables().values():
            iptables_save_lines.append(f"*{table.getName()}")

            for chain in table.getChains().values():
                # Add chain with default policy if any
                default_decision = chain.getDefaultDecision()
                if default_decision: #TODO DEFINE CHAIN packet AND byte COUNTERS
                    iptables_save_lines.append(f":{chain.getName()} {default_decision} [0:0]")
                else:
                    iptables_save_lines.append(f":{chain.getName()} - [0:0]")  

                # Add rules in the chain
                for rule in chain.getRules():
                    predicates = rule.getPredicates()
                    protocols = predicates.get("Protocol", None)
                    
                    # Get protocols as a list
                    if protocols:
                        protocol_list = protocols.getElementsList()
                    else:
                        protocol_list = [None]

                    for protocol in protocol_list:
                        rule_parts = [f"-A {chain.getName()}"]
                        for option, value in predicates.items():
                            # Manage each option according to the iptables format
                            self._manageOptions(option, value, rule_parts, protocol)

                        # Form Rule Decision
                        decision = rule.getDecision()
                        if decision:
                            rule_parts.append(f"-j {decision}")

                        iptables_save_lines.append(" ".join(rule_parts))

                # Finish iptables-save
                iptables_save_lines.append("COMMIT")

        return "\n".join(iptables_save_lines)

    def _preprocessSyntaxTable(self, syntax_table):
        """
        Process the syntax table to obtain all the posible alias of the
        different options

        Args:
            syntaxTable (dict): Syntax table for iptables

        Returns:
            dict: Processed syntax table
        """
        preprocessed_table = {}
        for table, table_ops in syntax_table.items():  # Create Dict for each Table
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
                else:   # Basic Operations
                    for option_set in rule_options:  # Create alias and assign values
                        regex = rule_options[option_set]
                        aliases = [alias.strip() for alias in option_set.split('|')]
                        for alias in aliases:  # Assign Value to all aliases
                            preprocessed_table[table][rule_type][alias] = regex
        return preprocessed_table

    def _composeOptions(self, option):
        """
        Get the iptables-save option format, depending on the rule predicate

        Args:
            option (Rule): Rule to compose

        Returns:
            Option: Option with iptables format
        """
        for pattern, field in syntaxes.fields.items():
            if field == option:
                return pattern.split(' | ')  # Return the first iptables option found
        return option  # If no match, return the original option

    def _renameOptions(self, rule):
        """
        Rename rule options based on FieldsFormat mapping.
        
        Args:
            rule (str): Rule to be formated
        
        Returns:
            new_rule (str): Formated Rule
        """
        new_rule = {}
        for key, value in rule.items():
            renamed_key = key
            for pattern, new_key in syntaxes.fields.items():
                if any(option == key for option in pattern.split(' | ')):
                    renamed_key = new_key
                    break
            new_rule[renamed_key] = value
        return new_rule

    def _manageOptions(self, option, value, rule_parts, protocol):
        """
        Format each rule according to the iptables format

        Args:
            option (str): Rule option
            value (str): Option value
            rule_parts (List): List of rules for the iptables-save
            protocol (str): Rule protocol
        """
        # Get Option iptables format
        iptables_option = self._composeOptions(option)
        
        if option.endswith("Protocol"):
            if protocol:
                rule_parts.append(f"{iptables_option[0]} {protocol}")
        elif option.endswith("Port"):
            elements_list = value.getElementsList()
            if len(elements_list) > 1:
                rule_parts.append(f"-m {protocol} -m multiport {iptables_option[2]} {', '.join(map(str, elements_list))}")
            else:
                rule_parts.append(f"-m {protocol} {iptables_option[1]} {', '.join(map(str, elements_list))}") #TODO CAMBIAR A SOLO elements_list
        elif option.endswith("IP"):
            elements_list = value.getElementsList()
            rule_parts.append(f"{iptables_option[0]} {', '.join(map(str, elements_list))}")
        else:
            if hasattr(value, 'getElementsList'):
                elements_list = value.getElementsList()
                rule_parts.append(f"{iptables_option[0]} {', '.join(map(str, elements_list))}")
            else:
                rule_parts.append(f"{iptables_option[0]} {value}")
 
    def _parseOptions(self, line, line_num, current_table):
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
        match_modules = []  # Store match modules
        extension_options = {}  # Store options for the -j extension

        # Tokenize line (considering quoted strings)
        tokens = re.findall(r'\"[^\"]*\"|\S+', line)

        i = 0
        current_prot = None
        current_extension = None
        
        option_handlers = {
            '-p': lambda v: self._handleProtocol(v, current_rule),
            '--protocol': lambda v: self._handleProtocol(v, current_rule),
            '-m': lambda v: self._handleMatchModule(v, match_modules, current_rule),
            '--match': lambda v: self._handleMatchModule(v, match_modules, current_rule),
            '-j': lambda v: self._handleJump(v, current_rule),
            '--jump': lambda v: self._handleJump(v, current_rule),
        }

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

            # Handle Specific Options
            if option in option_handlers:
                option_handlers[option](value)
                current_prot = current_rule.get('-p') or current_rule.get('--protocol')
                current_extension = current_rule.get('decision')
                continue

            # Select Appropriate Regex
            regex = self._getRegex(current_table, match_modules, current_prot, current_extension, option)

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
                                    current_rule[option] = match.group()
                            found_match = True
                        else:  # Value does not follow regex
                            print(
                                f"Warning (line {line_num}): Value '{value}' "
                                f"does not match the expected format for option '{option}' "
                                f"in line: {line}")
                            raise ValueError(f"Syntax Error in line {line_num}")
                    else:  # Value needed after option
                        print(
                            f"Warning (line {line_num}): Option '{option}'" 
                            f"requires a value in line: {line}")
                        raise ValueError(f"Syntax Error in line {line_num}")

            # Option not recognized or is a Table Op
            if not found_match and option not in ["-A", "-I", "-D", "-R"]:
                print(f"Warning (line {line_num}): Unrecognized option '{option}' in line: {line}")
                raise ValueError(f"Syntax Error in line {line_num}")

        # Add extension options to the main rule
        if extension_options:
            current_rule['jump_extensions'] = extension_options

        # Rename rule options based on FieldsFormat
        current_rule = self._renameOptions(current_rule)

        return current_rule

    def _getRegex(self, current_table, match_modules, current_prot, current_extension, option):
        """
        Get the appropiate regex for an option given the rule's semantic

        Args:
            current_table (_type_): _description_
            match_modules (_type_): _description_
            current_prot (_type_): _description_
            current_extension (_type_): _description_
            option (_type_): _description_

        Returns:
            _type_: _description_
        """
        regex = None
        
        if match_modules:
            for match_module in reversed(match_modules):
                regex = self._syntaxTable[current_table]['MatchModules'].get(
                    match_module, {}
                ).get(option)
                if regex is not None:
                    break

        if regex is None and current_prot:
            regex = self._syntaxTable[current_table]['MatchModules'].get(
                current_prot, {}
            ).get(option)

        if regex is None and current_extension:
            regex = self._syntaxTable[current_table]['Extensions'].get(
                current_extension, {}
            ).get(option)

        if regex is None:
            regex = self._syntaxTable[current_table]['BasicOperations'].get(option)
            
        return regex

    def _handleProtocol(self, value, current_rule):
        """
        Handle the protocol Option

        Args:
            value (_type_): _description_
            current_rule (_type_): _description_
        """
        current_rule['-p'] = value

    def _handleMatchModule(self, value, match_modules, current_rule):
        """
        Handle the Match Module Option

        Args:
            value (_type_): _description_
            match_modules (_type_): _description_
            current_rule (_type_): _description_
        """
        match_modules.append(value)
        current_rule[f'-m {value}'] = None

    def _handleJump(self, value, current_rule):
        """
        Handle the Jump Option

        Args:
            value (_type_): _description_
            current_rule (_type_): _description_
        """
        current_rule['decision'] = value

    def getRules(self):
        """
        Get all rules in RuleSet

        Returns:
            RuleSet: Set of RuleSet
        """
        return self._ruleSet
