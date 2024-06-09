"""
Firewall Decision Diagram (FDD) module
"""

from typing import List
import graphviz

from fwoptimizer.classes.firewall import Field, FieldList
from fwoptimizer.classes.rules import Chain
from fwoptimizer.utils.elementSet import ElementSetRegistry, ElementSet


class Level:
    """
    Represents a level in the node hierarchy.
    """
    def __init__(self, field: Field):
        """
        Create a new Level

        Args:
            field (Field): Field of the Level
        """
        if not isinstance(field, Field):
            raise ValueError("Domain of Level should be of Field Class.")
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
    
    def getField(self):
        """
        Return the field for this level

        Returns:
            Field: The field of this level
        """
        return self._field_


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
    
    def getLevel(self):
        """
        Return the level for this node
        """
        return self._level_
    
    def getName(self):
        """
        Return the name of this node
        """
        return self._name_


class Edge:
    """
    Edge Class
    """
    def __init__(self, node_id, origin: Node, destination: Node, elementSet: ElementSet, **attrs) -> None:
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
        self._elementSet_ = elementSet
        self._markedAny_ = False
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
        return (self._id_ == other.getId() and
                self._origin_ == other.getOrigin() and
                self._destination_ == other.getDestination() and
                self._elementSet_ == other.getElementSet()
                )

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
        return Edge(self._id_, self._origin_, self._destination_, self._elementSet_.replicate(),**self._attributes_)

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
    
    def getElementSet(self):
        """
        Return the elementSet of this Edge

        Returns:
            ElementSet: Edge elementSet
        """
        return self._elementSet_

class FDD:
    """
    Fdd class
    """

    def __init__(self):
        """_summary_
        """
        self._levels_ = []
        # Un diccionario de decisiones, deberíamos ver bien como tratarlo en el futuro
        self._decisions_ = {}

    def genPre(self, fieldList: FieldList, chain: Chain):
        """sumary
        """

        # Primero creamos la lista de niveles del arbol, usando las configuraciones extraidas de la FieldList
        # Lanzamos un Type error si alguno de los tipos especificados para el nivel no es valido (no existe su ElementSet correspondiente)
        for field in fieldList.getFields():

            if field.getType() in ElementSetRegistry.getRegistry():

                self._levels_.append(Level(field))
            
            else:

                raise TypeError()
            
        # Creamos el ultimo nivel, que corresponde a los nodos hoja y equivalen a las decisiones del FDD
        self._levels_.append(Level(Field('Decision', 'Decision')))

        # Creamos un unico nodo root en el primer nivel del arbol.
        root = Node(self._levels_[0].getField().getName(), self._levels_[0])
        root.autoConnect()
        
        # Recorremos la lista de Rules
        for rule in chain.getRules():

            # Creamos una lista de Nodos temporal, que usaremos para conectar los edges en un bucle
            # La lista se inicia con el nodo root
            nodes = [self._levels_[0].getNodes()[0]]

            #Agregamos un nodo por cada nivel, exptuando el primero y el ultimo
            for level in self._levels_[1:-1]:

                newNode = Node(f"{level.getField().getName()}_{rule.getId()}", level)
                newNode.autoConnect()
                nodes.append(newNode)

            # Revisamos la decision de la regla, si ya existe un nodo en el diccionario de decisiones para dicha decision, lo usamos
            # Si no existe, creamos el nodo y lo agregamos tanto al arbol como al diccionario de decisiones
            decision = rule.getDecision()
            if decision in self._decisions_:
                nodes.append(self._decisions_[decision])
            else:
                self._decisions_[decision] = Node(decision, self._levels_[-1])
                self._decisions_[decision].autoConnect()
                nodes.append(self._decisions_[decision])

            # Recorremos la lista temporal de nodos y vamos añadiendo los Edges que los conectan
            for j in range(1, len(nodes)):

                elements = rule.getOption(nodes[j-1].getLevel().getField().getName())
                elementSet = ElementSet.createElementSet(nodes[j-1].getLevel().getField().getType(), [elements])
                newEdge = Edge(rule.getId(), nodes[j-1], nodes[j], elementSet)
                newEdge.autoConnect()



    def printFDD(self, name: str):
        """sumary
        """

        dot = graphviz.Digraph()
            
        for level in self._levels_:

            for node in level.getNodes():

                dot.node(node.getName())    

        for level in self._levels_:

            for node in level.getNodes():

                for edge in node.getOutgoing():

                    dot.edge(edge.getOrigin().getName(), edge.getDestination().getName(), label=str(str(edge.getId()) + str(edge.getElementSet().getElementsList())))    

        dot.render(name, format='png', view=False, cleanup=True)



        
            
        


        
