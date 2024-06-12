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
        self._load_ : int = 0
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
        
    def addIncoming(self, incoming: "Edge"):
        """
        Add edge to the incoming incidence of the
        Node

        Args:
            incoming (Edge): Edge to add
        """
        self._incoming_.append(incoming)
        
    def addOutgoing(self, outgoing: "Edge"):
        """
        Add edge to the outgoing incidence of the
        Node

        Args:
            outgoinging (Edge): Edge to add
        """
        self._outgoing_.append(outgoing)

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
    
    def getAttributes(self, attr_name=None):
        """
        Return the Node attributes or a specific attribute if specified

        Args:
            attr_name (str, optional): The name of the attribute to get. 
                                       Defaults to None.

        Returns:
            dict or any: The Node attributes or the value of the specified attribute.
        """
        if attr_name is None:
            return self._attributes_
        else:
            return self._attributes_.get(attr_name, None)
        
    def getLoad(self):
        """
        Get The Node's Load

        Returns:
            load (int): Node's Load
        """
        return self._load_
    
    def setLoad(self, load:int):
        """
        Set the Node' Load

        Args:
            load (int): New Node's Load
        """
        self._load_ = load
    
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
        self._load_ = 0 #TODO Revisar, quizas no hace falta markedAny, ya que un arco marcado tiene load = 1
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
    
    def markEdge(self, mark:bool=True):
        """
        Set Edge Marked attribute

        Args:
            mark (bool, optional): Value to set the Marked attribute. Defaults to True.
        """
        self._markedAny_ = mark
        
    def getMarking(self):
        """
        Get Edge Marking

        Returns:
            markedAny (bool): Marking of the Edge
        """
        return self._markedAny_

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
    
    def setDestination(self, destination: "Node"):
        """
        Set the Edge destination Node

        Args:
            destination (Node): Destination Node
        """
        self._destination_ = destination
    
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
    
    def getAttributes(self, attr_name=None):
        """
        Return the Edge attributes or a specific attribute if specified

        Args:
            attr_name (str, optional): The name of the attribute to get. 
                                       Defaults to None.

        Returns:
            dict or any: The Edge attributes or the value of the specified attribute.
        """
        if attr_name is None:
            return self._attributes_
        else:
            return self._attributes_.get(attr_name, None)
        
    def setAttributes(self, **new_attrs):
        """
        Update the Node attributes with new values.

        Args:
            new_attrs: New attributes to update.
        """
        self._attributes_.update(new_attrs)
    
    def getElementSet(self):
        """
        Return the elementSet of this Edge

        Returns:
            ElementSet: Edge elementSet
        """
        return self._elementSet_
    
    def setElementSet(self, elementSet: ElementSet):
        """
        Set the Edge's ElementSet

        Args:
            elementSet (ElementSet): New ElementSet
        """
        self._elementSet_ = elementSet

