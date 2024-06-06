"""
Firewall Decision Diagram (FDD) module
"""

from classes.firewall import Field

from typing import List
import graphviz

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
        self.name = name        # Name of the Level
        self.field = field      # Domain of the Level
        self.nodes = []         # List of Nodes in the Level
    
    def add_node_to_lvl(self, node: "Node"):
        """
        Add Node to the Level

        Args:
            node (Node): Node to add
        """
        self.nodes.append(node)
                
    def del_node_from_lvl(self, node: "Node"):
        """
        Remove Node from the Level

        Args:
            node (Node): Node to delete
        """
        self.nodes.remove(node)


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
        self.level: Level = level
        self.name: str = name
        self.attributes = attrs if attrs else {}
        self.incoming: List[Edge] = []
        self.outgoing: List[Edge] = []
        
    def __repr__(self) -> str:
        """
        Node __repr__

        Returns:
            str: Node string representation
        """
        return f'{self.name}'

    def autoConnect(self):
        """
        Add Node to its Level list
        """
        self.level.add_node_to_lvl(self)

    def autoDisconnect(self):
        """
        Remove Node from its Level list
        """
        self.level.del_node_from_lvl(self)


class Edge:
    """
    Edge Class
    """
    def __init__(self, origin: Node, destination: Node, id, **attrs) -> None:
        """
        Create a new Edge

        Args:
            origin (Node): Origin Node of the Edge
            destination (Node): Destination Node of the Edge
            id (int): Id of the Edge
            attrs: Edge optional attributes
        """
        self.id: int = id
        self.origin: Node = origin
        self.destination: Node = destination
        self.attributes = attrs if attrs else {}
    
    def __repr__(self) -> str:
        """
        Edge __repr__

        Returns:
            str: Edge string representation
        """
        return f'{self.origin} -> {self.destination}'
    
    def __eq__(self, other: "Edge"):
        """
        Edge __eq__

        Args:
            other (Edge): Edge to compare
        """
        return (self.origin == other.origin and
                self.destination == other.destination and
                self.id == other.id)

    def __hash__(self):
        """
        Edge __hash__
        """
        return hash((self.origin, self.destination, self.id))
        
    def autoConnect(self):
        """
        Connect Edge to its origin and destination Nodes
        """
        if self not in self.origin.outgoing:
            self.origin.outgoing.append(self)
        if self not in self.destination.incoming:
            self.destination.incoming.append(self)

    def autoDisconnect(self):
        """
        Disconnect Edge to its origin and destination Nodes
        """
        if self in self.origin.outgoing:
            self.origin.outgoing.remove(self)
        if self in self.destination.incoming:
            self.destination.incoming.remove(self)

    def replicate(self) -> "Edge":
        """
        Duplicate the Edge and its info

        Returns:
            Edge: Edge to copy
        """
        return Edge(self.origin, self.destination, self.id, **self.attributes)
    
    def setOrigin(self, origin: "Node"):
        """
        Set the Edge origin Node

        Args:
            origin (Node): Origin Node
        """
        self.origin = origin


class FDD:
    """_summary_
    """
    