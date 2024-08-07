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
        self._field = field      # Domain of the Level
        self._nodes = []         # List of Nodes in the Level

    def addNodeToLvl(self, node: "Node"):
        """
        Add Node to the Level

        Args:
            node (Node): Node to add
        """
        self._nodes.append(node)

    def delNodeFromLvl(self, node: "Node"):
        """
        Remove Node from the Level

        Args:
            node (Node): Node to delete
        """
        self._nodes.remove(node)

    def getNodes(self):
        """
        Return the list of nodes for this nodes

        Returns:
            List: Nodes for this level
        """
        return self._nodes
    
    def getField(self):
        """
        Return the field for this level

        Returns:
            Field: The field of this level
        """
        return self._field


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
        self._level: Level = level
        self._name: str = name
        self._load : int = 0
        self._attributes = attrs if attrs else {}
        self._incoming: List[Edge] = []
        self._outgoing: List[Edge] = []

    def __repr__(self) -> str:
        """
        Node __repr__

        Returns:
            str: Node string representation
        """
        return f'{self._name}'

    def autoConnect(self):
        """
        Add Node to its Level list
        """
        self._level.addNodeToLvl(self)

    def autoDisconnect(self):
        """
        Remove Node from its Level list
        """
        self._level.delNodeFromLvl(self)
        
    def addIncoming(self, incoming: "Edge"):
        """
        Add edge to the incoming incidence of the
        Node

        Args:
            incoming (Edge): Edge to add
        """
        self._incoming.append(incoming)
        
    def addOutgoing(self, outgoing: "Edge"):
        """
        Add edge to the outgoing incidence of the
        Node

        Args:
            outgoinging (Edge): Edge to add
        """
        self._outgoing.append(outgoing)

    def getIncoming(self):
        """
        Return the list of incoming edges
        """
        return self._incoming

    def getOutgoing(self):
        """
        Return the list of outgoings edges
        """
        return self._outgoing
    
    def getLevel(self):
        """
        Return the level for this node
        """
        return self._level
    
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
            return self._attributes
        return self._attributes.get(attr_name, None)
        
    def getLoad(self):
        """
        Get The Node's Load

        Returns:
            load (int): Node's Load
        """
        return self._load
    
    def setLoad(self, load:int):
        """
        Set the Node' Load

        Args:
            load (int): New Node's Load
        """
        self._load = load
    
    def getName(self):
        """
        Return the name of this node
        """
        return self._name


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
        self._id: List[int] = [] + edgeId
        self._origin: Node = origin
        self._destination: Node = destination
        self._elementSet = elementSet
        self._markedAny = False
        self._load = 0
        self._attributes = attrs if attrs else {}

    def __repr__(self) -> str:
        """
        Edge __repr__

        Returns:
            str: Edge string representation
        """
        return f'{self._origin} -> {self._destination}'

    def __eq__(self, other: "Edge"):
        """
        Edge __eq__

        Args:
            other (Edge): Edge to compare
        """
        return (self._id == other.getId() and
                self._origin == other.getOrigin() and
                self._destination == other.getDestination() and
                self._elementSet == other.getElementSet()
                )

    def __hash__(self):
        """
        Edge __hash__
        """
        return hash((self._origin, self._destination, self._id))

    def autoConnect(self):
        """
        Connect Edge to its origin and destination Nodes
        """
        if self not in self._origin.getOutgoing():
            self._origin.getOutgoing().append(self)
        if self not in self._destination.getIncoming():
            self._destination.getIncoming().append(self)

    def autoDisconnect(self):
        """
        Disconnect Edge to its origin and destination Nodes
        """
        if self in self._origin.getOutgoing():
            self._origin.getOutgoing().remove(self)
        if self in self._destination.getIncoming():
            self._destination.getIncoming().remove(self)

    def replicate(self) -> "Edge":
        """
        Duplicate the Edge and its info

        Returns:
            Edge: Edge to copy
        """
        return Edge(self._id, self._origin, self._destination, self._elementSet.replicate(),**self._attributes)
    
    def markEdge(self, mark:bool=True):
        """
        Set Edge Marked attribute

        Args:
            mark (bool, optional): Value to set the Marked attribute. Defaults to True.
        """
        self._markedAny = mark
        
    def getMarking(self):
        """
        Get Edge Marking

        Returns:
            markedAny (bool): Marking of the Edge
        """
        return self._markedAny

    def setOrigin(self, origin: "Node"):
        """
        Set the Edge origin Node

        Args:
            origin (Node): Origin Node
        """
        self._origin = origin

    def extendId(self, ids: List[int]):
        """
        Extend the list of ids

        Args:
            ids (List[int]): List of new ids
        """
        self._id.extend(ids)

    def getOrigin(self):
        """
        Return the Edge origin node

        Returns:
            Node: Origin Node
        """
        return self._origin
    
    def setDestination(self, destination: "Node"):
        """
        Set the Edge destination Node

        Args:
            destination (Node): Destination Node
        """
        self._destination = destination
    
    def getDestination(self):
        """
        Return the Edge destination node

        Returns:
            Node: destination Node
        """
        return self._destination

    def getId(self):
        """
        Return the ids of this Edge

        Returns:
            List[int]: List of Edge ids
        """
        return self._id
    
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
            return self._attributes
        return self._attributes.get(attr_name, None)
        
    def setAttributes(self, **new_attrs):
        """
        Update the Node attributes with new values.

        Args:
            new_attrs: New attributes to update.
        """
        self._attributes.update(new_attrs)
    
    def getElementSet(self):
        """
        Return the elementSet of this Edge

        Returns:
            ElementSet: Edge elementSet
        """
        return self._elementSet
    
    def setElementSet(self, elementSet: ElementSet):
        """
        Set the Edge's ElementSet

        Args:
            elementSet (ElementSet): New ElementSet
        """
        self._elementSet = elementSet

