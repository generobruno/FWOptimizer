"""_summary_
"""

class Rule:
    """_summary_
    """
    
    def __init__(self, id):
        """_summary_

        Args:
            id (_type_): _description_
        """
        self.id = id
        self.predicates = {}
        self.decision = None
        
    def __repr__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return "Rule {}: {} -> {}".format(self.id, self.predicates, self.decision)
    
    def get_option(self, option):
        """_summary_

        Args:
            option (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.predicates.get(option, None) #TODO Revisar si devolver "Any" aca o en otro lado
    
    def get_decision(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.decision
    
    def get_id(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.id


class Chain:
    """_summary_
    """
    pass


class Table:
    """_summary_
    """
    pass


class RuleSet:
    """_summary_
    """
    pass


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