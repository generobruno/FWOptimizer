"""_summary_
"""

from typing import List, Set
from abc import abstractmethod
import netaddr as nt
import portion as p

class ElementSetRegistry(type):
    """_summary_

    Args:
        type (_type_): _description_

    Returns:
        _type_: _description_
    """

    _REGISTRY_ = {}

    def __new__(mcs, name, base, attrs):
        """_summary_

        Args:
            name (_type_): _description_
            base (_type_): _description_
            attrs (_type_): _description_

        Returns:
            _type_: _description_
        """

        new_cls = type.__new__(mcs, name, base, attrs)
        mcs._REGISTRY_[new_cls.__name__] = new_cls
        return new_cls
    
    @classmethod
    def getRegistry(mcs):
        """_summary_

        Returns:
            _type_: _description_
        """
        return mcs._REGISTRY_
    
    @classmethod
    def getElementSetClass(mcs, field_type):
        return mcs._REGISTRY_.get(field_type)


class ElementSet(metaclass = ElementSetRegistry):
    """_summary_
    """

    _domain_ = set()

    @classmethod
    def createElementSet(cls, elementType: str, values: List[str]):
        """
        sumary
        """
        registry = ElementSetRegistry.getRegistry()
        if elementType in registry:
            if values == [None]:
                return registry[elementType](registry[elementType].getDomainList())
            return registry[elementType](values)
        raise TypeError()

    @abstractmethod
    def __init__(self, values: List[str]) -> None:
        """_summary_
        """

    @abstractmethod
    def __eq__(self, value: object) -> bool:
        pass

    @abstractmethod
    def __repr__(self):
        return str(self.getElementsList())
    
    @classmethod
    @abstractmethod
    def getDomainList(cls):
        """_summary_
        """

    @classmethod
    @abstractmethod
    def getDomain(cls):
        """_summary_
        """ 

    @abstractmethod
    def addSet(self, otherSet: "ElementSet"):
        """_summary_
        """

    @abstractmethod
    def isOverlapping(self, otherSet: "ElementSet"):
        """_summary_
        """

    @abstractmethod
    def isEmpty(self):
        """_summary_
        """
    
    @abstractmethod
    def isSubset(self, otherSet: "ElementSet"):
        """_summary_
        """
        
    @abstractmethod
    def isDisjoint(self, otherSet: "ElementSet"):
        """_summary_
        """

    @abstractmethod
    def intersectionSet(self, otherSet: "ElementSet"):
        """_summary_
        """
        
    @abstractmethod
    def unionSet(self, otherSet: "ElementSet"):
        """_summary_
        """

    @abstractmethod
    def remove(self, otherSet: "ElementSet"):
        """_summary_
        """

    @abstractmethod
    def getElements(self):
        """_summary_
        """

    @abstractmethod
    def getElementsList(self):
        """_summary_
        """

    @abstractmethod
    def replicate(self):
        """_summary_
        """



