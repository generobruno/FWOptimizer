"""
Firewall Decision Diagram (FDD) module
"""

from typing import List

from fwoptimizer.classes.firewall import Field

class Level:
    """
    Represents a level in the node hierarchy.
    """
    def __init__(self, name: str, field: Field):
        """
        Create a new Level

        Args:
            name (str): Name of the Level
            field (Field): Field of the Level
        """
        if not isinstance(field, Field):
            raise ValueError("Domain of Level should be of Field Class.")
        self._name_ = name        # Name of the Level
        self._field_ = field      # Domain of the Level
        self._nodes_ = []         # List of Nodes in the Level

    def addNodeToLvl(self, node: "Node"):
        """
        Add Node to the Level

        Args:
            node (Node): Node to add
        """
        self._nodes_.append(node)

    def delNodeFromLvl(self, node: "Node"):
        """
        Remove Node from the Level

        Args:
            node (Node): Node to delete
        """
        self._nodes_.remove(node)

    def getNodes(self):
        """
        Return the list of nodes for this nodes

        Returns:
            List: Nodes for this level
        """
        return self._nodes_


class Node:
    """
    Node Class
    """
    def __init__(self, name: str, level: Level, **attrs):
        """
        Create a new Node. 
        A Node has a name, attributes and Lists of outgoing and incoming
        Edges.
        
        Args:
            name (str): Node Name
            level (Level): Node Level
            attrs: Node optional attributes
        """
        self._level_: Level = level
        self._name_: str = name
        self._attributes_ = attrs if attrs else {}
        self._incoming_: List[Edge] = []
        self._outgoing_: List[Edge] = []

    def __repr__(self) -> str:
        """
        Node __repr__

        Returns:
            str: Node string representation
        """
        return f'{self._name_}'

    def autoConnect(self):
        """
        Add Node to its Level list
        """
        self._level_.addNodeToLvl(self)

    def autoDisconnect(self):
        """
        Remove Node from its Level list
        """
        self._level_.delNodeFromLvl(self)

    def getIncoming(self):
        """
        Return the list of incoming edges
        """
        return self._incoming_

    def getOutgoing(self):
        """
        Return the list of outgoings edges
        """
        return self._outgoing_


class Edge:
    """
    Edge Class
    """
    def __init__(self, origin: Node, destination: Node, node_id, **attrs) -> None:
        """
        Create a new Edge

        Args:
            origin (Node): Origin Node of the Edge
            destination (Node): Destination Node of the Edge
            id (int): Id of the Edge
            attrs: Edge optional attributes
        """
        self._id_: int = node_id
        self._origin_: Node = origin
        self._destination_: Node = destination
        self._attributes_ = attrs if attrs else {}

    def __repr__(self) -> str:
        """
        Edge __repr__

        Returns:
            str: Edge string representation
        """
        return f'{self._origin_} -> {self._destination_}'

    def __eq__(self, other: "Edge"):
        """
        Edge __eq__

        Args:
            other (Edge): Edge to compare
        """
        return (self._origin_ == other.getOrigin() and
                self._destination_ == other.getDestination() and
                self._id_ == other.getId())

    def __hash__(self):
        """
        Edge __hash__
        """
        return hash((self._origin_, self._destination_, self._id_))

    def autoConnect(self):
        """
        Connect Edge to its origin and destination Nodes
        """
        if self not in self._origin_.getOutgoing():
            self._origin_.getOutgoing().append(self)
        if self not in self._destination_.getIncoming():
            self._destination_.getIncoming().append(self)

    def autoDisconnect(self):
        """
        Disconnect Edge to its origin and destination Nodes
        """
        if self in self._origin_.getOutgoing():
            self._origin_.getOutgoing().remove(self)
        if self in self._destination_.getIncoming():
            self._destination_.getIncoming().remove(self)

    def replicate(self) -> "Edge":
        """
        Duplicate the Edge and its info

        Returns:
            Edge: Edge to copy
        """
        return Edge(self._origin_, self._destination_, self._id_, **self._attributes_)

    def setOrigin(self, origin: "Node"):
        """
        Set the Edge origin Node

        Args:
            origin (Node): Origin Node
        """
        self._origin_ = origin

    def getOrigin(self):
        """
        Return the Edge origin node

        Returns:
            Node: Origin Node
        """
        return self._origin_
    
    def getDestination(self):
        """
        Return the Edge destination node

        Returns:
            Node: destination Node
        """
        return self._destination_

    def getId(self):
        """
        Return the id of this Edge

        Returns:
            int: Edge id
        """
        return self._id_

class FDD:
    """_summary_
    """
    
