"""_summary_
"""

from abc import abstractmethod
import netaddr as nt
from typing import List, Set

class ElementSetRegistry(type):

    _REGISTRY_ = {}

    def __new__(cls, name, base, attrs):

        new_cls = type.__new__(cls, name, base, attrs)
        cls._REGISTRY_[new_cls.__name__] = new_cls
        return new_cls
    
    @classmethod
    def getRegistry(cls):
        return cls._REGISTRY_



class ElementSet(metaclass = ElementSetRegistry):
    """_summary_
    """

    _domain_ = set()

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def addSet(self):
        pass

    @abstractmethod
    def isOverlapping(self):
        pass

    @abstractmethod
    def isEmpty(self):
        pass

    @abstractmethod
    def intersectionSet(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def getElements(self):
        pass

    @abstractmethod
    def getElementsList(self):
        pass



class DirSet(ElementSet):

    _domain_ = nt.IPSet(['0.0.0.0/0'])

    def __init__(self, values: List[str]) -> None:
        self._elements = nt.IPSet()
        for value in values:
            self._elements.add(value)

    def addSet(self, otherSet: "DirSet") -> None:
        self._elements = self._elements.union(otherSet.getElements())

    def isOverlapping(self, otherSet: "DirSet") -> bool:
        return not self._elements.isdisjoint(otherSet.getElements())
    
    def isEmpty(self) -> bool:
        return len(self._elements) == 0
    
    def intersectionSet(self, otherSet: "DirSet") -> "DirSet":
        return DirSet([str(x) for x in self._elements.intersection(otherSet.getElements())])
    
    def remove(self, otherSet: "DirSet") -> None:
        self._elements = self._elements.difference(otherSet.getElements())

    def getElements(self) -> nt.IPSet:
        return self._elements
    
    def getElementsList(self) -> List[str]:
        return [str(net) for net in self._elements.iter_cidrs()] 
    


class ProtSet(ElementSet):

    _domain_ = {'TCP', 'UDP', 'ICMP'}

    def __init__(self, values: List[str]) -> None:
        self._elements = set(values)

    def addSet(self, otherSet: "ProtSet") -> None:
        self._elements.update(otherSet.getElements())

    def isOverlapping(self, otherSet: "ProtSet") -> bool:
        return not self._elements.isdisjoint(otherSet.getElements())
    
    def isEmpty(self):
        return len(self._elements) == 0
    
    def intersectionSet(self, otherSet: "ProtSet") -> "ProtSet":
        return ProtSet([str(x) for x in self._elements & otherSet.getElements()])
    
    def remove(self, otherSet: "ProtSet") -> None:
        self._elements = self._elements.difference(otherSet.getElements())

    def getElements(self) -> Set:
        return self._elements
    
    def getElementsList(self):
        return list(self._elements)