class DirectionSet(ElementSet):
    """_summary_

    Args:
        ElementSet (_type_): _description_

    Returns:
        _type_: _description_
    """

    _domain_ = nt.IPSet(['0.0.0.0/0'])

    def __init__(self, values: List[str]) -> None:
        """_summary_

        Args:
            values (List[str]): _description_
        """
        self._elements = nt.IPSet(values)

    def __eq__(self, other: "DirectionSet") -> bool:
        """
        DirSet __eq__

        Args:
            other (DirSet): DirSet to compare
        """
        return self._elements == other.getElements()
    
    def __repr__(self):
        return 'DirSet' + super().__repr__()
    
    @classmethod
    def getDomainList(cls):
        """
        Get the ElementSet Domain as a list

        Returns:
            Domain: ElementSet Domain
        """
        return [str(net) for net in cls._domain_.iter_cidrs()]
    
    @classmethod
    def getDomain(cls):
        """
        Returns the Domain of the ElementSet as an object

        Returns:
            DirSet: Domain of the set
        """
        return DirectionSet(cls.getDomainList())

    def addSet(self, otherSet: "DirectionSet") -> None:
        """_summary_

        Args:
            otherSet (DirSet): _description_
        """
        self._elements = self._elements.union(otherSet.getElements())

    def isOverlapping(self, otherSet: "DirectionSet") -> bool:
        """_summary_

        Args:
            otherSet (DirSet): _description_

        Returns:
            bool: _description_
        """
        return not self._elements.isdisjoint(otherSet.getElements())
    
    def isEmpty(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        return len(self._elements) == 0
    
    def isSubset(self, otherSet: "DirectionSet") -> bool:
        """
        Checks if a DirSet is a subset of the other set.
        A set is a subset of itself.

        Args:
            otherSet (ElementSet): Other DirSet to compare
        """
        return self._elements.issubset(otherSet.getElements())
    
    def isDisjoint(self, otherSet: "DirectionSet") -> bool:
        """
        Checks if a DirSet is not a subset of the other set.

        Args:
            otherSet (DirSet): Other DirSet to compare
        """
        return self._elements.isdisjoint(otherSet.getElements())
    
    def intersectionSet(self, otherSet: "DirectionSet") -> "DirectionSet":
        """_summary_

        Args:
            otherSet (DirSet): _description_

        Returns:
            DirSet: _description_
        """
        return DirectionSet([str(x) for x in self._elements.intersection(otherSet.getElements()).iter_cidrs()]) #TODO Revisar, le agregue iter_cidrs()
    
    def unionSet(self, otherSet: "DirectionSet") -> "DirectionSet":
        """_summary_

        Args:
            otherSet (ElementSet): _description_

        Returns:
            _type_: _description_
        """
        return DirectionSet([str(x) for x in self._elements.union(otherSet.getElements()).iter_cidrs()])
    
    def remove(self, otherSet: "DirectionSet") -> None:
        """_summary_

        Args:
            otherSet (DirSet): _description_
        """
        self._elements = self._elements.difference(otherSet.getElements())

    def getElements(self) -> nt.IPSet:
        """_summary_

        Returns:
            nt.IPSet: _description_
        """
        return self._elements
    
    def getElementsList(self) -> List[str]:
        """_summary_

        Returns:
            List[str]: _description_
        """
        return [str(net) for net in self._elements.iter_cidrs()] 
    
    def replicate(self):
        """
        Duplicate the DirSet and its info

        Returns:
            DirSet: Copied DirSet
        """
        return DirectionSet(self.getElementsList())
    



class ProtocolSet(ElementSet):
    """_summary_

    Args:
        ElementSet (_type_): _description_

    Returns:
        _type_: _description_
    """

    _domain_ = {'tcp', 'udp', 'icmp'}

    def __init__(self, values: List[str]) -> None:
        """_summary_

        Args:
            values (List[str]): _description_
        """
        # Chequeamos que los valores esten incluidos en el dominio
        lowCaseValues = [x.lower() for x in values]

        for value in lowCaseValues:
            if value not in self._domain_:
                raise ValueError(f"Value {value} isn't include in the domain of {self.__class__.__name__}")
            
        self._elements = set(values)

    def __eq__(self, other: "ProtocolSet") -> bool:
        """
        ProtSet __eq__

        Args:
            other (ProtSet): ProtSet to compare
        """
        return self._elements == other.getElements()
    
    def __repr__(self):
        return 'ProtSet' + super().__repr__()
    
    @classmethod
    def getDomainList(cls):
        """
        Get the ElementSet Domain

        Returns:
            Domain: ElementSet Domain
        """
        return list(cls._domain_)
    
    @classmethod
    def getDomain(cls):
        """
        Returns the Domain of the ElementSet as an object

        Returns:
            ProtSet: Domain of the set
        """
        return ProtocolSet(cls.getDomainList())

    def addSet(self, otherSet: "ProtocolSet") -> None:
        """_summary_

        Args:
            otherSet (ProtSet): _description_
        """
        self._elements.update(otherSet.getElements())

    def isOverlapping(self, otherSet: "ProtocolSet") -> bool:
        """_summary_

        Args:
            otherSet (ProtSet): _description_

        Returns:
            bool: _description_
        """
        return not self._elements.isdisjoint(otherSet.getElements())
    
    def isEmpty(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return len(self._elements) == 0
    
    def isSubset(self, otherSet: "ProtocolSet") -> bool:
        """
        Checks if a ProtSet is a subset of the other set.
        A set is a subset of itself.

        Args:
            otherSet (ProtSet): Other ProtSet to compare
        """
        return self._elements.issubset(otherSet.getElements()) #TODO Revisar si influye en load
    
    def isDisjoint(self, otherSet: "ProtocolSet") -> bool:
        """
        Checks if a ProtSet is not a subset of the other set.

        Args:
            otherSet (ProtSet): Other ProtSet to compare
        """
        return self._elements.isdisjoint(otherSet.getElements())
    
    def intersectionSet(self, otherSet: "ProtocolSet") -> "ProtocolSet":
        """_summary_

        Args:
            otherSet (ProtSet): _description_

        Returns:
            ProtSet: _description_
        """
        return ProtocolSet([str(x) for x in self._elements & otherSet.getElements()])
    
    def unionSet(self, otherSet: "ProtocolSet"):
        """_summary_

        Args:
            otherSet (ProtSet): _description_

        Returns:
            _type_: _description_
        """
        return ProtocolSet([str(x) for x in self._elements | otherSet.getElements()])
    
    def remove(self, otherSet: "ProtocolSet") -> None:
        """_summary_

        Args:
            otherSet (ProtSet): _description_
        """
        self._elements = self._elements.difference(otherSet.getElements())

    def getElements(self) -> Set:
        """_summary_

        Returns:
            Set: _description_
        """
        return self._elements
    
    def getElementsList(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return list(self._elements)
    
    def replicate(self):
        """
        Duplicate the ProtSet and its info

        Returns:
           ProtSet: Copied ProtSet
        """
        return ProtocolSet(self.getElementsList())
    
class PortSet(ElementSet):
    """_summary_
    """
    _domain_ = p.closedopen(0, 65535+1)
    _groupable_ = True

    def __init__(self, values: List[str]) -> None:
        """_summary_
        """

        self._elements = p.empty()

        for value in values:

            try:

                intValue = int(value)

                if intValue not in self._domain_:

                    raise ValueError(f"Value {value} isn't include in the domain of {self.__class__.__name__}")
                
                else:

                    self._elements = self._elements | p.closedopen(intValue, intValue+1)
                
            except:

                ends = value.split(":")
                if len(ends) == 2:

                    interval = p.closedopen(int(ends[0]), int(ends[1])+1)

                    if not self._domain_.contains(interval) :
                        raise ValueError(f"Value {value} isn't include in the domain of {self.__class__.__name__}")
                    else: 
                        self._elements = self._elements | interval

                else:

                    raise ValueError(f"Value {value} isn't include in the domain of {self.__class__.__name__}")

    def __eq__(self, other: "PortSet") -> bool:
        
        return self._elements == other.getElements()

    def __repr__(self):
        return "PortSet" + super().__repr__()
    
    @classmethod
    def _formatedList_(cls, inter: p.Interval):

        formated = []

        for element in p.to_data(inter):
            if element[1] == element[2]-1 and element[0] and not element[3]:
                formated.append(str(element[1]))
            else:

                if element[0]:
                    string = str(element[1])
                else:
                    string = str(element[1]+1) 

                if element[3]:
                    string = string + ":" + str(element[2])
                else:
                    string = string + ":" + str(element[2]-1)

                formated.append(string)
  
        return formated

    @classmethod
    def getDomainList(cls):
        """_summary_
        """
        return cls._formatedList_(cls._domain_)

    @classmethod
    def getDomain(cls):
        """_summary_
        """
        return PortSet(cls.getDomainList())
    
    @classmethod
    def setGroupable(self, value: bool):
        """summary"""
        self._groupable_ = value

    def addSet(self, otherSet: "PortSet"):
        """_summary_
        """
        self._elements = self._elements | otherSet.getElements()

    def isOverlapping(self, otherSet: "PortSet"):
        """_summary_
        """
        return self._elements.overlaps(otherSet.getElements())

    def isEmpty(self):
        """_summary_
        """
        return self._elements.empty
    
    def isSubset(self, otherSet: "PortSet"):
        """_summary_
        """
        return self._elements in otherSet.getElements() #TODO Revisar si influye en load
        
    def isDisjoint(self, otherSet: "PortSet"):
        """_summary_
        """
        return self._elements.intersection(otherSet.getElements()).empty

    def intersectionSet(self, otherSet: "ElementSet"):
        """_summary_
        """
        return PortSet(self._formatedList_(list(self._elements.intersection(otherSet.getElements()))))
        
    def unionSet(self, otherSet: "ElementSet"):
        """_summary_
        """
        return PortSet(self._formatedList_(list(self._elements.union(otherSet.getElements()))))
        
    def remove(self, otherSet: "ElementSet"):
        """_summary_
        """
        self._elements = self._elements.difference(otherSet.getElements())

    def getElements(self):
        """_summary_
        """
        return self._elements

    def getElementsList(self):
        """_summary_
        """
        
        if not self._groupable_:

            noGrouped = []

            for element in p.to_data(self._elements):

                if element[1] == element[2]-1 and element[0] and not element[3]:
                    noGrouped.append(str(element[1]))
                else:
                    for i in range(element[1], element[2]):
                        noGrouped.append(str(i))
            
            return noGrouped
        
        else:   

            return self._formatedList_(self._elements)

    def replicate(self):
        """_summary_
        """
        return PortSet(self.getElementsList())
    
    
