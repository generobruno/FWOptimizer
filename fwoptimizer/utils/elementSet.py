"""_summary_
"""

from typing import List, Set
from abc import abstractmethod
import netaddr as nt
import portion as p

class ElementSetRegistry(type):
    """
    A registry of all ElementSet types in the current application.
    Adds all classes that implement it as a metaclass to the registry.
    Used to relate the filtering fields of a firewall to their representation in the FDD.
    """

    _REGISTRY_ = {}

    def __new__(mcs, name, base, attrs):

        new_cls = type.__new__(mcs, name, base, attrs)
        mcs._REGISTRY_[new_cls.__name__] = new_cls
        return new_cls
    
    @classmethod
    def getRegistry(mcs):
        """
        Gets the registry of ElementSet classes.

        Returns:
            Dict: A dictionary with class names as keys and class references as values. 
        """
        return mcs._REGISTRY_
    
    @classmethod
    def getElementSetClass(mcs, className):
        """
        Gets a class reference for a given class name.

        Returns:
            class reference if class name exist. None otherwise.
        """
        return mcs._REGISTRY_.get(className)


class ElementSet(metaclass = ElementSetRegistry):
    """
    An abstract base class for defining sets of elements.

    The `ElementSet` class serves as a blueprint for other specific sets 
    of elements, such as IP_address, ports, etc. Subclasses must implement all 
    abstract methods defined in this class to provide specific behaviors 
    and attributes.

    This class cannot be instantiated directly and should be subclassed 
    by concrete implementations.
    """

    _domain_ = set()

    @classmethod
    def createElementSet(cls, elementType: str, values: List[str]) -> "ElementSet":
        """
        If elementType is the name of a subclas of ElementSet, call te constructor of this class with 'values' as parameter.

        Args:
            elemetnType: Name of the class to instantiate.
            values: List of values for the set.

        Returns:
            A instance of given ElementSet subclass.
        """
        registry = ElementSetRegistry.getRegistry()
        if elementType in registry:
            if values == []:
                return registry[elementType](registry[elementType].getDomainList())
            return registry[elementType](values)
        raise TypeError()

    @abstractmethod
    def __init__(self, values: List[str]) -> None:
        """
        ElementSet __init__.

        Args:
            values (List[str]): A list of strings containing elements for this set.
        """
        pass

    @abstractmethod
    def __eq__(self, other: "ElementSet") -> bool:
        """
        DirectionSet __eq__

        Args:
            other (ElementSet): ElementSet to compare.

        Returns:
            True if self and 'other' are equals. False otherwise.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        ElementSet __repr__
        """
        return str(self.getElementsList())
    
    @classmethod
    @abstractmethod
    def getDomainList(cls) -> List:
        """
        Gets the domain of the element set as a list.

        Returns:
            A list of elements of this set.
        """
        pass

    @classmethod
    @abstractmethod
    def getDomain(cls):
        """
        Get a ElementSet object with the domain of the element set.
        """ 
        pass

    @abstractmethod
    def add(self, otherSet: "ElementSet") -> None:
        """
        Add the elements of otherSet to this set.
        Equivalent to say self = self U otherSet.

        Args:
            otherSet: The ElementSet to add to this.
        """
        pass

    @abstractmethod
    def isOverlapping(self, otherSet: "ElementSet") -> bool:
        """
        Check if this ElementSet and otherSet have common elements.

        Args:
            otherSet: The ElementSet to compare this.

        Returns:
            True if exist common elements. False otherwise.
        """
        pass

    @abstractmethod
    def isEmpty(self) -> bool:
        """
        Check if this ElementSet is Empty.

        Returns:
            True if the set is empty. False otherwise.
        """
        pass
    
    @abstractmethod
    def isSubset(self, otherSet: "ElementSet") -> bool:
        """
        Check if this ElementSet is a subset of 'otherSet'.

        Args:
            otherSet: The ElementSet to compare this.

        Returns:
            True if this ElementSet if a subset of otherSet. False otherwise.
        """
        pass
        
    @abstractmethod
    def isDisjoint(self, otherSet: "ElementSet") -> bool:
        """
        Check if this ElementSet and otherSet have common elements.

        Args:
            otherSet: The ElementSet to compare this.

        Returns:
            True if not exist common elements. False otherwise.
        """
        pass

    @abstractmethod
    def intersectionSet(self, otherSet: "ElementSet") -> "ElementSet":
        """
        Gets a new ElementSet with the intersection between self and 'otherSet'.

        Args:
            otherSet: The ElementSet to compare this.

        Returns:
            ElementSet whit the intersection between self and 'otherSet'. 
        """
        pass
        
    @abstractmethod
    def unionSet(self, otherSet: "ElementSet") -> "ElementSet":
        """
        Gets a new ElementSet with the union between self and 'otherSet'.

        Args:
            otherSet: The ElementSet to compare this.

        Returns:
            ElementSet whit the union between self and 'otherSet'. 
        """
        pass

    @abstractmethod
    def differenceSet(self, otherSet: "ElementSet") -> "ElementSet":
        """
        Gets a new ElementSet with the difference between self and 'otherSet'.

        Args:
            otherSet: The ElementSet to compare this.

        Returns:
            ElementSet whit the difference between self and 'otherSet'. 
        """
        pass

    @abstractmethod
    def remove(self, otherSet: "ElementSet") -> None:
        """
        Remove the elements of otherSet to this set.
        Equivalent to say self = self - (self ∩ otherSet).

        Args:
            otherSet: The ElementSet to remove to this.
        """
        pass

    @abstractmethod
    def getElements(self) -> set:
        """
        Gets the set instance contains in this object.

        Returns:
            The set of elements contain in this object.
        """
        pass

    @abstractmethod
    def getElementsList(self) -> List[str]:
        """
        Gets the elements of this set as a list.

        Returns:
            A list with elements contains in this set.
        """
        pass

    @abstractmethod
    def replicate(self) -> "ElementSet":
        """
        Gets a replica of this object.

        Returns:
            A replica of this object.
        """
        pass



