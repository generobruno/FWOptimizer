"""
rules Module
"""
from fwoptimizer.core.fields import ElementSetRegistry



class Rule:
    """
    The Rule Class represent a given rule in a policy, with its predicates and decision.
    """

    def __init__(self, rule_id: int):
        """
        A Rule has an identificator number, which represents its priority in the
        policy set, a dictionary of predicates of options to values, and a 
        final decision.
        
        Args:
            id (int): Rule identifier or priority (0 = top priority)
        """
        self._id = rule_id
        self._predicates = {}
        self._decision = None
        self._matchingPredicate = {}
        self._resolvingPredicate = {}

    def __repr__(self) -> str:
        """
        Rule __repr__
        
        Returns:
            str: Rule String representation
        """
        return f"Rule {self._id}: {self._predicates} -> {self._decision}"
    
    def setPredicate(self, fieldName, value):
        """sumary
        """
        self._predicates[fieldName] = value

    def setDecision(self, decision):
        """sumary
        """
        self._decision = decision
        
    def getPredicates(self):
        """
        Get all the predicates dictionary

        Returns:
            predicates: Rule predicates
        """
        return self._predicates
    
    def setMatchingPredicate(self, field, values):
        """
        Set the Matching Predicate of the rule

        Args:
            field (Predicate): Option of the rule
            values (ElementSet): Value of the rule
        """
        self._matchingPredicate[field] = values

    def getMatchingPredicate(self, field, default=None):
        """
        Get the Matching Predicate of the rule

        Args:
            field (Predicate): Option of the rule
            default (Any, optional): Default value. Defaults to None.

        Returns:
            Option: Predicate Option
        """
        return self._matchingPredicate.get(field, default)

    def setResolvingPredicate(self, field, values):
        """
        Set the Resolving Predicate of the rule

        Args:
            field (Predicate): Option of the rule
            values (ElementSet): Value of the rule
        """
        self._resolvingPredicate[field] = values

    def getResolvingPredicate(self, field, default=None):
        """
        Get the Resolving Predicate of the rule

        Args:
            field (Predicate): Option of the rule
            default (Any, optional): Default value. Defaults to None.

        Returns:
            Option: Predicate Option
        """
        return self._resolvingPredicate.get(field, default)

    def getOption(self, option, default=None):
        """
        Get a given option value from the rule predicates

        Args:
            option : Option to obtain

        Returns:
            value: Value of the option
        """
        return self._predicates.get(option, default)

    def getDecision(self):
        """
        Get the rule's decision

        Returns:
            decision: Rule's decision
        """
        return self._decision

    def getId(self):
        """
        Get the rule's identifier (priority)

        Returns:
            id: Rule id
        """
        return self._id
    
    def setId(self, new_id):
        """
        Set the new Rule Id

        Args:
            new_id: New Id
        """
        self._id = new_id
    
    def isNone(self, fieldList) -> bool:
        """
        Check whether all predicates of this rule are None.
        
        Returns:
            bool: True if all predicates are None, False otherwise
        """
        for field in fieldList.getFields():
            val = self.getOption(field.getName(), None)
            element_set = ElementSetRegistry.getElementSetClass(field.getType())
            
            if not isinstance(val, element_set) and val is not None:
                val = element_set([val]) if val is not None else element_set([])
            
            if not val.isEmpty():
                return False
            
        return True



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
        self._name = name
        self._rules = []
        self._defaultDecision = None

    def __repr__(self) -> str:
        """
        Chain __repr__

        Returns:
            str: Chain String representation
        """
        rules_str = "\n".join([str(rule) for rule in self._rules])
        return f"{self._name}:\n{rules_str if rules_str else ''}"

    def __getitem__(self, idx) -> Rule:
        """
        Chain __getitem__

        Args:
            idx (int): Rule index

        Returns:
            Rule: Rule in Chain List
        """
        return self._rules[idx]

    def addRule(self, rule: Rule):
        """
        Add a rule to the chain
        
        Args:
            rule (Rule): Rule to add
        """
        self._rules.append(rule)
        
    def setRules(self, rules):
        """
        Set the rules for this chain, replacing existing rules.

        Args:
            rules (list): List of Rule objects to set as rules for this chain.
        """
        self._rules = rules

    def setDefaultDecision(self, decision):
        """
        Set the default decision for this chain.

        Args:
            decision (str): 
        """
        self._defaultDecision = decision

    def getDefaultDecision(self):
        """
        Get the default decision for this chain.

        Returns:
            str: Default decision for this chain 
        """
        return self._defaultDecision

    def getRules(self):
        """
        Return the list of rules for this chain
        
        Returns:
            List<Rule>: list of rules
        """
        return self._rules
    
    def getRuleForId(self, id: int) -> Rule:
        """
        Gets the Rule that owns the given id
        
        Args:
            id: Rule id
            
        Returns:
            The searched rule if exist. None otherwise
        """
        for rule in self._rules:
            if rule.getId() == id:
                return rule
        return None

    def getName(self):
        """
        Get the Chain name

        Returns:
            String: Chain Name
        """
        return self._name
    


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
        self._name = name
        self._chains = {}

    def __repr__(self) -> str:
        """
        Table __repr__

        Returns:
            str: Table String representation
        """
        chains_str = "\n".join([str(chain) for chain in self._chains.values()])
        return f"{self._name} - {chains_str}"

    def __getitem__(self, chain_name) -> Chain:
        """
        Table __getitem__

        Args:
            chain_name (str): Chain Name

        Returns:
            Chain: Chain in List
        """
        return self._chains[chain_name]

    def addChain(self, chain: Chain):
        """
        Add a chain to the table
        
        Args:
            chain (Chain): Chain to add
        """
        self._chains[chain.getName()] = chain
    
    def getChains(self):
        """
        Get all chains in table

        Returns:
            Chain: Chains in Table
        """
        return self._chains
    
    def getName(self):
        """
        Get the table name

        Returns:
            String: Table Name
        """
        return self._name



