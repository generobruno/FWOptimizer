"""
Firewall Decision Diagram (FDD) module
"""

from typing import List
import graphviz

from fwoptimizer.classes.firewall import Field, FieldList
from fwoptimizer.classes.rules import Chain, Rule
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
    def __init__(self, edgeId: List[int], origin: Node, destination: Node, elementSet: ElementSet, **attrs) -> None:
        """
        Create a new Edge

        Args:
            origin (Node): Origin Node of the Edge
            destination (Node): Destination Node of the Edge
            id (int): Id of the Edge
            attrs: Edge optional attributes
        """
        self._id_: List[int] = [] + edgeId
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

    def extendId(self, ids: List[int]):
        """
        Extend the list of ids

        Args:
            ids (List[int]): List of new ids
        """
        self._id_.extend(ids)

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
        Return the ids of this Edge

        Returns:
            List[int]: List of Edge ids
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

    def __init__(self, fieldList: FieldList):
        """_summary_
        """
        self._levels_ = []
        # Un diccionario de decisiones, deberíamos ver bien como tratarlo en el futuro
        self._decisions_ = {}

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

    def genPre(self, chain: Chain):
        """sumary
        """
        
        # Recorremos la lista de Rules
        for rule in chain.getRules():

            # Revisamos que todos los predicados de la regla esten contemplados en la lista de fields
            fields = [level.getField().getName() for level in self._levels_]
            for predicate in rule.getPredicates():
                if predicate not in fields:
                    raise TypeError(f"Predicate {predicate} isn't include in FieldList")

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
                self._decisions_[decision] = Node(decision, self._levels_[-1], shape='box', fontsize='25')
                self._decisions_[decision].autoConnect()
                nodes.append(self._decisions_[decision])

            # Recorremos la lista temporal de nodos y vamos añadiendo los Edges que los conectan
            for j in range(1, len(nodes)):

                elements = rule.getOption(nodes[j-1].getLevel().getField().getName())
                elementSet = ElementSet.createElementSet(nodes[j-1].getLevel().getField().getType(), [elements])
                newEdge = Edge([rule.getId()], nodes[j-1], nodes[j], elementSet)
                newEdge.autoConnect()

    def printFDD(self, name: str):
        """sumary
        """
        dot = graphviz.Digraph()

        # Create a dictionary to hold subgraphs for each field level
        field_subgraphs = {}

        # Iterate through the levels to create subgraphs
        for level in self._levels_:
            field_name = level.getField().getName()  # Get the field name for the level

            if field_name not in field_subgraphs:
                # Create a new subgraph for this field level if it doesn't exist
                field_subgraphs[field_name] = graphviz.Digraph(name=f'cluster_{field_name}')
                field_subgraphs[field_name].attr(label=f"{field_name} Level", style='invis')

            # Add nodes to the corresponding subgraph
            for node in level.getNodes():
                node_name = node.getName()
                field_subgraphs[field_name].node(node_name, _attributes=node.getAttributes())

                # Add edges to the main graph
                for edge in node.getOutgoing():
                    origin_name = edge.getOrigin().getName()
                    destination_name = edge.getDestination().getName()
                    label = f"{edge.getId()},{edge.getElementSet().getElementsList()}" 
                    edge_attributes = edge.getAttributes()
                    dot.edge(origin_name, destination_name, label=label, _attributes=edge_attributes)

        # Add each subgraph to the main graph
        for subgraph in field_subgraphs.values():
            dot.subgraph(subgraph)

        # Render the graph to a file
        dot.render(name, format='png', view=False, cleanup=True)

    def _sanityStep1(self):
        """ Sanitizes all first-level nodes of the FDD, except the last one, as it requires a different treatment. 
        """

        newIndex = 0

        # Recorremos los niveles, a excepcion de los ultimos dos.
        for h in range(len(self._levels_[:-2])):

            level = self._levels_[h]

            # El bucle i recorre todos los nodos de cada nivel
            i = 0
            while i < len(level.getNodes()):

                node = level.getNodes()[i]

                # El bucle j recorre todos los edges de salida de cada nodo
                j = 0
                while j < len(node.getOutgoing()):

                    edge1 = node.getOutgoing()[j]

                    # El bucle k recorre los edges de salida posteriores al edge j para poder compararlos
                    k = j + 1
                    while k < len(node.getOutgoing()):

                        edge2 = node.getOutgoing()[k]

                        # Si hay solapamiento
                        if edge1.getElementSet().isOverlapping(edge2.getElementSet()):

                            # Obtenemos el elementSet interseccion entre los dos edges
                            intersectionSet = edge1.getElementSet().intersectionSet(edge2.getElementSet())

                            # Creamos un nuevo nodo en el nivel
                            newNode = Node(self._levels_[h+1].getField().getName() + " new " + str(newIndex), self._levels_[h+1])
                            newNode.autoConnect()
                            newIndex = newIndex + 1

                            # Creamos un nuevo edge que irá del nodo origen al nuevo nodo, cuyo set es la interseccion de los comparados
                            newEdge = Edge(edge1.getId() + edge2.getId(), edge1.getOrigin(), newNode, intersectionSet)
                            newEdge.autoConnect()

                            # Replicamos todos los arcos salientes del nodo de destino del edge1 en el nuevo nodo
                            for outEdge in edge1.getDestination().getOutgoing():

                                copiedEdge = outEdge.replicate()
                                copiedEdge.setOrigin(newNode)
                                copiedEdge.autoConnect()

                            # Replicamos todos los arcos salientes del nodo de destino del edge2 en el nuevo nodo                            
                            for outEdge in edge2.getDestination().getOutgoing():

                                copiedEdge = outEdge.replicate()
                                copiedEdge.setOrigin(newNode)
                                copiedEdge.autoConnect()

                            # Removemos los elementos de la intesección de ambos arcos
                            edge1.getElementSet().remove(intersectionSet)
                            edge2.getElementSet().remove(intersectionSet)

                            # Revisamos si el edge2 quedó vacío y en ese caso lo desconectamos
                            if edge2.getElementSet().isEmpty():

                                orphanNode = edge2.getDestination()
                                edge2.autoDisconnect()

                                # Si posterior a la desconexion el nodo no tiene otros arcos de entrada, eliminamos todos sus arcos de salida y lo eliminamos
                                if len(orphanNode.getIncoming()) == 0:

                                    while len(orphanNode.getOutgoing()) != 0:

                                        orphanNode.getOutgoing()[0].autoDisconnect()

                                    orphanNode.autoDisconnect()
                            
                            else: 

                                k = k + 1

                        # Si no hay solapamiento avanzamos un edge en el bucle k
                        else: 

                            k = k + 1

                    # Revisamos si el edge1 quedó vacío y en ese caso lo desconectamos
                    if edge1.getElementSet().isEmpty():

                        orphanNode = edge1.getDestination()
                        edge1.autoDisconnect()

                        # Si posterior a la desconexion el nodo no tiene otros arcos de entrada, eliminamos todos sus arcos de salida y lo eliminamos
                        if len(orphanNode.getIncoming()) == 0:

                            while len(orphanNode.getOutgoing()) != 0:

                                orphanNode.getOutgoing()[0].autoDisconnect()

                            orphanNode.autoDisconnect()

                    else:
                        
                        j = j + 1

                i = i + 1
                    

    def _sanityStep2(self):
        """Sanitizes the last-level nodes of the FDD.
        """

        level = self._levels_[-2]
        
        # El bucle i recorre todos los nodos del nivel
        i = 0
        while i < len(level.getNodes()):

            node = level.getNodes()[i]

            # El bucle j recorre todos los edges de salida de cada nodo
            j = 0
            while j < len(node.getOutgoing()):

                edge1 = node.getOutgoing()[j]

                # El bucle k recorre los edges de salida posteriores al edge j para poder compararlos
                k = j + 1
                while k < len(node.getOutgoing()):

                    edge2 = node.getOutgoing()[k]

                    # Si hay solapamiento
                    if edge1.getElementSet().isOverlapping(edge2.getElementSet()):

                        ### A CONTINUACION SE DEBERIA PEDIR RESOLUCION AL USUARIO ###

                        # Si los arcos tienen el mismo destino existe redundancia
                        if edge1.getDestination() == edge2.getDestination():

                            print(f"Detectada redundancia para:\nNode: {node.getName()}\nEdge1: {edge1.getId()}\nEdge2: {edge2.getId()}")

                            edge1.getElementSet().addSet(edge2.getElementSet())
                            edge1.extendId(edge2.getId())
                            edge2.autoDisconnect()

                        #Si los arcos no tienen el mismo destino entonces es una inconsistencia
                        else:

                            print(f"Detectada inconsitencia, resolviendo mediante prioridad para:\nNode: {node.getName()}\nEdge1: {edge1.getId()}\nEdge2: {edge2.getId()}")

                            intersectionSet = edge1.getElementSet().intersectionSet(edge2.getElementSet())

                            # Ordeno las prioridades y selecciono la regla que tiene una prioridad mas alta (valor mas cercano a 0)
                            if sorted(edge1.getId())[0] < sorted(edge2.getId())[0]:

                                edge2.getElementSet().remove(intersectionSet)

                                #Si el edge2 quedó vacio, lo elimino
                                if edge2.getElementSet().isEmpty():

                                    edge2.autoDisconnect()

                            else:
                                
                                edge1.getElementSet().remove(intersectionSet)

                                #Si el edge1 quedó vacio, lo elimino
                                if edge1.getElementSet().isEmpty():

                                    edge1.autoDisconnect()
                                    j = j - 1
                                    break

                    else:

                        k = k + 1
                
                j = j + 1

            i = i + 1


    def sanity(self):
        """Sanitize the FDD.
        """

        self._sanityStep1()
        self._sanityStep2()


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
        
    def firewallGen(self) -> Chain:
        """
        Generate a sequence of rules from the FDD, equivalent to this one,
        and then compact this set of rules.
        
        ---------------------------------------------------------------------------------------------
        
        The first step (FIREWALL GENERATION) is done making a depth-first traversal of 
        the FDD f, such that for each non-terminal node v, the outgoing edge marked 
        "All" (or "Any") of v is traversed after all the other outgoing edges of v have 
        been traversed.
        Whenever a terminal node is encountered, assuming <v_1 e_1 ... v_k e_k v_k+1> is
        the decision path where for every i (1 <= i <= k), e_i is the most recently traversed
        outgoing edge of node v_i, output a rule r as follows:
            
            F_1 ∈ S_1 ∧ ... ∧ F_d ∈ S_d -> F(v_k+1)
            
        Where:  S_i = I(e_j)    if the decision path has a node v_j that 
                                is labeled with field F_i and e_j is not marked
                S_i = D(F_i)    otherwise
        
        For the above rule r, the predicate "F_1 ∈ S_1 ∧ ... ∧ F_d ∈ S_d" is called the
        MATCHING PREDICATE of r.
        The rule represented by the path <v_1 e_1 ... v_k e_k v_k+1> is 
        F_1 ∈ T_1 ∧ ... ∧ F_d ∈ T_d -> F(v_k+1), where:
        
                T_i = I(e_j)    if the decision path has a node v_j that
                                is labeled with field F_i
                T_i = D(F_i)    otherwise
                
        We call the predicate "F_1 ∈ T_1 ∧ ... ∧ F_d ∈ T_d" the RESOLVING PREDICATE of r.
        
        The ith rule output by Algorithm is the ith rule in the ﬁrewall generated. 
        The correctness of this algorithm follows directly from the semantics of FDDs 
        and ﬁrewalls.
        
        ---------------------------------------------------------------------------------------------
        
        The second step (FIREWALL COMPACTION) removes redundant rules from a ﬁrewall
        producing an equivalent ﬁrewall but with fewer rules.
        
        A rule in a ﬁrewall is redundant if removing the rule does not change the semantics
        of the ﬁrewall. 
        
        ---------------------------------------------------------------------------------------------

        Returns:
            Chain: Set of Rules equivalent to the FDD
        """
        #TODO Ver si pasarle el nombre de la chain o setearlo despues? -> Tambien ver si guardar el nombre de la chain original en el fdd para usar este
        chain = Chain("FirewallGenChain")
    
        # We don't mark visited nodes since we need to traverse all paths (rules)
        # There is no risk of divergence since there are no cycles (DAG) 
        def dfs(node, decision_path):
            if not node.getOutgoing():  # Terminal node
                rule = Rule(len(chain.getRules())) #TODO REVISAR CUAL DEBERIA SER EL rule_id
                matching_predicate = {}
                resolving_predicate = {}
    
                for v, e in decision_path:
                    field = v.getLevel().getField().getName()
                    element_set = e.getElementSet() 
    
                    if not e.getMarking():  # Not marked with "all"
                        matching_predicate[field] = element_set.getElements()
                    else:
                        matching_predicate[field] = element_set.getDomain() 
                        
                    resolving_predicate[field] = element_set.getElements() #TODO SACAR?
    
                # Set the predicates and decision for the rule
                for field, values in matching_predicate.items():
                    rule.setPredicate(field, values)
                rule.setDecision(node.getName())
                chain.addRule(rule)
                return
            
            # Separate marked and unmarked edges
            unmarked_edges = [e for e in node.getOutgoing() if not e.getMarking()]
            marked_edges = [e for e in node.getOutgoing() if e.getMarking()]

            # First traverse all unmarked edges
            for edge in unmarked_edges:
                dfs(edge.getDestination(), decision_path + [(node, edge)])
            
            # Then traverse marked edges (should only be one if exists)
            for edge in marked_edges:
                dfs(edge.getDestination(), decision_path + [(node, edge)])
        
        # Step 1: Generate Rules from FDD
        dfs(self._levels_[0].getNodes()[0], []) 
        #return chain

        # Step 2: Compact Rules
        redundant = [False] * len(chain.getRules())

        # Mark redundant rules #TODO Revisar
        n = len(chain.getRules())
        for i in range(n - 1, -1, -1):
            for k in range(i + 1, n):
                if (    not redundant[k] and
                        self._sameDecision(chain[i], chain[k]) and
                        self._implies(chain[i], chain[k])):
                    # Check if rule i is redundant based on rule k
                    is_redundant = True
                    for j in range(i + 1, k):
                        if (    not redundant[j] and
                                not self._sameDecision(chain[i], chain[j]) and
                                not self._mutuallyExclusive(chain[i], chain[j])):
                            is_redundant = False
                            break
                    if is_redundant:
                        redundant[i] = True
                        break

        # Remove redundant rules
        new_rules = [rule for i, rule in enumerate(chain.getRules()) if not redundant[i]]
        chain.setRules(new_rules)
        #TODO ACOMODAR RULE_IDs DESPUES DE ELIMINAR REGLAS REDUNDANTES
        print(f'Removed {n - len(chain.getRules())} REDUNDANT rules from the chain.\n')

        return chain     
    
    def _sameDecision(self, rule1: Rule, rule2: Rule) -> bool:
        """
        Check if two rules have the same decision.
        """
        print(f'Check sameDecision: Rule_{rule1.getId()} & Rule_{rule2.getId()} = {rule1.getDecision() == rule2.getDecision()}')
        return rule1.getDecision() == rule2.getDecision()

    def _implies(self, rule1: Rule, rule2: Rule) -> bool:
        """
        Check if rule1's resolving predicate implies rule2's matching predicate.
        
        'r_i.rp implies r_k.mp' means that for any packet p, if p satisfies 
        r_i.rp, then p satisﬁes r_k.mp. Checking whether r_i.rp implies r_k.mp is simple. 
        Let r_i.rp be F_1 ∈ T_1 ∧ ... ∧ F_d ∈ T_d and let r_k.mp be F_1 ∈ S_1 ∧ ... ∧ F_d ∈ S_d. 
        Then, r_i.rp implies r_k.mp if and only if for every j, where 1 <= j <= d, the condition T_j ⊆ S_j holds.
        """
        fields = set(rule1.getPredicates().keys()).union(rule2.getPredicates().keys())
        for field in fields:
            option1 = rule1.getOption(field, set())
            option2 = rule2.getOption(field, set())
            print(f'Checking predicates {option1} - {option2}: {option1.issubset(option2)}')
            if not option1.issubset(option2):
                return False
        return True
    
    def _mutuallyExclusive(self, rule1, rule2):
        fields = set(rule1.getPredicates().keys()).union(rule2.getPredicates().keys())
        for field in fields:
            option1 = rule1.getOption(field, set())
            option2 = rule2.getOption(field, set())
            print(f'Checking Mutual Exclusion {option1} - {option2}: {option1.isdisjoint(option2)}')
            if not option1.isdisjoint(option2):  # Check if they have no common elements
                return False
        return True

    def _satisfiesBoth(self, rule1: Rule, rule2: Rule) -> bool:
        """
        Check if no packet satisfies both rule1's resolving predicate and rule2's matching predicate.
        """
        for field in rule1.getPredicates():
            print(f'Checking satisfies both {rule2.getPredicates()} AND {rule1.getOption(field).isdisjoint(rule2.getOption(field))} ')
            if field in rule2.getPredicates() and rule1.getOption(field).isdisjoint(rule2.getOption(field)):
                return False
        return True