class DirectionSet(ElementSet):
    """
    A subclass of ElementSet used to operate with IP directions.
    """

    _domain_ = nt.IPSet(['0.0.0.0/0'])

    def __init__(self, values: List[str]) -> None:
        """
        DirectionSet __init__.

        Args:
            values (List[str]): A list of strings containing IP directions or IP networks in CIDR notation (0.0.0.0/0).
        """
        self._elements = nt.IPSet(values)

    def __eq__(self, other: "DirectionSet") -> bool:
        """
        DirectionSet __eq__

        Args:
            other (DirectionSet): DirSet to compare

        Returns:
            (bool) True if self and 'other' are equals. False otherwise.
        """
        return self._elements == other.getElements()
    
    def __repr__(self):
        """
        DirectionSet __repr__
        """
        return 'DirectionSet' + super().__repr__()
    
    @classmethod
    def getDomainList(cls) -> List[str]:
        """
        Get the DirectionSet Domain as a list

        Returns:
            List of DirectionSet Domain
        """
        return [str(net) for net in cls._domain_.iter_cidrs()]
    
    @classmethod
    def getDomain(cls) -> "DirectionSet":
        """
        Gets a DirectionSet object with the Domain of DirectionSet

        Returns:
            DirectionSet: Domain of the DirectionSet
        """
        return DirectionSet(cls.getDomainList())

    def add(self, otherSet: "DirectionSet") -> None:
        """
        Add the elements of otherSet to this set.
        Equivalent to say self = self U otherSet.

        Args:
            otherSet: The DirectionSet to add to this.
        """
        self._elements = self._elements.union(otherSet.getElements())

    def isOverlapping(self, otherSet: "DirectionSet") -> bool:
        """
        Check if this DirectionSet and otherSet have common elements.

        Args:
            otherSet: The DirectionSet to compare this.

        Returns:
            (bool) True if exist common elements. False otherwise.
        """
        return not self._elements.isdisjoint(otherSet.getElements())
    
    def isEmpty(self) -> bool:
        """
        Check if this DirectionSet is Empty.

        Returns:
            (bool) True if the set is empty. False otherwise.
        """
        return len(self._elements) == 0
    
    def isSubset(self, otherSet: "DirectionSet") -> bool:
        """
        Check if this DirectionSet is a subset of 'otherSet'.

        Args:
            otherSet: The DirectionSet to compare this.

        Returns:
            (bool) True if this DirectionSet if a subset of otherSet. False otherwise.
        """
        return self._elements.issubset(otherSet.getElements())
    
    def isDisjoint(self, otherSet: "DirectionSet") -> bool:
        """
        Check if this DirectionSet and otherSet have common elements.

        Args:
            otherSet: The DirectionSet to compare this.

        Returns:
            (bool) True if not exist common elements. False otherwise.
        """
        return self._elements.isdisjoint(otherSet.getElements())
    
    def intersectionSet(self, otherSet: "DirectionSet") -> "DirectionSet":
        """
        Gets a new DirectionSet with the intersection between self and 'otherSet'.

        Args:
            otherSet: The DirectionSet to compare this.

        Returns:
            DirectionSet whit the intersection between self and 'otherSet'. 
        """
        return DirectionSet([str(x) for x in self._elements.intersection(otherSet.getElements()).iter_cidrs()])
    
    def unionSet(self, otherSet: "DirectionSet") -> "DirectionSet":
        """
        Gets a new DirectionSet with the union between self and 'otherSet'.

        Args:
            otherSet: The DirectionSet to compare this.

        Returns:
            DirectionSet whit the union between self and 'otherSet'. 
        """
        return DirectionSet([str(x) for x in self._elements.union(otherSet.getElements()).iter_cidrs()]) 

    def differenceSet(self, otherSet: "DirectionSet"):
        """
        Gets a new DirectionSet with the difference between self and 'otherSet'.

        Args:
            otherSet: The DirectionSet to compare this.

        Returns:
            DirectionSet whit the difference between self and 'otherSet'. 
        """
        return DirectionSet([str(x) for x in self._elements.difference(otherSet.getElements()).iter_cidrs()])
    
    def remove(self, otherSet: "DirectionSet") -> None:
        """
        Remove the elements of otherSet to this set.
        Equivalent to say self = self - (self ∩ otherSet).

        Args:
            otherSet: The DirectionSet to remove to this.
        """
        self._elements = self._elements.difference(otherSet.getElements())

    def getElements(self) -> nt.IPSet:
        """
        Gets the set instance contains in this object.

        Returns:
            netaddr.IPSet: The set of elements contain in this object.
        """
        return self._elements
    
    def getElementsList(self) -> List[str]:
        """
        Gets the elements of this set as a list.

        Returns:
            A list with elements contains in this set.
        """
        return [str(net) for net in self._elements.iter_cidrs()] 
    
    def replicate(self) -> "DirectionSet":
        """
        Gets a replica of this object.

        Returns:
            DirectionSet: A replica of this object.
        """
        return DirectionSet(self.getElementsList())
    



