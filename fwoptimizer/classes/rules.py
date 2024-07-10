"""
rules Module
"""
from fwoptimizer.utils.elementSet import ElementSetRegistry

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
        
    def getEffectivePart(self, rules, field_list):
        """
        Compute the effective part of this rule based on the previous rules.
        
        Args:
            rules (list[Rule]): List of rules with higher priority
            field_list (FieldList): List of fields in the rule
        
        Returns:
            Rule: The effective part of this rule
        """
        # Find the index of the current rule in all_rules
        current_rule_index = next(i for i, rule in enumerate(rules) if rule._id == self._id)

        # If this is rule 0, return the rule itself
        if current_rule_index == 0:
            return self  
        
        Ri_redundant = set()
        Ri_shadowed = set()
        Ri_effective = {self}

        #for field in field_list.getFields():
        #    field_name = field.getName()
        #    element_set_class = ElementSetRegistry.getElementSetClass(field.getType())
        #    # Set Ri sub-rules 
        #    for eff_rule in Ri_effective:
        #        eff_rule.setPredicate(field_name, element_set_class([]))
                
        # Iterate over all previous rules
        for j in range(current_rule_index):
            print(f'Rule {current_rule_index} vs {j}')
            Rj = rules[j]
            intersection = self._intersection(Rj, self, field_list)
            if Rj.getDecision() == "ACCEPT":  # Assuming positive rules have ACCEPT decision
                Ri_redundant.add(intersection)
                print(f'\tRedundant part: {Ri_redundant}\n')
            else:
                Ri_shadowed.add(intersection)
                print(f'\tShadowed part: {Ri_shadowed}\n')

        # Calculate the effective part
        print(f'Rule {current_rule_index} Sub-Rules:')
        print('Redundant Part:\n' + '\n'.join(str(r) for r in Ri_redundant))
        print('Shadowed Part:\n' + '\n'.join(str(r) for r in Ri_shadowed))
        print()
        
        # Calculate the effective part
        Ri_effective_1 = self.subtractList(Ri_effective, Ri_redundant, field_list)
        print()
        Ri_effective_2 = self.subtractList(Ri_effective, Ri_shadowed, field_list)
        
        print('AAAAAAAAAAAAAAAAA')
        print(Ri_effective_1)
        print()
        print(Ri_effective_2)
        
        for eff_rule in Ri_effective:
            eff_rule.setDecision(self.getDecision())
        
        return Ri_effective
    
    def _union_set(self, rule_set, field_list):
        if not rule_set:
            return None
        
        result = next(iter(rule_set))
        for rule in list(rule_set)[1:]:
            result = self._union(result, rule, field_list)
        return result
        
    def subtractList(self, rules_set, rules_list, field_list):
        """
        Subtract each rule in rules_list from each rule in rules_set.
        
        Args:
            rules_set (set[Rule]): The set of rules to subtract from
            rules_list (set[Rule]): The set of rules to subtract
            field_list (FieldList): List of fields in the rule
        
        Returns:
            set[Rule]: The resulting set of rules after subtraction
        """
        result_set = set()
        for rule in rules_set:
            temp_rule = rule
            for r in rules_list:
                res = self.subtract(temp_rule, r, field_list)
                if res is not None:
                    result_set.add(res)
                print(f'\tIntermediate Result: {result_set}')
            
        print(f'\tResult: {result_set}')
        for rule in result_set:
            for pred in rule.getPredicates().values():
                print(f'\t{list(pred.getElements().iter_ipranges())}')
        
        return result_set

    def _union(self, rule1, rule2, field_list):
        """
        Compute the union of two rules.
        """
        result = Rule(self._id)
        print("Geting Union")
        for field in field_list.getFields():
            field_name = field.getName()
            element_set = ElementSetRegistry.getElementSetClass(field.getType())
            field_dom = element_set.getDomain()
            
            option1 = rule1.getOption(field_name, element_set([]))
            option2 = rule2.getOption(field_name, element_set([]))
            
            # Ensure both options are ElementSet instances #TODO MEJORAR
            if not isinstance(option1, element_set):
                option1 = element_set([option1]) if option1 is not None else element_set([])
            if not isinstance(option2, element_set):
                option2 = element_set([option2]) if option2 is not None else element_set([])
                
            print(f'{field.getName()}: {option1} ∪ {option2} = ')
            
            result.setPredicate(field_name, option1.unionSet(option2))
            
            print(f'{option1}')
            
        return result

    def _intersection(self, rule1, rule2, field_list):
        """
        Compute the intersection of two rules.
        """
        result = Rule(self._id)
        print("Geting Intersection")
        for field in field_list.getFields():
            field_name = field.getName()
            element_set = ElementSetRegistry.getElementSetClass(field.getType())
            field_dom = element_set.getDomain()
            
            option1 = rule1.getOption(field_name, field_dom)
            option2 = rule2.getOption(field_name, field_dom)
            
            # Cast to ElementSet if not already the domain #TODO MEJORAR
            if str(option1) != str(field_dom) and not isinstance(option1, element_set):
                option1 = element_set([option1])
            if str(option2) != str(field_dom) and not isinstance(option2, element_set):
                option2 = element_set([option2])
                
            print(f'{field.getName()}: {option1} ∩ {option2} = {option1.intersectionSet(option2)}')
            
            result.setPredicate(field_name, option1.intersectionSet(option2))
        
        return result

    def subtract(self, rule1, rule2, field_list):
        """
        Compute the difference between two rules (rule1 - rule2).
        """
        if rule2 is None:
            return rule1
        
        result = Rule(self._id)
        print(f"Getting Subtraction")
        for field in field_list.getFields():
            field_name = field.getName()
            if field_name != 'SrcIP': #TODO SACAR
                continue
            element_set = ElementSetRegistry.getElementSetClass(field.getType())
            field_dom = element_set.getDomain()
            
            option1 = rule1.getOption(field_name, field_dom)
            option2 = rule2.getOption(field_name, field_dom)
            
            # Ensure both options are ElementSet instances #TODO MEJORAR
            if not isinstance(option1, element_set):
                option1 = element_set([option1]) if option1 is not None else element_set([])
            if not isinstance(option2, element_set):
                option2 = element_set([option2]) if option2 is not None else element_set([])
                
            print(f'{field.getName()}: {option1} - {option2} = ')
            option1.remove(option2)

            result.setPredicate(field_name, option1)
            
            if isinstance(option1, ElementSetRegistry.getElementSetClass('DirSet')):
                print(f'{list(option1.getElements().iter_ipranges())}')
            else:
                print(f'{option1}')
              
        print(f'RESULT: {result}\n')
        if len(option1.getElements()) == 0:
            return None
        
        return result
    
    def isNone(self) -> bool:
        """
        Check whether all predicates of this rule are None.
        
        Returns:
            bool: True if all predicates are None, False otherwise
        """
        for predicate in self.getPredicates().values():
            if predicate is not None and predicate != []:
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

    def getName(self):
        """
        Get the Chain name

        Returns:
            String: Chain Name
        """
        return self._name
    
    def simplifyRules(self):
        """
        Simplify the set of rules in the chain.
        """
        simplified_rules = []
        for rule in self._rules:
            predicates = rule.getPredicates()
            decision = rule.getDecision()
            new_rules = [rule]
            
            # Identify if any predicate set has multiple non-overlapping ranges
            for field, value in predicates.items():
                elements_list = value.getElementsList()
                # Split mutliple values
                temp_rules = []
                for subrange in elements_list:
                    for r in new_rules:
                        new_rule = Rule(r.getId())
                        new_rule.setDecision(decision)
                        
                        for k, v in r.getPredicates().items():
                            if k == field:
                                new_rule.setPredicate(k, subrange)
                            else:
                                new_rule.setPredicate(k, v)
                        
                        temp_rules.append(new_rule)
                new_rules = temp_rules
                    
            simplified_rules.extend(new_rules)
        
        # Replace the original rules with the simplified rules
        self.setRules(simplified_rules)
        
        # Fix Rules Ids after removal
        for idx, rule in enumerate(self._rules):
            rule.setId(idx)

    def isEquivalent(self, otherChain: "Chain", fieldList):
        """
        Check whether 2 chains are equivalent.

        Args:
            otherChain (Chain): Other chain to check
            fieldList (FieldList): List of Rule Fields

        Returns:
            equivalence: True if the tables are equivalent
            diff_rules_1, diff_rules_2: Rules that conflict between tables
            diff_1, diff_2: Packets permited by one of the tables only
        """
        # Boolean for equivalence
        equivalence = True
        # Opposite Rules
        diff_rules_1 = []
        diff_rules_2 = []
        # Packets permitted by one chain
        diff_1 = []
        diff_2 = []

        print('Getting Effective Parts\n')

        # Get Chain effective rules
        chain_1_eff = []        
        for ri in self._rules:
            print(f'Getting effective part of {ri}')
            ri_effective = ri.getEffectivePart(self._rules, fieldList)
            print(f'\t{ri_effective}')
            chain_1_eff.append(ri_effective)
            
        print()
        
        # Get other chain effective rules
        otherRules = otherChain.getRules()
        chain_2_eff = []
        for Ri in otherRules:
            print(f'Getting effective part of {Ri}')
            Ri_effective = Ri.getEffectivePart(otherRules, fieldList)
            print(f'\t{Ri_effective}')
            chain_2_eff.append(Ri_effective)
        
        print('\nComparing Chains...\n')
               
        for ri_eff in chain_1_eff:
            temp_ri_eff = ri_eff
            for Ri_eff in chain_2_eff:
                print(f'Comparing {ri_eff} to {Ri_eff}')
                temp_ri_eff = temp_ri_eff.subtract(ri_eff, Ri_eff, fieldList)
                print(f'\t{temp_ri_eff}')
            if not temp_ri_eff.isNone():
                equivalence = False
                # Add ri to the list
                diff_rules_1.append(self[temp_ri_eff.getId()])
                # Diff_1 U temp_ri_eff
                diff_1.append(temp_ri_eff) #TODO REVISAR
                
        print()
                
        for Ri_eff in chain_2_eff:
            temp_Ri_eff = Ri_eff
            for ri_eff in chain_1_eff:
                print(f'Comparing {Ri_eff} to {ri_eff}')
                temp_Ri_eff = temp_Ri_eff.subtract(Ri_eff, ri_eff, fieldList)
                print(f'\t{temp_Ri_eff}')
            if not temp_Ri_eff.isNone(): 
                equivalence = False
                # Add ri to the list
                diff_rules_2.append(otherChain[temp_Ri_eff.getId()])
                # Diff_1 U temp_ri_eff
                diff_2.append(temp_Ri_eff) #TODO REVISAR
                
        print('\nDone.\n')
        
        return equivalence, diff_rules_1, diff_rules_2, diff_1, diff_2

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