class FDD:
    """
    Fdd class
    """

    def __init__(self, levels=None):
        """_summary_
        """
        self._levels_ = levels if levels else []
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
                    
                    origin_name = edge.getOrigin().getName()
                    destination_name = edge.getDestination().getName()
                    label = f"{edge.getId()},{edge.getElementSet().getElementsList()}"
                    edge_attributes = edge.getAttributes()
                    
                    # Include the additional attributes in the label if needed
                    dot.edge(origin_name, destination_name, label=label, _attributes=edge_attributes)
                    
        print(f'\n{dot}')

        dot.render(name, format='png', view=False, cleanup=True)


    def reduction(self):
        """
        Reduce the FDD by applying the 3 reductions:
            1. If there is a node v that has only one outgoing edge e, assuming e points to node
            v', then remove both node v and edge e, and let all the edges that point to v point
            to v'.
            2. If there are two nodes v and v' that are isomorphic, then remove v' together with
            all its outgoing edges, and let all the edges that point to v point to v'
            3. If there are two edges e and e' that both are between the same pair of nodes, then
            remove e' and change the label of e from I(e) to I(e) U I(e').
            
        An FDD f is reduced if it satisﬁes all of the following three conditions:
            1. No node in f has only one outgoing edge.
            2. No two nodes in f are isomorphic.
            3. No two nodes have more than one edge between them.
        """
        changed = True
        while changed:
            changed = False
            changed |= self._removeSimpleNodes()
            changed |= self._removeIsomorphicNodes()
            changed |= self._mergeEdges()
            
    def _removeSimpleNodes(self):
        """
        Apply the first reduction rule:
        If there is a node v that has only one outgoing edge e, assuming e points to node
        v', then remove both node v and edge e, and let all the edges that point to v point
        to v'.
        """
        changed = False
        for level in self._levels_:
            nodes_to_remove = []
            for node_v in level.getNodes():
                v_out = node_v.getOutgoing()
                if len(v_out) == 1:  # Simple Node
                    print(f"REMOVING SIMPLE NODE {node_v}")
                    e = v_out[0]    # Get the edge
                    v_prime = e.getDestination()
                    incoming_edges = list(node_v.getIncoming())  # Make a copy of the list to iterate safely
                    
                    for incoming_edge in incoming_edges:
                        # All edges now point to Node v'
                        incoming_edge.autoDisconnect()
                        incoming_edge.setDestination(v_prime)
                        print(f'\tAdding {incoming_edge} to incoming edges of {v_prime}')
                        print(f'\t\tEdge {incoming_edge} label: {incoming_edge.getElementSet().getElements()}')
                        incoming_edge.autoConnect() 
                    
                    # Mark Node v for removal
                    nodes_to_remove.append(node_v)
                    print(f'\tMarked {node_v} for removal from {level.getField().getName()} Level')
                    changed = True
            
            # Remove all marked nodes after iteration
            for node in nodes_to_remove:
                node.autoDisconnect()
                print(f'\tRemoved Simple node {node} from {level.getField().getName()} Level')
        
        return changed
            
    def _removeIsomorphicNodes(self):
        """
        Apply the second reduction rule:
        If there are two nodes v and v' that are isomorphic, then remove v' along with all 
        its outgoing edges, and make all edges that pointed to v' now point to v.
        """
        changed = False
        for level in self._levels_:
            nodes_to_remove = []
            
            # Convert nodes list to a temporary list to avoid modification issues
            nodes = list(level.getNodes())
            
            # Check consecutive Nodes using indices
            for i in range(len(nodes)):
                node_v = nodes[i]
                for j in range(i + 1, len(nodes)):
                    node_v_prime = nodes[j]
                    # Check if Nodes are Isomorphic
                    if self._areIsomorphic(node_v, node_v_prime):
                        print(f'\tREMOVING ISOMORPHIC NODES {node_v} - {node_v_prime}')
                        
                        # v_prime Edges now point to v
                        print(f'\t{node_v_prime} Edges now point to {node_v}:')
                        for incoming_edge in node_v_prime.getIncoming():
                            incoming_edge.setDestination(node_v)
                            print(f'\tUpdated Edge {incoming_edge}')
                            incoming_edge.autoConnect()
                        
                        # Remove v_prime's outgoing incidence #TODO REVISAR SI HACERLO ACA O FUERA DEL LOOP
                        for edge in node_v_prime.getIncoming():
                            edge.autoDisconnect()
                        
                        # Mark node_v_prime for removal
                        nodes_to_remove.append(node_v_prime)
                        changed = True
            
            # Remove all marked nodes after iteration
            for node in nodes_to_remove:
                if node in level.getNodes():
                    node.autoDisconnect()
                    print(f'Removed Isomorphic node {node} from {level.getField().getName()} Level')
        
        return changed
        
    def _mergeEdges(self):
        """
        Apply the third reduction rule:
        If there are two edges e and e' that both are between the same pair of nodes, then
        remove e' and change the label of e from I(e) to I(e) U I(e').
        """
        changed = False
        for level in self._levels_:
            for node in level.getNodes():
                seen_edges = {}
                for edge in node.getOutgoing():
                    # Pair of nodes
                    key = (edge.getOrigin(), edge.getDestination())
                    if key in seen_edges:
                        seen_edge = seen_edges[key]
                        # Merge element sets
                        print(f'MERGING edges {seen_edge} and {edge}: '
                              f'{seen_edge.getElementSet().getElements()} U {edge.getElementSet().getElements()}')
                        seen_edge.setElementSet(seen_edge.getElementSet().unionSet(edge.getElementSet()))
                        edge.autoDisconnect()
                        changed = True
                    else:
                        seen_edges[key] = edge
        return changed
        
    def _areIsomorphic(self, node_a: Node, node_b: Node) -> bool:
        """
        Check if two Nodes are isomorphic.
        
        Two nodes v and v' in an FDD are isomorphic if and only if
        v and v' satisfy one of the following two conditions:
            1. Both v and v' are terminal nodes with identical
            labels.
            2. Both v and v' are non-terminal nodes and there is
            a one-to-one correspondence between the outgoing edges 
            of v and the outgoing edges of v' such that every pair 
            of corresponding edges have identical labels and they 
            both point to the same node.

        Args:
            node_a (Node): Node A to compare
            node_b (Node): Node B to compare

        Returns:
            bool: True if both nodes are isomorphic
        """
        print(f'Checking ISOMORPHISM between {node_a} and {node_b}')
        if len(node_a.getOutgoing()) == 0 or len(node_a.getOutgoing()) != len(node_b.getOutgoing()):
            return False
        
        for edge_v in node_a.getOutgoing():
            match = False
            for edge_v_prime in node_b.getOutgoing():
                print(f'\t{edge_v}: {edge_v.getElementSet().getElements()}\n'
                      f'\t{edge_v_prime}: {edge_v_prime.getElementSet().getElements()}')
                if (edge_v.getDestination() == edge_v_prime.getDestination() 
                    and edge_v.getElementSet() == edge_v_prime.getElementSet()): #TODO REVISAR OTRA COSA?
                    match = True
                else:
                    match = False
                    break
            if not match:
                return False
        
        return True
    

    def marking(self):
        """
        Compute the load for each node in the FDD.
            1. Compute the load of each terminal node v in f as follows: load(v) := 1
            2. WHILE 
            there is a node v whose load has not yet been computed, suppose v has k
            out edges e_1, ..., e_k and these edges point to nodes v_1, ..., v_k respectively,
            and the loads of these k nodes have been computed
            DO
                a. Among the k edges e_1, ..., e_k, choose an edge e_j with the largest values
                of (load(e_j) - 1) * load(v_j), and mark edge e_j with "all"
                b. Compute the load of v as follows: load(v) := Sum (from i=1 to i=k) (load(e_i) * load(v_i))
            END
            
        In a Marked version of an FDD exactly one outgoing edge of each non-terminal node is marked "All" (or "Any").
        Since all the edge's labels do not change, the semantics of a marked and a non-marked FDD are the same.
        """
        # Step 1: Initialize the load of each terminal node to 1
        last_level = self._levels_[-1]  # Last Level has terminal Nodes
        for node in last_level.getNodes():
            if not node.getOutgoing():
                node.setLoad(1)

        # Step 2: Compute the load for non-terminal nodes
        changed = True
        while changed:
            changed = False
            for level in self._levels_:
                for node in level.getNodes():
                    if node.getLoad() == 0 and all(dest.getLoad() != 0 for dest in (e.getDestination() for e in node.getOutgoing())):
                        # (a) Select the edge with the largest (load(e_j) - 1) * load(v_j)
                        best_edge = max(node.getOutgoing(), key=lambda e: (self._edgeLoad(e) - 1) * e.getDestination().getLoad())
                        best_edge.markEdge()
                        print(f'Marking Edge {best_edge}')
                        best_edge.setAttributes(color='blue')

                        # (b) Compute the load of v
                        node_load = sum(self._edgeLoad(e) * e.getDestination().getLoad() for e in node.getOutgoing())
                        node.setLoad(node_load)
                        changed = True
                        
    def _edgeLoad(self, edge):
        """
        Compute the load of an edge based on its marking and its element set.
        """
        if edge.getMarking():
            return 1
        else:
            return len(edge.getElementSet().getElementsList()) #TODO Revisar si esto esta bien o hay que calcularlo de otra forma

        
            
        


        