class ProtocolSet(ElementSet):
    """
    A subclass of ElementSet used to operate with transport layer protocols.
    """

    _domain_ = {'tcp', 'udp', 'icmp'}

    def __init__(self, values: List[str]) -> None:
        """
        ProtocolSet __init__.

        Args:
            values (List[str]): A list of strings containing transport layer protocols.
        """

        # Check that values are included in the domain
        lowCaseValues = [x.lower() for x in values]

        for value in lowCaseValues:
            if value not in self._domain_:
                raise ValueError(f"Value {value} isn't include in the domain of {self.__class__.__name__}")
            
        self._elements = set(values)

    def __eq__(self, other: "ProtocolSet") -> bool:
        """
        ProtocolSet __eq__

        Args:
            other (ProtocolSet): ProtocolSet to compare

        Returns:
            (bool) True if self and 'other' are equals. False otherwise.
        """
        return self._elements == other.getElements()
    
    def __repr__(self):
        """
        ProtocolSet __repr__
        """
        return 'ProtocolSet' + super().__repr__()
    
    @classmethod
    def getDomainList(cls) -> List[str]:
        """
        Get the ProtocolSet Domain as a list

        Returns:
            List of ProtocolSet Domain
        """
        return list(cls._domain_)
    
    @classmethod
    def getDomain(cls) -> "ProtocolSet":
        """
        Gets a ProtocolSet object with the Domain of ProtocolSet

        Returns:
            ProtocolSet: Domain of the ProtocolSet
        """
        return ProtocolSet(cls.getDomainList())

    def add(self, otherSet: "ProtocolSet") -> None:
        """
        Add the elements of otherSet to this set.
        Equivalent to say self = self U otherSet.

        Args:
            otherSet: The ProtocolSet to add to this.
        """
        self._elements.update(otherSet.getElements())

    def isOverlapping(self, otherSet: "ProtocolSet") -> bool:
        """
        Check if this ProtocolSet and otherSet have common elements.

        Args:
            otherSet: The ProtocolSet to compare this.

        Returns:
            (bool) True if exist common elements. False otherwise.
        """
        return not self._elements.isdisjoint(otherSet.getElements())
    
    def isEmpty(self):
        """
        Check if this ProtocolSet is Empty.

        Returns:
            (bool) True if the set is empty. False otherwise.
        """
        return len(self._elements) == 0
    
    def isSubset(self, otherSet: "ProtocolSet") -> bool:
        """
        Check if this ProtocolSet is a subset of 'otherSet'.

        Args:
            otherSet: The ProtocolSet to compare this.

        Returns:
            (bool) True if this ProtocolSet if a subset of otherSet. False otherwise.
        """
        return self._elements.issubset(otherSet.getElements())
    
    def isDisjoint(self, otherSet: "ProtocolSet") -> bool:
        """
        Check if this ProtocolSet and otherSet have common elements.

        Args:
            otherSet: The ProtocolSet to compare this.

        Returns:
            (bool) True if not exist common elements. False otherwise.
        """
        return self._elements.isdisjoint(otherSet.getElements())
    
    def intersectionSet(self, otherSet: "ProtocolSet") -> "ProtocolSet":
        """
        Gets a new ProtocolSet with the intersection between self and 'otherSet'.

        Args:
            otherSet: The ProtocolSet to compare this.

        Returns:
            ProtocolSet whit the intersection between self and 'otherSet'. 
        """
        return ProtocolSet([str(x) for x in self._elements & otherSet.getElements()])
    
    def unionSet(self, otherSet: "ProtocolSet") -> "ProtocolSet":
        """
        Gets a new ProtocolSet with the union between self and 'otherSet'.

        Args:
            otherSet: The ProtocolSet to compare this.

        Returns:
            ProtocolSet whit the union between self and 'otherSet'. 
        """
        return ProtocolSet([str(x) for x in self._elements | otherSet.getElements()])
    
    def differenceSet(self, otherSet: "ProtocolSet") -> "ProtocolSet":
        """
        Gets a new ProtocolSet with the difference between self and 'otherSet'.

        Args:
            otherSet: The ProtocolSet to compare this.

        Returns:
            ProtocolSet whit the difference between self and 'otherSet'. 
        """
        return ProtocolSet([str(x) for x in self._elements - otherSet.getElements()])
    
    def remove(self, otherSet: "ProtocolSet") -> None:
        """
        Remove the elements of otherSet to this set.
        Equivalent to say self = self - (self ∩ otherSet).

        Args:
            otherSet: The ProtocolSet to remove to this.
        """
        self._elements = self._elements.difference(otherSet.getElements())

    def getElements(self) -> Set:
        """
        Gets the set instance contains in this object.

        Returns:
            set: The set of elements contain in this object.
        """
        return self._elements
    
    def getElementsList(self):
        """
        Gets the elements of this set as a list.

        Returns:
            A list with elements contains in this set.
        """
        return list(self._elements)
    
    def replicate(self):
        """
        Gets a replica of this object.

        Returns:
            ProtocolSet: A replica of this object.
        """
        return ProtocolSet(self.getElementsList())



