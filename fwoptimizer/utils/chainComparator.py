
from typing import List

from fwoptimizer.core.rules import Rule, Chain
from fwoptimizer.core.firewall import FieldList
from fwoptimizer.utils.elementSet import ElementSet

class ChainComparator:

    def reduceRedundancies(rules: List["ChainComparator.PseudoRule"], fieldList: FieldList) -> None:
        """
        Drop redundant PseudoRules of the 'rules' list.
        The way to detect redundancies is to see if any of the rules is equal to the intersection between both.

        Args:
            rules: The list of PseudoRules to be reduced.
            fieldList: The fieldlist that determines the fields that will be compared
        """

        i = 0
        while i < len(rules)-1:

            intersection = rules[i].intersection(rules[i+1], fieldList)

            if intersection != None:

                if intersection.sameFieldValues(rules[i]):
                    rules.pop(i)
                elif intersection.sameFieldValues(rules[i+1]):
                    rules.pop(i+1)
                else:
                    i += 1

            else:
                i += 1

    class PseudoRule:
        """
        It is a class similar to Rule, but its predicates are objects instead of strings. 
        Allows compare PseudoRules with each other.
        """

        def __init__(self) -> None:
            """
            PseudoRule __init__.
            """

            self._id = None
            self._decision = None
            self._predicates = {}

        def __repr__(self) -> str:
            """
            PseudoRule __repr__.
            
            Returns:
                str: PseudoRule String representation
            """
            return f"PseudoRule {self._id}: {self._predicates} -> {self._decision}"

        def fillFromRule(self, rule: Rule, fieldList: FieldList):
            """
            Add to the PseudoRule the fields set in the fieldList, based on the values of the given rule.
            
            Args:
                rule: Rule from which to take the values.
                fieldList: The fieldlist that determines the fields that will be added.
            """
            self._id = rule.getId()
            self._decision = rule.getDecision()
            self._predicates = {}

            for field in fieldList.getFields():
                element_list = rule.getOption(field.getName(), None)
                self._predicates[field.getName()] = ElementSet.createElementSet(field.getType(), element_list if element_list else [])
        
        def setId(self, id) -> None:
            """
            Sets the id of the rule.

            Args:
                id: Id to set.
            """
            self._id = id

        def getId(self) -> int:
            """
            Gets the id of the rule.

            Returns:
                int: The id of the rule.
            """
            return self._id

        def setDecision(self, decision: str) -> None:
            """
            Sets the decision of the rule.

            Args:
                decision: Decision to set.
            """
            self._decision = decision

        def getDecision(self) -> str:
            """
            Gets the decision of the rule.

            Returns:
                str: The decision of the rule.
            """
            return self._decision
        
        def setPredicate(self, key, value) -> None:
            """
            Sets a predicate for the rule.

            Args:
                key: name of the predicate
                value: ElementSet that represent the value for the predicate.
            """
            self._predicates[key] = value

        def getPredicates(self) -> dict:
            """
            Gets the dict of predicates for the rule.

            Returns:
                A Dict containing the predicates for the rule
            """
            return self._predicates
        
        def replicate(self) -> "ChainComparator.PseudoRule":
            """
            Gets a replica of this object.

            Returns:
                PseudoRule: A replica of this object.
            """
            rep = ChainComparator.PseudoRule()
            rep.setId(self.getId())
            rep.setDecision(self.getDecision())
            for key in self.getPredicates():
                rep.setPredicate(key, self.getPredicates()[key].replicate())
            return rep
        
        def sameFieldValues(self, other: "ChainComparator.PseudoRule") -> bool:
            """
            Check if the 'other' PseudoRule have the same values for the predicates in self.
            Do not check if 'other' have more predicates.

            Args:
                other: PseudoRule to compare.

            Returns:
                True if self and other have the same values. False otherwise.
            """
            for key in self.getPredicates():
                if self.getPredicates()[key] != other.getPredicates()[key]:
                    return False
            return True

        def isNull(self) -> bool:
            """
            Check if this PseudoRule is Null.
            This condition occurs when one of the elementSet does not contain any value.         
            
            Returns:
                True if self is Null. False otherwise.
            """
            for key in self.getPredicates():
                if self.getPredicates()[key].isEmpty():
                    return True
            return False

        def intersection(self, other: "ChainComparator.PseudoRule", fieldList: FieldList) -> "ChainComparator.PseudoRule":
            """
            Gets a new PseudoRule contains the intersection beetwen self and other.

            Args:
                other: The PseudoRule to compare.
                fieldList: The fieldlist that determines the fields that will be compared.

            Returns:
                PseudoRule with intersection beetwen the rules if exist. None otherwise.
            """
            result = ChainComparator.PseudoRule()

            for field in fieldList.getFields():
                
                option1 = self.getPredicates().get(field.getName())
                option2 = other.getPredicates().get(field.getName())

                intersection = option1.intersectionSet(option2)

                result.setPredicate(field.getName(), intersection)
            
            if result.isNull():
                return None
            return result

        def difference(self, other: "ChainComparator.PseudoRule", fieldList: FieldList) -> List["ChainComparator.PseudoRule"]:
            """
            Gets a list of rules whose union represents the difference set between the two sets.
            For two Rules with N fields A = [A1, A2, ..., AN] and B = [B1, B2, ..., BN] their substraction will be:
            A - B = [A1-B1, A2, ..., AN] U [A1, A2-B2, ..., AN] U [A1, A2, ..., AN-BN]
            This method reduces the number of resulting rules by eliminating duplicate rules or those that are a subset of another rule.

            Args:
                other: The PseudoRule to substract.
                fieldList: The fieldlist that determines the fields that will be compared.

            Returns:
                List of PseudoRules that determine the difference set.
            """
                
            diff = []

            for field in fieldList.getFields():

                fDiff = self.getPredicates()[field.getName()].differenceSet(other.getPredicates()[field.getName()])
                if not fDiff.isEmpty():
                    # Replicate the rule
                    rule = self.replicate()
                    # Change the current predicate
                    rule.setPredicate(field.getName(), fDiff)
                    diff.append(rule)

            # Drop redundant rules from the list
            ChainComparator.reduceRedundancies(diff, fieldList)

            return diff
    
    class PseudoChain:
        """
        It is a class similar to Chain, but its rules are PseudoRules. 
        """

        def __init__(self) -> None:
            """
            PseudoChain __init__.
            """
            self._name = None
            self._defaultdecision = None
            self._rules = []

        def __repr__(self) -> str:
            """
            PseudoChain __repr__.

            Returns:
                str: PseudoChain String representation
            """
            rules_str = "\n".join([str(rule) for rule in self._rules])
            return f"{self._name}:\n{rules_str if rules_str else ''}"
        
        def fillFromChain(self, chain: Chain, fieldList: FieldList) -> None:
            """
            Add to the PseudoChain the PseudoRules set in the fieldList, based on the Rules of the given chain.
            
            Args:
                chain: Chain from which to take the values.
                fieldList: The fieldlist that determines the fields that will be added toi PseudoRules.
            """
            self._name = chain.getName()
            self._defaultdecision = chain.getDefaultDecision()
            self._rules = []

            for rule in chain.getRules():
                aux = ChainComparator.PseudoRule()
                aux.fillFromRule(rule, fieldList)
                self._rules.append(aux)

        def addRule(self, rule: "ChainComparator.PseudoRule") -> None:
            """
            Add the given PseudoRule to list of Rules.

            Args:
                rule: PseudoRule to add.
            """
            self._rules.append(rule)

        def getRules(self) -> List["ChainComparator.PseudoRule"]:
            """
            Gets the list of rules of the chain.
            
            Returns:
                List of PseudoRules.
            """
            return self._rules

        def setName(self, name) -> None:
            """
            Sets the name of the chain.

            Args:
                name: Name to set.
            """
            self._name = name
        
        def getName(self):
            """
            Gets the nome of the chain.
            
            Returns:
                str: Name of the chain.
            """
            return self._name
        
        def setDefaultDecision(self, defaultDecision) -> None:
            """
            Sets the default decision for the chain.
            
            Args:
                defaultDecision: Decision to set.
            """
            self._defaultdecision = defaultDecision
        
        def getDefaultDecision(self) -> str:
            """
            Gets the default decision for the chain.
            
            Returns:
                The default  decision for the chain.
            """
            return self._defaultdecision
        
        def replicate(self) -> "ChainComparator.PseudoChain":
            """
            Gets a replica of this object.

            Returns:
                PseudoChain: A replica of this object.
            """
            rep = ChainComparator.PseudoChain()
            rep.setName(self.getName())
            rep.setDefaultDecision(self.getDefaultDecision())
            for rule in self.getRules():
                rep.addRule(rule.replicate())
            return rep
        
        def getEffectiveChain(self, fieldList: FieldList) -> "ChainComparator.PseudoChain":
            """
            Gets the effective PseudoChain from the current PseudoChain.

            Args:
                fieldList: The fieldlist that determines the fields that will be compared.

            Returns:
                The effective PseudoChain.
            """

            if self.getDefaultDecision() != "DROP":
                raise ValueError(f"La cadena tiene Default decision {self.getDefaultDecision()} y por el momento solo se pueden comparar cadenas con default decision DROP")

            newChain = ChainComparator.PseudoChain()
            newChain.setDefaultDecision(self.getDefaultDecision())
            newChain.setName(f"effective-{self.getName()}")

            rules = self.getRules()

            # Iterate over the list of rules from 0 to N-1
            for i in range(len(rules)):

                print(f"\ni: {i}")
                print(rules[i].getDecision())

                # If the decision is ACCEPT, look for the effective part of the rule
                if rules[i].getDecision() == "ACCEPT":

                    # Due to the difference can be more than one rule, will use a list to iterate its
                    # The first value is the i rule. Then, it will be replace for the list of rules resulting of i-j.
                    # As j progresses, resRules store the previous i-j result. 
                    resRules = [rules[i]]

                    # For each rule i, iterate through the previous rules from 0 to i-1 
                    for j in range(i):

                        print(f"\nj: {j}")
                        print(f"resRules: {resRules}")

                        # Here store the results for the current i-j that replace resRules later 
                        resRules2 = []

                        # For each rule in resRules (previous i-j) gets the difference with the current j rule
                        for k in range(len(resRules)):

                            print(f"\nk: {k}")

                            diff = resRules[k].difference(rules[j], fieldList)

                            print(f"restando A-B\nA: {resRules[k]}\nB: {rules[j]}")
                            print(f"diff: {diff}")

                            if diff != None:

                                resRules2 += diff

                        ChainComparator.reduceRedundancies(resRules2, fieldList)

                        # Store the new i-j list of resulting rules for the next iteration
                        resRules = resRules2

                    # Add the resulting list of rules to the effective chain
                    for rule in resRules:

                        print(f"Agregando a newChain: {rule}")
                        newChain.addRule(rule)
                
            return newChain


    def __init__(self, fieldList: FieldList) -> None:
        """
        ChainComparator __init__.
        """
        
        self._fieldList = fieldList
        self._chain1 = None
        self._chain2 = None
        self._effectiveChain1 = None
        self._effectiveChain2 = None
    
    def __repr__(self) -> str:
        """
        ChainComparator __repr__.

        Returns:
            str: ChainComparator String representation
        """
        return f"CHAIN COMPARATOR\n\nORIGINALS\n\n{self._chain1}\n\n{self._chain2}\
                \n\nCONVERTED\n\n{self._effectiveChain1}\n\n{self._effectiveChain2}"
    
    def setFieldList(self, fieldList: FieldList) -> None:
        """
        Set the FieldList used for ChainComparator operations.
        
        Args:
            fieldList: FieldList to use.
        """
        self._fieldList = fieldList
    
    def setChain1FromChain(self, chain1: Chain) -> None:
        """
        Sets the chain1 PseudoChain from the given chain values.
        Gets and save his effective form as well.
        
        Args:
            chain: Chain to use for generate if correspondient PseudoChain. 
        """
        self._chain1 = ChainComparator.PseudoChain()
        self._chain1.fillFromChain(chain1, self._fieldList)
        self._effectiveChain1 = self._chain1.getEffectiveChain(self._fieldList)

    def setChain2FromChain(self, chain2: Chain):
        """
        Sets the chain2 PseudoChain from the given chain values.
        Gets and save his effective form as well.
        
        Args:
            chain: Chain to use for generate if correspondient PseudoChain. 
        """
        self._chain2 = ChainComparator.PseudoChain()
        self._chain2.fillFromChain(chain2, self._fieldList)
        self._effectiveChain2 = self._chain2.getEffectiveChain(self._fieldList)

    def areEquivalents(self):
        """
        Compare the two effective chains saved into CainComparator to see if they are equivalent.

        Returns:
            True if are equivalent. False otherwise.
        """

        if self._effectiveChain1 and self._effectiveChain2:

            #Compare 1 against 2.

            for rule1 in self._effectiveChain1.getRules():

                # Due to the difference can be more than one rule, will use a list to iterate its
                # The first value is the first rule. Then, it will be replace for the list of rules resulting of the difference.
                residual = [rule1]

                for rule2 in self._effectiveChain2.getRules():

                    accum = []

                    for rule in residual:

                        diff = rule.difference(rule2, self._fieldList)

                        if diff != None:

                            accum += diff

                    ChainComparator.reduceRedundancies(accum, self._fieldList)

                    residual = accum

                for result in residual:

                    if not result.isNull():
                        return False

            #Compare 2 against 1

            for rule1 in self._effectiveChain2.getRules():

                # Due to the difference can be more than one rule, will use a list to iterate its
                # The first value is the first rule. Then, it will be replace for the list of rules resulting of the difference.
                residual = [rule1]

                for rule2 in self._effectiveChain1.getRules():

                    accum = []

                    for rule in residual:

                        diff = rule.difference(rule2, self._fieldList)

                        if diff != None:

                            accum += diff

                    ChainComparator.reduceRedundancies(accum, self._fieldList)

                    residual = accum

                for result in residual:

                    if not result.isNull():
                        return False
                    
            # If we do not return false up to here, then it is True

            return True
        
        else:

            raise ValueError("Debe cargar primero dos Chain en ChainComparator")