class FDD:
    """
    Fdd class
    """

    def __init__(self, fieldList: FieldList):
        """_summary_
        """
        # FDD Name
        self._name = "Unnamed_FDD"
        # FDD Levels
        self._levels = []
        # Un diccionario de decisiones, deberíamos ver bien como tratarlo en el futuro
        self._decisions = {}
        # FieldList del FDD
        self._fieldList = fieldList

        # Primero creamos la lista de niveles del arbol, usando las configuraciones extraidas de la FieldList
        # Lanzamos un Type error si alguno de los tipos especificados para el nivel no es valido (no existe su ElementSet correspondiente)
        for field in fieldList.getFields():

            if field.getType() in ElementSetRegistry.getRegistry():

                self._levels.append(Level(field))
            
            else:

                raise TypeError()
            
        # Creamos el ultimo nivel, que corresponde a los nodos hoja y equivalen a las decisiones del FDD
        self._levels.append(Level(Field('Decision', 'Decision')))

        # Creamos un unico nodo root en el primer nivel del arbol.
        root = Node(self._levels[0].getField().getName(), self._levels[0])
        root.autoConnect()


    def _getDecisionNode(self, decision: str):
        """Obtains the node corresponding to this decision if it exists, or adds a new one and returns it
        """
        # Revisamos la decision de la regla, si ya existe un nodo en el diccionario de decisiones para dicha decision, lo usamos
        # Si no existe, creamos el nodo y lo agregamos tanto al arbol como al diccionario de decisiones
        if decision  not in self._decisions:
            self._decisions[decision] = Node(decision, self._levels[-1], shape='box', fontsize='35')
            self._decisions[decision].autoConnect()
        return self._decisions[decision]


    def printFDD(self, name: str, img_format='png', rank_dir='TB', unroll_decisions=False):
        """
        Generate a graph image from the data structure

        Args:
            name (str): Name of the graph
            img_format (str, optional): Output Format. Defaults to 'png'.
        """
        dot = graphviz.Digraph(engine='dot')

        # Create a dictionary to hold subgraphs for each field level
        field_subgraphs = {}
        edge_node_counter = 0 # For intermediate nodes
        
        # Calculate total number of nodes and edges
        total_nodes = sum(len(level.getNodes()) for level in self._levels)
        total_edges = sum(len(node.getOutgoing()) for level in self._levels for node in level.getNodes())

        # Determine node size based on total number of nodes and edges
        base_width = 2.0
        base_height = 0.5
        base_font = 20.0
        total_elements = (total_nodes + total_edges)
        width_factor = 10.0 / total_elements
        height_factor = 5.5 / total_elements
        font_factor = 5.0 / total_elements
        
        if total_nodes < 50:
            ranksep_factor = 2.5
        elif total_nodes < 100:
            ranksep_factor = 3.0
        elif total_nodes < 200:
            ranksep_factor = 3.5
        elif total_nodes < 500:
            ranksep_factor = 4.0
        else:
            ranksep_factor = 5.0
            
        # Set SVG for large graphs
        if total_elements >= 1500:
            print(f'Graph too Large ({total_elements} elements). Rendering to .svg')
            img_format = 'svg'
        
        # Set graph attributes
        dot.attr(ranksep=str(ranksep_factor),nodesep='0.5')#, overlap='scale', pack='true', sep='+4')
        
        # Change layout direction (rotate 90 degrees)
        dot.attr(rankdir=rank_dir)
        
        # Set tail and head ports
        if rank_dir == 'BT':
            head_port = 's'
            tail_port = 'n'
        elif rank_dir == 'LR':
            head_port = 'w'
            tail_port = 'e'
        elif rank_dir == 'RL':
            head_port = 'e'
            tail_port = 'w'
        else: # TB
            head_port = 'n'
            tail_port = 's'

        # Iterate through the levels to create subgraphs
        for level in self._levels:
            field_name = level.getField().getName()  # Get the field name for the level

            if field_name not in field_subgraphs:
                # Create a new subgraph for this field level if it doesn't exist
                field_subgraphs[field_name] = graphviz.Digraph(name=f'cluster_{field_name}')
                field_subgraphs[field_name].attr(label=f"{field_name} Level", style='invis')

            # Add nodes to the corresponding subgraph
            for node in level.getNodes():
                node_name = node.getName()
                
                # Skip adding ACCEPT and DROP nodes if unroll_decisions is True
                if unroll_decisions and node_name in ['ACCEPT', 'DROP']:
                    dot.node(
                        node_name, 
                        style='invis'  # Make the node invisible
                    )
                    continue
                
                field_subgraphs[field_name].node(
                                            node_name, 
                                            _attributes = node.getAttributes(), 
                                            width = str(base_width + width_factor), 
                                            height= str(base_height + height_factor), 
                                            fontsize= str(base_font + font_factor))

                # Add edges to the main graph
                for edge in node.getOutgoing():
                    origin_name = edge.getOrigin().getName()
                    destination_name = edge.getDestination().getName()
                    edge_node_name = f"edge_node_{edge_node_counter}"
                    edge_node_counter += 1

                    if edge.getAttributes('label') is not None:
                        label = f"{edge.getId()},{edge.getAttributes('label')}"
                    else:
                        elements = edge.getElementSet().getElementsList()
                        if len(elements) > 5:
                            elements_str = '\n'.join(str(elem) for elem in elements[:5]) + '\n...'
                        else:
                            elements_str = '\n'.join(str(elem) for elem in elements)
                        label = f"{edge.getId()},\n{elements_str}"

                    edge_attributes = edge.getAttributes()

                    # Add the intermediate node with the label
                    dot.node(
                        edge_node_name, 
                        label, 
                        shape='plaintext', 
                        width=str(base_width + width_factor), 
                        height=str(base_height + height_factor),
                        fontsize=str(base_font + font_factor))

                    # Connect the origin to the intermediate node and intermediate node to the destination
                    dot.edge(origin_name, edge_node_name, tailport=tail_port, headport=head_port, _attributes=edge_attributes)

                    if unroll_decisions and destination_name in ['ACCEPT', 'DROP']:
                        unique_destination_name = f"{destination_name}_{edge_node_counter}"
                        dot.node(
                            unique_destination_name, 
                            destination_name, 
                            style='filled',
                            shape='box' if destination_name == 'ACCEPT' else 'diamond',
                            fillcolor='greenyellow' if destination_name == 'ACCEPT' else 'crimson',
                            width=str(base_width + width_factor), 
                            height=str(base_height + height_factor), 
                            fontsize=str(base_font + font_factor)
                        )
                        dot.edge(edge_node_name, unique_destination_name, tailport=tail_port, headport=head_port, _attributes=edge_attributes)
                    else:
                        dot.edge(edge_node_name, destination_name, tailport=tail_port, headport=head_port, _attributes=edge_attributes)

        # Add each subgraph to the main graph
        for subgraph in field_subgraphs.values():
            dot.subgraph(subgraph)
            

        # Render the graph to a file
        dot.render(name, format=img_format, view=False, cleanup=True)

    def highlightPath(self, rule_id, color='blue'):
        """
        Highlight the edges of a decision path for a given rule ID in the graph.

        Args:
            rule_id (int): The rule ID to highlight.
            color (str, optional): The color to use for highlighting. Defaults to 'red'.
        """
        # Traverse the graph to find all edges containing the specified rule ID
        for level in self._levels:
            for node in level.getNodes():
                for edge in node.getOutgoing():
                    if rule_id in edge.getId():
                        edge.setAttributes(color=color)
                    else:
                        edge.setAttributes(color='black')

        # Call the printFDD function to print the graph with the modified attributes
        self.printFDD(name=f"FilterRule_{rule_id}")

    def highlightDecisions(self):
        """
        Highlight all decision paths that end in 'ACCEPT' in green and those that end in 'DROP' in red.
        
        """
        def dfs(node, decision_path):
            if not node.getOutgoing():  # Terminal node
                color = "red" if node.getName() == "DROP" else "green"
                for _, e in decision_path:
                    e.setAttributes(color=color)
                return

            for edge in node.getOutgoing():
                dfs(edge.getDestination(), decision_path + [(node, edge)])

        # Start DFS from the root node
        dfs(self._levels[0].getNodes()[0], [])

        # Print the FDD with highlighted edges
        self.printFDD("highlighted_FDD")


    def _genPre(self, chain: Chain):
        """sumary
        """
        # Set FDD Name
        self._name = chain.getName()
        
        # Recorremos la lista de Rules
        for rule in chain.getRules():

            # Revisamos que todos los predicados de la regla esten contemplados en la lista de fields
            fields = [level.getField().getName() for level in self._levels]
            for predicate in rule.getPredicates():
                if predicate not in fields:
                    raise TypeError(f"Predicate {predicate} isn't include in FieldList")

            # Creamos una lista de Nodos temporal, que usaremos para conectar los edges en un bucle
            # La lista se inicia con el nodo root
            nodes = [self._levels[0].getNodes()[0]]

            # Agregamos un nodo por cada nivel, exptuando el primero y el ultimo
            for level in self._levels[1:-1]:

                newNode = Node(f"{level.getField().getName()}_{rule.getId()}", level)
                newNode.autoConnect()
                nodes.append(newNode)

            # Añadimos el nodo de decision al final
            decisionNode = self._getDecisionNode(rule.getDecision())
            nodes.append(decisionNode)

            # Recorremos la lista temporal de nodos y vamos añadiendo los Edges que los conectan
            for j in range(1, len(nodes)):

                elements = rule.getOption(nodes[j-1].getLevel().getField().getName())
                elementSet = ElementSet.createElementSet(nodes[j-1].getLevel().getField().getType(), elements if elements else [])
                newEdge = Edge([rule.getId()], nodes[j-1], nodes[j], elementSet)
                newEdge.autoConnect()


    def _sanityStep1(self):
        """ Sanitizes all first-level nodes of the FDD, except the last one, as it requires a different treatment. 
        """

        newIndex = 0

        # Recorremos los niveles, a excepcion de los ultimos dos.
        for h in range(len(self._levels[:-2])):

            level = self._levels[h]

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
                            newNode = Node(self._levels[h+1].getField().getName() + " new " + str(newIndex), self._levels[h+1])
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

        level = self._levels[-2]
        
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

    
    def _sanityStep3(self, chain: Chain):
        """Check and achieve completeness in the nodes
        """

        for level in self._levels[:-1]:

            for node in level.getNodes():

                left = ElementSet.createElementSet(level.getField().getType(), [])

                for edge in node.getOutgoing():

                    left.remove(edge.getElementSet())

                if not left.isEmpty():
                    
                    newEdge = Edge([999], node, self._getDecisionNode(chain.getDefaultDecision()), left)
                    newEdge.autoConnect()


    def genFDD(self, chain):
        """Generates the PreFDD and sanitizes it to convert it to FDD.
        """
        self._genPre(chain)
        self._sanityStep1()
        self._sanityStep2()
        self._sanityStep3(chain)


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
        for level in self._levels[1:-1]:
            nodes_to_remove = []
            for node_v in level.getNodes():
                v_out = node_v.getOutgoing()
                if len(v_out) == 1:  # Simple Node
                    # print(f"REMOVING SIMPLE NODE {node_v}")
                    e = v_out[0]    # Get the edge
                    v_prime = e.getDestination()
                    incoming_edges = list(node_v.getIncoming())  # Make a copy of the list to iterate safely
                    
                    for incoming_edge in incoming_edges:
                        # All edges now point to Node v'
                        incoming_edge.autoDisconnect()
                        incoming_edge.setDestination(v_prime)
                        # print(f'\tAdding {incoming_edge} to incoming edges of {v_prime}')
                        # print(f'\t\tEdge {incoming_edge} label: {incoming_edge.getElementSet().getElements()}')
                        incoming_edge.autoConnect() 
                    
                    # Mark Node v for removal
                    nodes_to_remove.append(node_v)
                    e.autoDisconnect()
                    # print(f'\tMarked {node_v} for removal from {level.getField().getName()} Level')
                    changed = True
            
            # Remove all marked nodes after iteration
            for node in nodes_to_remove:
                node.autoDisconnect()
                # print(f'\tRemoved Simple node {node} from {level.getField().getName()} Level')
        
        return changed
            
    def _removeIsomorphicNodes(self):
        """
        Apply the second reduction rule:
        If there are two nodes v and v' that are isomorphic, then remove v' along with all 
        its outgoing edges, and make all edges that pointed to v' now point to v.
        """
        changed = False
        for level in self._levels[:-1]: 
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
                        # print(f'\tREMOVING ISOMORPHIC NODES {node_v} - {node_v_prime}')
                        
                        # v_prime Edges now point to v
                        # print(f'\t{node_v_prime} Edges now point to {node_v}:')
                        for incoming_edge in node_v_prime.getIncoming():
                            incoming_edge.autoDisconnect()
                            incoming_edge.setDestination(node_v)
                            # print(f'\tUpdated Edge {incoming_edge}')
                            incoming_edge.autoConnect()
                        
                        # Remove v_prime's outgoing incidence 
                        for edge in node_v_prime.getOutgoing():
                            edge.autoDisconnect()
                        
                        # Mark node_v_prime for removal
                        nodes_to_remove.append(node_v_prime)
                        changed = True
            
            # Remove all marked nodes after iteration
            for node in nodes_to_remove:
                if node in level.getNodes():
                    node.autoDisconnect()
                    # print(f'Removed Isomorphic node {node} from {level.getField().getName()} Level')
        
        return changed
        
    def _mergeEdges(self):
        """
        Apply the third reduction rule:
        If there are two edges e and e' that both are between the same pair of nodes, then
        remove e' and change the label of e from I(e) to I(e) U I(e').
        """
        changed = False
        for level in self._levels[:-1]:
            for node in level.getNodes():
                seen_edges = {}
                for edge in node.getOutgoing():
                    # Pair of nodes
                    key = edge.getDestination()
                    if key in seen_edges:
                        seen_edge = seen_edges[key]
                        # Merge element sets
                        # print(f'MERGING edges {seen_edge} and {edge}: '
                              #f'{seen_edge.getElementSet().getElements()} U {edge.getElementSet().getElements()}')
                        merged_set = seen_edge.getElementSet().unionSet(edge.getElementSet())
                        seen_edge.setElementSet(merged_set)
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
        # print(f'Checking ISOMORPHISM between {node_a} and {node_b}')
        if len(node_a.getOutgoing()) == 0 or len(node_a.getOutgoing()) != len(node_b.getOutgoing()):
            return False
        
        for edge_v in node_a.getOutgoing():
            match = False
            for edge_v_prime in node_b.getOutgoing():
                # print(f'\t{edge_v}: {edge_v.getElementSet().getElements()}\n'
                    #  f'\t{edge_v_prime}: {edge_v_prime.getElementSet().getElements()}')
                if (edge_v.getDestination() == edge_v_prime.getDestination() 
                    and edge_v.getElementSet() == edge_v_prime.getElementSet()):
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
        last_level = self._levels[-1]  # Last Level has terminal Nodes
        for node in last_level.getNodes():
            if not node.getOutgoing():
                node.setLoad(1)

        # Step 2: Compute the load for non-terminal nodes
        changed = True
        while changed:
            changed = False
            for level in self._levels:
                for node in level.getNodes():
                    if node.getLoad() == 0 and all(dest.getLoad() != 0 for dest in (e.getDestination() for e in node.getOutgoing())):
                        # (a) Select the edge with the largest (load(e_j) - 1) * load(v_j)
                        best_edge = max(node.getOutgoing(), key=lambda e: (self._edgeLoad(e) - 1) * e.getDestination().getLoad())
                        best_edge.markEdge()
                        # print(f'Marking Edge {best_edge}')
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
        return len(edge.getElementSet().getElementsList())
        
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
        chain = Chain(f"{self._name}")
    
        # We don't mark visited nodes since we need to traverse all paths (rules)
        # There is no risk of divergence since there are no cycles (DAG) 
        def dfs(node, decision_path):
            if not node.getOutgoing():  # Terminal node
                rule = Rule(len(chain.getRules())) 
                matching_predicate = {}
                resolving_predicate = {}
    
                for v, e in decision_path:
                    element_class = ElementSetRegistry.getElementSetClass(v.getLevel().getField().getType()) # ElementSet Type
                    field = v.getLevel().getField() # Field of level
                    element_set = e.getElementSet() # Edge elementSet
    
                    if not e.getMarking():  # Not marked with "all"
                        matching_predicate[field] = element_set
                    else:
                        matching_predicate[field] = element_class.getDomain() 
                        
                    resolving_predicate[field] = element_set 
    
                # Set the predicates and decision for the rule
                for field, values in matching_predicate.items():
                    if values != ElementSetRegistry.getRegistry()[field.getType()].getDomain():
                        rule.setPredicate(field.getName(), values.getElementsList())
                        rule.setMatchingPredicate(field.getName(), values)
                
                for field, values in resolving_predicate.items():
                    rule.setResolvingPredicate(field.getName(), values)
                
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
        dfs(self._levels[0].getNodes()[0], []) 
        
        #return chain
        #print(f'NOT COMPACTED CHAIN:\n{chain}\n\nCompacting Rules...')

        # Step 2: Compact Rules
        redundant = [False] * len(chain.getRules())

        # Mark redundant rules
        n = len(chain.getRules())
        for i in range(n - 1, -1, -1):
            for k in range(i + 1, n):
                #print(f'CHECKING RULES {i} and {k}')
                if (not redundant[k] and
                    self._sameDecision(chain[i], chain[k]) and
                    self._implies(chain[i], chain[k])):
                    # Check if rule i is redundant based on rule k
                    is_redundant = True
                    for j in range(i + 1, k):
                        #print(f'\tIntermediate rule check: {j}')
                        if (not redundant[j] and
                            not self._sameDecision(chain[i], chain[j]) and
                            not self._mutuallyExclusive(chain[i], chain[j])):
                            #print(f'\t\tRule {i} and rule {j} are NOT REDUNDANT.')
                            is_redundant = False
                            break
                    if is_redundant:
                        #print(f'\t\tMarking rule {i} as REDUNDANT based on rule {k}.')
                        redundant[i] = True
                        break
                else:
                    pass
                    #print(f'\tRule {i} and rule {k} did not get to the intermediate Rule check.')

        # Remove redundant rules
        new_rules = [rule for i, rule in enumerate(chain.getRules()) if not redundant[i]]
        chain.setRules(new_rules)
        
        # Fix Rules Ids after removal
        for idx, rule in enumerate(chain.getRules()):
            rule.setId(idx)
            
        print(f'\nRemoved {n - len(chain.getRules())} REDUNDANT rules from the chain.\n')

        return chain     
    
    def _sameDecision(self, rule1: Rule, rule2: Rule) -> bool:
        """
        Check if two rules have the same decision.
        
        Args:
            rule1 (Rule): First rule to compare.
            rule2 (Rule): Second rule to compare.
        
        Returns:
            bool: True if rule1 and rule2 have the same decision, False otherwise.
        """
        #print(f'\tCheck sameDecision: Rule_{rule1.getId()} & Rule_{rule2.getId()} = {rule1.getDecision() == rule2.getDecision()}')
        return rule1.getDecision() == rule2.getDecision()

    def _implies(self, rule1: Rule, rule2: Rule) -> bool:
        """
        Check if rule1's resolving predicate implies rule2's matching predicate.
        
        'r_i.rp implies r_k.mp' means that for any packet p, if p satisfies 
        r_i.rp, then p satisﬁes r_k.mp. Checking whether r_i.rp implies r_k.mp is simple. 
        Let r_i.rp be F_1 ∈ T_1 ∧ ... ∧ F_d ∈ T_d and let r_k.mp be F_1 ∈ S_1 ∧ ... ∧ F_d ∈ S_d. 
        Then, r_i.rp implies r_k.mp if and only if for every j, where 1 <= j <= d, the condition T_j ⊆ S_j holds.
        
        Args:
            rule1 (Rule): First rule to compare.
            rule2 (Rule): Second rule to compare.
            
        Returns:
            bool: True if rule1 predicate implies rule2 predicate, False otherwise.
        """
        for field in self._fieldList.getFields():
            field_dom = ElementSetRegistry.getElementSetClass(field.getType()).getDomain()
            field_name = field.getName()
            
            option1 = rule1.getResolvingPredicate(field_name, field_dom)
            option2 = rule2.getMatchingPredicate(field_name, field_dom)

            #print(f'\tChecking predicates ({field.getName()}) {option1} - {option2}: {option1.isSubset(option2)}')
            if not option1.isSubset(option2):
                return False
        return True
    
    def _mutuallyExclusive(self, rule1: Rule, rule2: Rule) -> bool:
        """
        Check if rule1 and rule2 are mutually exclusive.

        Two rules are mutually exclusive if there are no common values across all fields.

        Args:
            rule1 (Rule): First rule to compare.
            rule2 (Rule): Second rule to compare.

        Returns:
            bool: True if rule1 and rule2 are mutually exclusive, False otherwise.
        """
        for field in self._fieldList.getFields():
            field_dom = ElementSetRegistry.getElementSetClass(field.getType()).getDomain()
            field_name = field.getName()
            
            option1 = rule1.getResolvingPredicate(field_name, field_dom) 
            option2 = rule2.getMatchingPredicate(field_name, field_dom)
            
            #print(f'\tChecking Mutual Exclusion {option1} - {option2}: {option1.isDisjoint(option2)}')
            if option1.isDisjoint(option2):  # Check if they have any common elements
                return True
        return False