class PortSet(ElementSet):
    """
    A subclass of ElementSet used to operate with transport layer ports.
    It has a class variable that allows you to indicate whether ports should be grouped by ranges when they are contiguous.
    """
    _domain_ = p.closedopen(0, 65535+1)
    _groupable_ = True

    def __init__(self, values: List[str]) -> None:
        """
        PortSet __init__.

        Args:
            values (List[str]): A list of strings containing port ranges or single ports of the transport layer.
        """

        self._elements = p.empty()

        for value in values:

            # try transform string into integer
            try:

                intValue = int(value)

                if intValue not in self._domain_:

                    raise ValueError(f"Value {value} isn't include in the domain of {self.__class__.__name__}")
                
                else:

                    self._elements = self._elements | p.closedopen(intValue, intValue+1)
                
            # if an error is raised, the value could be a range 
            except:

                # try split the string into two, using ':' as a divisor
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
        """
        PortSet __eq__

        Args:
            other (PortSet): PortSet to compare

        Returns:
            (bool) True if self and 'other' are equals. False otherwise.
        """
        return self._elements == other.getElements()

    def __repr__(self):
        """
        PortSet __repr__
        """
        return "PortSet" + super().__repr__()
    
    @classmethod
    def _formatedList_(cls, inter: p.Interval) -> List[str]:
        """
        Formats a list of the portion library ranges to be suitable for use with firewall rules.

        Args:
            inter: A portion.Interval object to transform into its List[str] useful representation.

        Returns:
            List[str] with a useful representation to this intervals.
        """

        formated = []

        # Because the intervals used by the portion library can be open or closed, we convert to the discrete model.
        # The .to_data() method returns a list of elements where each element is a 4-tuple representing a range. 
        # The tuple contains the values ​​of the endpoints and a boolean flag indicating whether the endpoint is open or closed.
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
    def getDomainList(cls) -> List[str]:
        """
        Get the PortSet Domain as a list

        Returns:
            List of PortSet Domain
        """
        return cls._formatedList_(cls._domain_)

    @classmethod
    def getDomain(cls) -> "PortSet":
        """
        Gets a PortSet object with the Domain of PortSet

        Returns:
            PortSet: Domain of the PortSet
        """
        return PortSet(cls.getDomainList())
    
    @classmethod
    def setGroupable(self, value: bool) -> None:
        """
        Set the value of 'groupable' to 'value'.

        Args:
            value: New bool value for 'groupable'.
        """
        self._groupable_ = value

    def add(self, otherSet: "PortSet") -> None:
        """
        Add the elements of otherSet to this set.
        Equivalent to say self = self U otherSet.

        Args:
            otherSet: The PortSet to add to this.
        """
        self._elements = self._elements | otherSet.getElements()

    def isOverlapping(self, otherSet: "PortSet") -> bool:
        """
        Check if this PortSet and otherSet have common elements.

        Args:
            otherSet: The PortSet to compare this.

        Returns:
            (bool) True if exist common elements. False otherwise.
        """
        return self._elements.overlaps(otherSet.getElements())

    def isEmpty(self) -> bool:
        """
        Check if this PortSet is Empty.

        Returns:
            (bool) True if the set is empty. False otherwise.
        """
        return self._elements.empty
    
    def isSubset(self, otherSet: "PortSet") -> bool:
        """
        Check if this PortSet is a subset of 'otherSet'.

        Args:
            otherSet: The PortSet to compare this.

        Returns:
            (bool) True if this PortSet if a subset of otherSet. False otherwise.
        """
        return self._elements in otherSet.getElements() 
        
    def isDisjoint(self, otherSet: "PortSet") -> bool:
        """
        Check if this PortSet and otherSet have common elements.

        Args:
            otherSet: The PortSet to compare this.

        Returns:
            (bool) True if not exist common elements. False otherwise.
        """
        return self._elements.intersection(otherSet.getElements()).empty

    def intersectionSet(self, otherSet: "PortSet") -> "PortSet":
        """
        Gets a new PortSet with the intersection between self and 'otherSet'.

        Args:
            otherSet: The PortSet to compare this.

        Returns:
            PortSet whit the intersection between self and 'otherSet'. 
        """
        return PortSet(self._formatedList_(list(self._elements.intersection(otherSet.getElements()))))
        
    def unionSet(self, otherSet: "PortSet") -> "PortSet":
        """
        Gets a new PortSet with the union between self and 'otherSet'.

        Args:
            otherSet: The PortSet to compare this.

        Returns:
            PortSet whit the union between self and 'otherSet'. 
        """
        return PortSet(self._formatedList_(list(self._elements.union(otherSet.getElements()))))
        
    def differenceSet(self, otherSet: "PortSet") -> "PortSet":
        """
        Gets a new PortSet with the difference between self and 'otherSet'.

        Args:
            otherSet: The PortSet to compare this.

        Returns:
            PortSet whit the difference between self and 'otherSet'. 
        """
        return PortSet(self._formatedList_(list(self._elements.difference(otherSet.getElements()))))
    
    def remove(self, otherSet: "ElementSet") -> None:
        """
        Remove the elements of otherSet to this set.
        Equivalent to say self = self - (self ∩ otherSet).

        Args:
            otherSet: The PortSet to remove to this.
        """
        self._elements = self._elements.difference(otherSet.getElements())

    def getElements(self):
        """
        Gets the set instance contains in this object.

        Returns:
            set: The set of elements contain in this object.
        """
        return self._elements

    def getElementsList(self):
        """
        Gets the elements of this set as a list.

        Returns:
            A list with elements contains in this set.
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
        """
        Gets a replica of this object.

        Returns:
            PortSet: A replica of this object.
        """
        return PortSet(self.getElementsList())
    
    
