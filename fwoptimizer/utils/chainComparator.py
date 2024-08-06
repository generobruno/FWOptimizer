
from typing import List

from fwoptimizer.classes.rules import Rule, Chain
from fwoptimizer.classes.firewall import FieldList
from fwoptimizer.utils.elementSet import ElementSet

class ChainComparator:

    def reduceRedundancies(rules: List["ChainComparator.PseudoRule"], fieldList: FieldList) -> None:
        """
        Drop redundant PseudoRules of the 'rules' list.

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

        def __init__(self) -> None:

            self._id = None
            self._decision = None
            self._predicates = {}

        def __repr__(self) -> str:
            """
            Rule __repr__
            
            Returns:
                str: PseudoRule String representation
            """
            return f"PseudoRule {self._id}: {self._predicates} -> {self._decision}"

        def fillFromRule(self, rule: Rule, fieldList: FieldList):

            self._id = rule.getId()
            self._decision = rule.getDecision()
            self._predicates = {}

            for field in fieldList.getFields():
                element_list = rule.getOption(field.getName(), None)
                self._predicates[field.getName()] = ElementSet.createElementSet(field.getType(), element_list if element_list else [])
        
        def setId(self, id):
            self._id = id

        def getId(self):
            return self._id

        def setDecision(self, decision):
            self._decision = decision

        def getDecision(self):
            return self._decision
        
        def setPredicate(self, key, value):
            self._predicates[key] = value

        def getPredicates(self):
            return self._predicates
        
        def replicate(self):
            rep = ChainComparator.PseudoRule()
            rep.setId(self.getId())
            rep.setDecision(self.getDecision())
            for key in self.getPredicates():
                rep.setPredicate(key, self.getPredicates()[key].replicate())
            return rep
        
        def sameFieldValues(self, other: "ChainComparator.PseudoRule"):
            """summary
            """
            for key in self.getPredicates():
                if self.getPredicates()[key] != other.getPredicates()[key]:
                    return False
            return True

        def isNull(self):

            for key in self.getPredicates():
                if self.getPredicates()[key].isEmpty():
                    return True
            return False

        def intersection(self, other: "ChainComparator.PseudoRule", fieldList: FieldList):

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

        def __init__(self) -> None:
            self._name = None
            self._defaultdecision = None
            self._rules = []

        def __repr__(self) -> str:
            """
            Chain __repr__

            Returns:
                str: Chain String representation
            """
            rules_str = "\n".join([str(rule) for rule in self._rules])
            return f"{self._name}:\n{rules_str if rules_str else ''}"
        
        def fillFromChain(self, chain: Chain, fieldList: FieldList):
            self._name = chain.getName()
            self._defaultdecision = chain.getDefaultDecision()
            self._rules = []

            for rule in chain.getRules():
                aux = ChainComparator.PseudoRule()
                aux.fillFromRule(rule, fieldList)
                self._rules.append(aux)

        def addRule(self, rule):
            self._rules.append(rule)

        def getRules(self):
            return self._rules

        def setName(self, name):
            self._name = name
        
        def getName(self):
            return self._name
        
        def setDefaultDecision(self, defaultDecision):
            self._defaultdecision = defaultDecision
        
        def getDefaultDecision(self):
            return self._defaultdecision
        
        def replicate(self):

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
        
        self._fieldList = fieldList
        self._chain1 = None
        self._chain2 = None
        self._effectiveChain1 = None
        self._effectiveChain2 = None
    
    def __repr__(self) -> str:
        
        return f"CHAIN COMPARATOR\n\nORIGINALS\n\n{self._chain1}\n\n{self._chain2}\
                \n\nCONVERTED\n\n{self._effectiveChain1}\n\n{self._effectiveChain2}"
    
    def setFieldList(self, fieldList: FieldList):
        self._fieldList = fieldList
    
    def setChain1FromChain(self, chain1: Chain):
        self._chain1 = ChainComparator.PseudoChain()
        self._chain1.fillFromChain(chain1, self._fieldList)
        self._effectiveChain1 = self._chain1.getEffectiveChain(self._fieldList)

    def setChain2FromChain(self, chain2: Chain):
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