class RuleSet:
    """
    A RuleSet represents the complete list of rules from a given policy.
    """

    def __init__(self) -> None:
        """
        A RuleSet has a dictionary of Tables, of Table.name to Table object
        """
        self._tables = {}

    def __repr__(self) -> str:
        """
        RuleSet __repr__

        Returns:
            str: RuleSet representation
        """
        return f"RuleSet: {self._tables}"

    def __str__(self) -> str:
        """
        RuleSet __str__

        Returns:
            str: RuleSet string representation
        """
        tables_str = "\n".join([str(table) for table in self._tables.values()])
        return f"Rule Set:\n{tables_str}"

    def __getitem__(self, table_name) -> Table:
        """
        RuleSet __getitem__

        Args:
            table_name (str): Table Name

        Returns:
            Table: Table in Tables dict
        """
        return self._tables[table_name]

    def __len__(self) -> int:
        """
        Returns the total number of rules across all tables and chains.
        
        Returns:
            int: Total number of rules
        """
        total_rules = 0
        for table in self._tables.values():
            for chain in table.getChains().values():
                total_rules += len(chain.getRules())
        return total_rules

    def numberOfChains(self) -> int:
        """
        Returns the total number of chains across all tables in the ruleset.
        
        Returns:
            int: Total number of chains
        """
        total_chains = sum(len(table.getChains()) for table in self._tables.values())
        return total_chains

    def addTable(self, table: Table):
        """
        Add a table to the ruleset
        
        Args:
            table (Table): Table to add
        """
        self._tables[table.getName()] = table
        
    def getTables(self):
        """
        Get the RuleSet Tables

        Returns:
            Dict: Dictionary of tables 
        """
        return self._tables

    def printAll(self):
        """
        Print all rules in RuleSet
        """
        for table_name, table in self._tables.items():
            print(f"Table: {table_name}")
            for chain_name, chain in table.getChains().items():
                print(f"Chain: {chain_name}")
                for rule in chain.getRules():
                    print(f"\t{rule}")
