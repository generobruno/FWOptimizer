"""
parser Module
"""

import re
import netaddr as nt
from abc import ABC, abstractmethod
from collections.abc import Iterable
from collections import defaultdict

from fwoptimizer.core import rules
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
                line = line.split('#', 1)[0].strip()  # Ignore comments after a line and strip whitespace
                line_num += 1

                if not line:  # Skip empty lines
                    continue

                if line.startswith('*'):            # Start of Table
                    current_table = rules.Table(line[1:])
                    self._ruleSet.addTable(current_table)
                elif line.startswith(':'):          # Define Chain 
                    chain_name = line.split()[0][1:]
                    current_chain = rules.Chain(chain_name)
                    current_table.addChain(current_chain)
                    current_chain.setDefaultDecision(line.split()[1])
                    rule_id = 0
                elif line == 'COMMIT':              # End of Table
                    current_table = None
                    current_chain = None
                else:
                    if line.startswith('-A'):       # Append Rule to Chain
                        chain_name = line.split()[1]
                        current_chain = current_table[chain_name]
                    current_rule = self._parseOptions(line, line_num, current_table.getName())
                    #print(current_rule)
                    if current_rule:                # Parse Rule
                        rule = rules.Rule(rule_id)
                        # Set rule predicates and filter -m options
                        for k, v in current_rule.items():
                            if k != 'decision' and not k.startswith('-m'):
                                values = v.split(',') if isinstance(v, str) and ',' in v else [v]
                                rule.setPredicate(k, values)
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
                if default_decision: 
                    iptables_save_lines.append(f":{chain.getName()} {default_decision} [0:0]")
                else:
                    iptables_save_lines.append(f":{chain.getName()} - [0:0]")  

                # Add rules in the chain
                for rule in chain.getRules():
                    predicates = rule.getPredicates()
                    protocol_list = predicates.get("Protocol", [None])

                    for protocol in protocol_list:
                        base_rule_parts = [f"-A {chain.getName()}"]
                        
                        # Handle source and destination IPs
                        src_ips = predicates.get("SrcIP", [None])
                        dst_ips = predicates.get("DstIP", [None])

                        # Handle other options
                        other_parts = []
                        for option, value in predicates.items():
                            if option not in ["SrcIP", "DstIP"]:
                                other_parts.extend(self._manageOptions(option, value, protocol))
                        
                        # Generate a rule for each src-dst IP combination
                        for src_ip in src_ips:
                            for dst_ip in dst_ips:
                                rule_parts = base_rule_parts.copy()
                                if src_ip:
                                    rule_parts.extend([f"-s {src_ip}"])
                                if dst_ip:
                                    rule_parts.extend([f"-d {dst_ip}"])
                                # Add other options after IPs
                                rule_parts.extend(other_parts)
                                
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

    def _manageOptions(self, option, value, protocol):
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
                return [f"-p {protocol}"]
        elif option.endswith("Port"):
            if isinstance(value, list) and len(value) > 1:
                ports = ','.join(map(str, value))
                return [f"-m {protocol}", f"-m multiport", f"{iptables_option[2]} {ports}"]
            else:
                port = value[0] if isinstance(value, list) else value
                return [f"-m {protocol}", f"{iptables_option[1]} {port}"]
        elif option.endswith("IP"):
            pass
            #if isinstance(value, list):
            #    return [f"{iptables_option[0]} {ip}" for ip in value]
            #else:
            #    return [f"{iptables_option[0]} {value}"]
        else:
            return [f"{iptables_option[0]} {value}"]
 
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
            
            # Handle set match-set option specifically
            if option == '-m' and i+1 < len(tokens) and tokens[i+1] == 'set':
                # Look for --match-set option
                match_set_index = tokens.index('--match-set') if '--match-set' in tokens else -1
                if match_set_index != -1 and match_set_index + 2 < len(tokens):
                    set_name = tokens[match_set_index + 1]
                    set_direction = tokens[match_set_index + 2]  # 'src' or 'dst'
                    
                    # Convert match-set to SrcIP or DstIP
                    ip_key = 'SrcIP' if set_direction == 'src' else 'DstIP'
                    current_rule[ip_key] = set_name
                    
            # Handle specific range options
            if option in ['--src-range', '--dst-range']:
                # Collect the value
                if i + 1 < len(tokens):
                    value = tokens[i + 1]
                    i += 2
                    # Split the range into start and end
                    try:
                        start_ip, end_ip = value.split('-')
                        ip_range = list(nt.IPRange(start_ip, end_ip))
                        ip_key = 'SrcIP' if option == '--src-range' else 'DstIP'
                        current_rule[ip_key] = ",".join(str(ip) for ip in ip_range)
                    except ValueError:
                        raise ValueError(f"Invalid IP range format '{value}' in line {line_num}")
                else:
                    raise ValueError(f"Missing value for {option} in line {line_num}")
                continue

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
            
            # Remove unnecessary set-related keys
            current_rule.pop('--match-set', None)
            current_rule.pop('--src-range', None)
            current_rule.pop('--dst-range', None)

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
    


class AliasDefaultDict:
    """_summary_
    """

    def __init__(self, default_factory, initial=None):
        """
        Create a new AliasDefaultDictionary

        Args:
            default_factory (_type_): _description_
            initial (list, optional): _description_. Defaults to [].
        """
        if initial is None:
            initial = []
        
        self.aliases = {}
        self.data = {}
        self.factory = default_factory
        
        for aliases, value in initial:
            self[aliases] = value

    @staticmethod
    def distinguishKeys(key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        if isinstance(key, Iterable) and not isinstance(key, str):
            return set(key)
        
        return {key}

    def __getitem__(self, key):
        """_summary_

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        keys = self.distinguishKeys(key)
        if keys & self.aliases.keys():
            return self.data[self.aliases[keys.pop()]]

        value = self.factory()
        self[keys] = value
        return value

    def __setitem__(self, key, value):
        """Sets the value for the given key or keys.

        Args:
            key: A single key or an iterable of keys.
            value: The value to set.

        Returns:
            value: The value that was set.
        """
        keys = self.distinguishKeys(key)
        if keys & self.aliases.keys():
            self.data[self.aliases[keys.pop()]] = value
        else:
            new_key = object()
            self.data[new_key] = value
            for alias in keys:
                self.aliases[alias] = new_key
            return value
        
        return None

    def __repr__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        representation = defaultdict(list)
        for alias, value in self.aliases.items():
            representation[value].append(alias)
        return f"AliasDefaultDict({repr(self.factory)}, {repr([(aliases, self.data[value]) for value, aliases in representation.items()])})"

    def get(self, key, default=None):
        """
        AliasDefaultDict get option value
        """
        keys = self.distinguishKeys(key)
        if keys & self.aliases.keys():
            return self.data[self.aliases[keys.pop()]]
        
        return default

