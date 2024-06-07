"""_summary_
"""

from typing import List, Set
from abc import abstractmethod
import netaddr as nt

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



class ElementSet(metaclass = ElementSetRegistry):
    """_summary_
    """

    _domain_ = set()

    @abstractmethod
    def __init__(self, values: List[str]) -> None:
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
    def intersectionSet(self, otherSet: "ElementSet"):
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


class DirSet(ElementSet):
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
        self._elements = nt.IPSet()
        for value in values:
            self._elements.add(value)

    def addSet(self, otherSet: "DirSet") -> None:
        """_summary_

        Args:
            otherSet (DirSet): _description_
        """
        self._elements = self._elements.union(otherSet.getElements())

    def isOverlapping(self, otherSet: "DirSet") -> bool:
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
    
    def intersectionSet(self, otherSet: "DirSet") -> "DirSet":
        """_summary_

        Args:
            otherSet (DirSet): _description_

        Returns:
            DirSet: _description_
        """
        return DirSet([str(x) for x in self._elements.intersection(otherSet.getElements())])
    
    def remove(self, otherSet: "DirSet") -> None:
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
    


class ProtSet(ElementSet):
    """_summary_

    Args:
        ElementSet (_type_): _description_

    Returns:
        _type_: _description_
    """

    _domain_ = {'TCP', 'UDP', 'ICMP'}

    def __init__(self, values: List[str]) -> None:
        """_summary_

        Args:
            values (List[str]): _description_
        """
        self._elements = set(values)

    def addSet(self, otherSet: "ProtSet") -> None:
        """_summary_

        Args:
            otherSet (ProtSet): _description_
        """
        self._elements.update(otherSet.getElements())

    def isOverlapping(self, otherSet: "ProtSet") -> bool:
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
    
    def intersectionSet(self, otherSet: "ProtSet") -> "ProtSet":
        """_summary_

        Args:
            otherSet (ProtSet): _description_

        Returns:
            ProtSet: _description_
        """
        return ProtSet([str(x) for x in self._elements & otherSet.getElements()])
    
    def remove(self, otherSet: "ProtSet") -> None:
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
