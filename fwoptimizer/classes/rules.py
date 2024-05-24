"""_summary_
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
        return self.predicates.get(option, None) #TODO Revisar si devolver "Any" aca o en otro lado
    
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
        self.name = name
        self.rules = []
        
    def __repr__(self) -> str:
        """
        Chain __repr__

        Returns:
            str: Chain String representation
        """
        return "Chain {}: {}".format(self.name, self.rules)

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
        self.name = name
        self.chains = []
        
    def __repr__(self) -> str:
        """
        Table __repr__

        Returns:
            str: Table String representation
        """
        return "Table {}: {}".format(self.name, self.chains)

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
        self.tables = []
        
    def __repr__(self) -> str:
        """
        RuleSet __repr__

        Returns:
            str: RuleSet String representation
        """
        return "RuleSet: {}".format(self.tables)
        
    def add_table(self, table: Table):
        """
        Add a table to the ruleset
        
        Args:
            table (Table): Table to add
        """
        self.tables[table.name] = table


class RuleFactory:
    """_summary_
    """
    
    def __init__(self):
        """_summary_
        """
        self.next_rule_id = 1

    def create_rule(self, parsed_rule):
        """_summary_

        Args:
            parsed_rule (_type_): _description_

        Returns:
            _type_: _description_
        """
        rule = Rule(self.next_rule_id)
        self.next_rule_id += 1

        
        for option, value in parsed_rule.items():
            if option == "-j":
                if value in ["ACCEPT", "DROP"]:
                    rule.decision = value
                else:
                    #TODO Modificar para tratar saltos a user_defined tables
                    pass
            else:
                rule.predicates[option] = value

        return rule

    def create_rules(self, parsed_rules):
        """_summary_

        Args:
            parsed_rules (_type_): _description_

        Returns:
            _type_: _description_
        """
        rules = []
        for parsed_rule in parsed_rules:
            rule = self.create_rule(parsed_rule)
            rules.append(rule)
        return rules