class ChainComparator:

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
        
        def difference(self, other: "ChainComparator.PseudoRule", fieldList: FieldList) -> List[Rule]:
                
            diff = []

            for field in fieldList.getFields():

                fDiff = self.getPredicates()[field.getName()].differenceSet(other.getPredicates()[field.getName()])
                if not fDiff.isEmpty():
                    rule = self.replicate()
                    rule.setPredicate(field.getName(), fDiff)
                    diff.append(rule)

            i = 0
            while i < len(diff)-1:

                intersection = diff[i].intersection(diff[i+1], fieldList)

                if intersection != None:

                    if intersection.sameFieldValues(diff[i]):
                        diff.pop(i)
                    elif intersection.sameFieldValues(diff[i+1]):
                        diff.pop(i+1)
                    else:
                        i += 1

                else:
                    i += 1

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

            if self.getDefaultDecision() != "DROP":
                raise ValueError(f"La cadena tiene Default decision {self.getDefaultDecision()} y por el momento solo se pueden comparar cadenas con default decision DROP")

            newChain = ChainComparator.PseudoChain()
            newChain.setDefaultDecision(self.getDefaultDecision())
            newChain.setName(f"effective-{self.getName()}")

            rules = self.getRules()

            for i in range(len(rules)):

                print(f"\ni: {i}")
                print(rules[i].getDecision())

                if rules[i].getDecision() == "ACCEPT":

                    resRules = [rules[i]]

                    for j in range(i):

                        print(f"\nj: {j}")
                        print(f"resRules: {resRules}")

                        resRules2 = []

                        for k in range(len(resRules)):

                            print(f"\nk: {k}")

                            diff = resRules[k].difference(rules[j], fieldList)

                            print(f"restando A-B\nA: {resRules[k]}\nB: {rules[j]}")
                            print(f"diff: {diff}")

                            if diff != None:

                                resRules2 += diff

                        i = 0
                        while i < len(resRules2)-1:

                            intersection = resRules2[i].intersection(resRules2[i+1], fieldList)

                            if intersection != None:

                                if intersection.sameFieldValues(resRules2[i]):
                                    resRules2.pop(i)
                                elif intersection.sameFieldValues(resRules2[i+1]):
                                    resRules2.pop(i+1)
                                else:
                                    i += 1

                            else:
                                i += 1

                        resRules = resRules2

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

        if self._effectiveChain1 and self._effectiveChain2:

            #Comparacion 1 contra 2

            for rule1 in self._effectiveChain1.getRules():

                residual = [rule1]

                for rule2 in self._effectiveChain2.getRules():

                    accum = []

                    for rule in residual:

                        diff = rule.difference(rule2, self._fieldList)

                        if diff != None:

                            accum += diff

                    i = 0
                    while i < len(accum)-1:

                        intersection = accum[i].intersection(accum[i+1], self._fieldList)

                        if intersection != None:

                            if intersection.sameFieldValues(accum[i]):
                                accum.pop(i)
                            elif intersection.sameFieldValues(accum[i+1]):
                                accum.pop(i+1)
                            else:
                                i += 1

                        else:
                            i += 1

                    residual = accum

                for result in residual:

                    if not result.isNull():
                        return False

            #Comparacion 2 contra 1

            for rule1 in self._effectiveChain2.getRules():

                residual = [rule1]

                for rule2 in self._effectiveChain1.getRules():

                    accum = []

                    for rule in residual:

                        diff = rule.difference(rule2, self._fieldList)

                        if diff != None:

                            accum += diff

                    i = 0
                    while i < len(accum)-1:

                        intersection = accum[i].intersection(accum[i+1], self._fieldList)

                        if intersection != None:

                            if intersection.sameFieldValues(accum[i]):
                                accum.pop(i)
                            elif intersection.sameFieldValues(accum[i+1]):
                                accum.pop(i+1)
                            else:
                                i += 1

                        else:
                            i += 1

                    residual = accum

                for result in residual:

                    if not result.isNull():
                        return False
                    
            # Si hasta aqui no retornamos un falso, entonces es True

            return True
        
        else:

            raise ValueError("Debe cargar primero dos Chain en ChainComparator")

            
                    

        