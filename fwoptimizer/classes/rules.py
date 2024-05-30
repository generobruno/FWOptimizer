"""
rules Module
"""

class Rule:
    """
    The Rule Class represent a given rule in a policy, with its predicates and decision.
    """
    
    def __init__(self, id: int):
        """
        A Rule has an identificator number, which represents its priority in the
        policy set, a dictionary of predicates of options to values, and a 
        final decision.
        
        Args:
            id (int): Rule identifier or priority (0 = top priority)
        """
        self.id = id
        self.predicates = {}
        self.decision = None
        
    def __repr__(self) -> str:
        """
        Rule __repr__
        
        Returns:
            str: Rule String representation
        """
        return "Rule {}: {} -> {}".format(self.id, self.predicates, self.decision)
    
    def get_option(self, option):
        """
        Get a given option value from the rule predicates

        Args:
            option : Option to obtain

        Returns:
            value: Value of the option
        """
        return self.predicates.get(option, None)
    
    def get_decision(self):
        """
        Get the rule's decision

        Returns:
            decision: Rule's decision
        """
        return self.decision
    
    def get_id(self):
        """
        Get the rule's identifier (priority)

        Returns:
            id: Rule id
        """
        return self.id

class Chain:
    """
    A Chain is a collection of Rules.
    """
    
    def __init__(self, name: str) -> None:
        """
        A Chain has a Name and a List of Rules

        Args:
            name (str): Name of the chain
        """
        self.name = name
        self.rules = []
        
    def __repr__(self) -> str:
        """
        Chain __repr__

        Returns:
            str: Chain String representation
        """
        rules_str = "\n".join([str(rule) for rule in self.rules])
        return "{}:\n{}".format(self.name, rules_str if rules_str else "")
    
    def __getitem__(self, idx) -> Rule:
        """
        Chain __getitem__

        Args:
            idx (int): Rule index

        Returns:
            Rule: Rule in Chain List
        """
        return self.rules[idx]

    def add_rule(self, rule: Rule):
        """
        Add a rule to the chain
        
        Args:
            rule (Rule): Rule to add
        """
        self.rules.append(rule)

class Table:
    """
    A Table is a collection of Chains.
    """
    
    def __init__(self, name: str) -> None:
        """
        A Table has a Name and a dict of Chains, of Chain.name to Chain Object

        Args:
            name (str): Table name
        """
        self.name = name
        self.chains = {}
        
    def __repr__(self) -> str:
        """
        Table __repr__

        Returns:
            str: Table String representation
        """
        chains_str = "\n".join([str(chain) for chain in self.chains.values()])
        return "{} - {}".format(self.name, chains_str)
    
    def __getitem__(self, chain_name) -> Chain:
        """
        Table __getitem__

        Args:
            chain_name (str): Chain Name

        Returns:
            Chain: Chain in List
        """
        return self.chains[chain_name]

    def add_chain(self, chain: Chain):
        """
        Add a chain to the table
        
        Args:
            chain (Chain): Chain to add
        """
        self.chains[chain.name] = chain
    
class RuleSet:
    """
    A RuleSet represents the complete list of rules from a given policy.
    """
    
    def __init__(self) -> None:
        """
        A RuleSet has a dictionary of Tables, of Table.name to Table object
        """
        self.tables = {}
        
    def __repr__(self) -> str:
        """
        RuleSet __repr__

        Returns:
            str: RuleSet representation
        """
        return "RuleSet: {}".format(self.tables)
    
    def __str__(self) -> str:
        """
        RuleSet __str__

        Returns:
            str: RuleSet string representation
        """
        tables_str = "\n".join([str(table) for table in self.tables.values()])
        return "Rule Set:\n{}".format(tables_str)
        
    def __getitem__(self, table_name) -> Table:
        """
        RuleSet __getitem__

        Args:
            table_name (str): Table Name

        Returns:
            Table: Table in Tables dict
        """
        return self.tables[table_name]
    
    def __len__(self) -> int:
        """
        Returns the total number of rules across all tables and chains.
        
        Returns:
            int: Total number of rules
        """
        total_rules = 0
        for table in self.tables.values():
            for chain in table.chains.values():
                total_rules += len(chain.rules)
        return total_rules
    
    def number_of_chains(self) -> int:
        """
        Returns the total number of chains across all tables in the ruleset.
        
        Returns:
            int: Total number of chains
        """
        total_chains = sum(len(table.chains) for table in self.tables.values())
        return total_chains
        
    def add_table(self, table: Table):
        """
        Add a table to the ruleset
        
        Args:
            table (Table): Table to add
        """
        self.tables[table.name] = table

    def print_all(self):
        """
        Print all rules in RuleSet
        """
        for table_name, table in self.tables.items():
            print(f"Table: {table_name}")
            for chain_name, chain in table.chains.items():
                print(f"Chain: {chain_name}")
                for rule in chain.rules:
                    print(f"\t{rule}")
