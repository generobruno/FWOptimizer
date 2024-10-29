"""
Firewall Decision Diagram (FDD) module
"""

from typing import List
import graphviz
import toml
import sys
import re
import hashlib

#QUITAR EN EL FUTURO
import random
from fwoptimizer.classes.rules import Chain, Rule
from fwoptimizer.utils.elementSet import ElementSetRegistry, ElementSet

class Field:
    """_summary_
    """

    def __init__(self, fieldName, fieldType):
        """_summary_

        Args:
            fieldName (_type_): _description_
            fieldType (_type_): _description_
        """
        self._fieldName_ = fieldName
        self._fieldType_ = fieldType

    def getName(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._fieldName_

    def getType(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._fieldType_

class FieldList:
    """_summary_
    """

    def __init__(self):
        """_summary_
        """
        self._fields_ = []

    def loadConfig(self, path):
        """_summary_

        Args:
            path (_type_): _description_
        """

        config = toml.load(path)

        _fields_ = config['fdd_config']['fields']

        for field in _fields_:
            self._fields_.append(Field(field['name'], field['type']))

    def getFields(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._fields_

    def printConfig(self):
        """_summary_
        """
        for i, field in enumerate(self._fields_):
            print(f'{i} [{field.getName()}, {field.getType()}]')

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
    
    def setAttributes(self, **new_attrs):
        """
        Update the Node attributes with new values.

        Args:
            new_attrs: New attributes to update.
        """
        self._attributes.update(new_attrs)
        
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
        self._id.sort()
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
        self._id.sort()

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
        Update the Edge attributes with new values.

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

    def __init__(self, fieldList: FieldList) -> None:
        """
        Fdd __init__.

        Args:
            fieldList: FieldList used by the firewall.
        """
        # FDD Name
        self._name = "Unnamed_FDD"
        # FDD Levels
        self._levels = []
        # A dict of registered decisions
        self._decisions = {}
        # FieldList of the FDD
        self._fieldList = fieldList

        # First create the list of tree levels using the settings extracted from the FieldList.
        # Throw a TypeError if any of the types specified for the level is invalid (its corresponding ElementSet does not exist)
        for field in fieldList.getFields():

            if field.getType() in ElementSetRegistry.getRegistry():

                self._levels.append(Level(field))
            
            else:

                raise TypeError()
            
        # Create the last level, which contains leaf nodes or what is the same, decisions 
        self._levels.append(Level(Field('Decision', 'Decision')))

        # Create the only root node in the first level of the tree.
        root = Node(self._levels[0].getField().getName(), self._levels[0])
        root.autoConnect()

    def getName(self):
        """
        Get FDD's Name

        Returns:
            str: FDD Name
        """
        return self._name

    def _getDecisionNode(self, decision: str) -> Node:
        """
        Obtains the node corresponding to this decision if it exists, or adds a new one and returns it.

        Args:
            decision: Str with a decision key word.

        Returns:
            A Node in the last level of the tree with the given decision.
        """
        if decision  not in self._decisions:
            self._decisions[decision] = Node(decision, self._levels[-1], shape='box', fontsize='35')
            self._decisions[decision].autoConnect()
        return self._decisions[decision]

    def getDecisions(self):
        """
        Get the FDD's Possible decisions

        Returns:
            Dict[fieldName, fieldType]: FDD's Decisions
        """
        return self._decisions

    def printFDD(self, name: str, img_format='png', rank_dir='TB', unroll_decisions=False) -> None:
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
        if total_elements >= 1500 and img_format != 'svg':
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
                if node.getAttributes('filterVisibility') == 'False':
                    continue
                
                node_name = node.getName()
                
                # Skip adding ACCEPT and DROP nodes if unroll_decisions is True
                if unroll_decisions and node_name in self._decisions.keys():
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
                    if edge.getAttributes('filterVisibility') == 'False':
                        continue
                    origin_name = edge.getOrigin().getName()
                    destination_name = edge.getDestination().getName()
                    edge_node_name = f"edge_node_{edge_node_counter}"
                    edge_node_counter += 1

                    if edge.getAttributes('label') is not None:
                        label = f"{min(edge.getId())},{edge.getAttributes('label')}"
                    else:
                        elements = edge.getElementSet().getElementsList()
                        if len(elements) > 5:
                            elements_str = '\n'.join(str(elem) for elem in elements[:5]) + '\n...'
                        else:
                            elements_str = '\n'.join(str(elem) for elem in elements)
                        label = f"{min(edge.getId())},\n{elements_str}"

                    edge_attributes = edge.getAttributes()
                    if edge.getMarking():
                        edge_attributes = edge_attributes.copy()
                        edge_attributes["color"] = "blue"

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

                    if unroll_decisions and destination_name in self._decisions.keys():
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

    def highlightPath(self, rule_id, color='blue') -> None:
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

    def highlightDecisions(self) -> None:
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

    def _setFilterVisibiltyToTop(self, node: Node):

        node.setAttributes(filterVisibility="True")
        for edge in node.getIncoming():
            edge.setAttributes(filterVisibility="True")
            self._setFilterVisibiltyToTop(edge.getOrigin())

    def _setFilterVisibiltyToBot(self, node: Node):

        node.setAttributes(filterVisibility="True")
        for edge in node.getOutgoing():
            edge.setAttributes(filterVisibility="True")
            self._setFilterVisibiltyToBot(edge.getDestination())

    def _setFilterAttr(self, value: str):

        for level in self._levels:

            for node in level.getNodes():

                node.setAttributes(filterVisibility=value)

                for edge in node.getOutgoing():

                    edge.setAttributes(filterVisibility=value)
                    
    def clearFilters(self):
        """
        Clear all filters.
        """
        self._setFilterAttr('True')

    def filterFDDForValue(self, fieldFiltered: str, matchExpresion: str, literal: bool = False):

        self._setFilterAttr("False")

        levelSelected = None

        for level in self._levels:
            if level.getField().getName() == fieldFiltered:
                levelSelected = level
                break

        if levelSelected == None:
            print(f"El campo {fieldFiltered} no coincide con nigún campo existente")
            return False
        
        if literal:
            matchExpresion = "^" + matchExpresion + "$"
        else:
            matchExpresion = "^" + matchExpresion

        found = False
        for node in levelSelected.getNodes():

            for outgoing in node.getOutgoing():

                for element in outgoing.getElementSet().getElementsList():

                    if re.search(matchExpresion, str(element)):

                        outgoing.setAttributes(filterVisibility="True")
                        self._setFilterVisibiltyToTop(outgoing.getOrigin())
                        self._setFilterVisibiltyToBot(outgoing.getDestination())
                        found = True
                        break
                    
        return found

    def _genPre(self, chain: Chain) -> None:
        """
        Generate the preFDD based on the rules of the given chain.
        A preFDD is a graph that no satisfy the rules to be a FDD still. 

        Args:
            chain: Chain from which the rules are extracted
        """
        # Set FDD Name
        self._name = chain.getName()
        
        # Iterate through the list of Rules.
        for rule in chain.getRules():

            # Check that all predicates in the Rule are in the fieldList. If anyone not are include raise an error.
            fields = [level.getField().getName() for level in self._levels]
            for predicate in rule.getPredicates():
                if predicate not in fields:
                    raise TypeError(f"Predicate {predicate} isn't include in FieldList")

            # Create a temporal list of Nodes to iterate later and connect the edges.
            # The first element of the lit is the root node.
            nodes = [self._levels[0].getNodes()[0]]

            # For each Level add a node, except the first and the last.
            for level in self._levels[1:-1]:

                newNode = Node(f"{level.getField().getName()}_{rule.getId()}", level)
                newNode.autoConnect()
                nodes.append(newNode)

            # Add the decision Node at the end.
            decisionNode = self._getDecisionNode(rule.getDecision())
            nodes.append(decisionNode)

            # Iterate through the Nodes and connect it with Edges.
            for j in range(1, len(nodes)):

                elements = rule.getOption(nodes[j-1].getLevel().getField().getName())
                elementSet = ElementSet.createElementSet(nodes[j-1].getLevel().getField().getType(), elements if elements else [])
                newEdge = Edge([rule.getId()], nodes[j-1], nodes[j], elementSet)
                newEdge.autoConnect()


    def _sanityFirstLevels(self) -> None:
        """ 
        Sanitizes all first-level nodes of the FDD, except the last one, as it requires a different treatment. 
        """

        newIndex = 0

        # Iterate the firsts levels, except the last two.
        for h in range(len(self._levels[:-2])):

            level = self._levels[h]

            # The i loop goes through all nodes in each level
            i = 0
            while i < len(level.getNodes()):

                node = level.getNodes()[i]

                # The j loop goes through all outgoing edges in each node.
                j = 0
                while j < len(node.getOutgoing()):

                    edge1 = node.getOutgoing()[j]

                    # The k loop goes through the outgoing edges after j edge to can be compares them.
                    k = j + 1
                    while k < len(node.getOutgoing()):

                        edge2 = node.getOutgoing()[k]

                        # If are overlapping
                        if edge1.getElementSet().isOverlapping(edge2.getElementSet()):

                            intersectionSet = edge1.getElementSet().intersectionSet(edge2.getElementSet())

                            # Create a new node in the level.
                            newNode = Node(self._levels[h+1].getField().getName() + " new " + str(newIndex), self._levels[h+1])
                            newNode.autoConnect()
                            newIndex = newIndex + 1

                            # Create a new edge among origin node and new node. His elementSet is the intersection.
                            newEdge = Edge(edge1.getId() + edge2.getId(), edge1.getOrigin(), newNode, intersectionSet)
                            newEdge.autoConnect()

                            # Replicate all outgoing edges of destination node of edge1 in the new node.
                            for outEdge in edge1.getDestination().getOutgoing():

                                copiedEdge = outEdge.replicate()
                                copiedEdge.setOrigin(newNode)
                                copiedEdge.autoConnect()

                            # Replicate all outgoing edges of destination node of edge1 in the new node.    
                            for outEdge in edge2.getDestination().getOutgoing():

                                copiedEdge = outEdge.replicate()
                                copiedEdge.setOrigin(newNode)
                                copiedEdge.autoConnect()

                            # Remove the intersection set elemnts from edge1 and edge2
                            edge1.getElementSet().remove(intersectionSet)
                            edge2.getElementSet().remove(intersectionSet)

                            # Check if edge2 is empty and if so we disconnect it.
                            if edge2.getElementSet().isEmpty():

                                orphanNode = edge2.getDestination()
                                edge2.autoDisconnect()

                                # If after desconection the node no have any incomming edge, remove all his outgoing edges and delete it.
                                if len(orphanNode.getIncoming()) == 0:

                                    while len(orphanNode.getOutgoing()) != 0:

                                        orphanNode.getOutgoing()[0].autoDisconnect()

                                    orphanNode.autoDisconnect()
                            
                            else: 

                                k = k + 1

                        # If there is no overlap we advance one edge in k loop.
                        else: 

                            k = k + 1

                    # Check if edge1 is empty and if so we disconnect it.
                    if edge1.getElementSet().isEmpty():

                        orphanNode = edge1.getDestination()
                        edge1.autoDisconnect()

                        # If after desconection the node no have any incomming edge, remove all his outgoing edges and delete it.
                        if len(orphanNode.getIncoming()) == 0:

                            while len(orphanNode.getOutgoing()) != 0:

                                orphanNode.getOutgoing()[0].autoDisconnect()

                            orphanNode.autoDisconnect()

                    else:
                        
                        j = j + 1

                i = i + 1
                    

    def _sanityLastLevel(self, chain: Chain, reportsPath: str = None) -> None:
        """
        Sanitizes the last-level nodes of the FDD.

        Args:
            chain: Chain used to get the rules and include them in the report.
            reportPath: Path to the report file. If None, the report will be output to stdout.
        """

        level = self._levels[-2]

        # variables to record redundancies and inconsistencies
        redundancies = set()
        inconsistencies = set()
        
        # The i loop goes through all nodes in last level
        i = 0
        while i < len(level.getNodes()):

            node = level.getNodes()[i]

            # The j loop goes through all outgoing edges in each node.
            j = 0
            while j < len(node.getOutgoing()):

                edge1 = node.getOutgoing()[j]

                # The k loop goes through the outgoing edges after j edge to can be compares them.
                k = j + 1
                while k < len(node.getOutgoing()):

                    edge2 = node.getOutgoing()[k]

                    # If are overlapping
                    if edge1.getElementSet().isOverlapping(edge2.getElementSet()):

                        ### IF THE USER SHOULD TAKE DECSIONS, PLACE ITS HERE ###
                        ### STARTING CURRENT RESOLUTION MODE FOR REDUNDANCY AND INCONSISTENCY ###

                        # If the edges have the same destination, so there is redundancy
                        if edge1.getDestination() == edge2.getDestination():

                            redundancies.add((min(edge1.getId()[0], edge2.getId()[0]), max(edge1.getId()[0], edge2.getId()[0])))

                            intersectionSet = edge1.getElementSet().intersectionSet(edge2.getElementSet())

                            # Sort the priorities and select the rule that has a higher priority (value closest to 0)
                            if sorted(edge1.getId())[0] <= sorted(edge2.getId())[0]:

                                edge2.getElementSet().remove(intersectionSet)

                                # If edge2 is empty, delete it
                                if edge2.getElementSet().isEmpty():

                                    edge2.autoDisconnect()

                            else:

                                edge1.getElementSet().remove(intersectionSet)

                                # If edge1 is empty, delete it
                                if edge1.getElementSet().isEmpty():

                                    edge1.autoDisconnect()
                                    j = j - 1
                                    break

                        # If the edges don't have the same destination, so there is inconsistency.
                        else:

                            inconsistencies.add((min(edge1.getId()[0], edge2.getId()[0]), max(edge1.getId()[0], edge2.getId()[0])))

                            intersectionSet = edge1.getElementSet().intersectionSet(edge2.getElementSet())

                            # Sort the priorities and select the rule that has a higher priority (value closest to 0)
                            if sorted(edge1.getId())[0] <= sorted(edge2.getId())[0]:

                                edge2.getElementSet().remove(intersectionSet)

                                # If edge2 is empty, delete it
                                if edge2.getElementSet().isEmpty():

                                    edge2.autoDisconnect()

                            else:

                                edge1.getElementSet().remove(intersectionSet)

                                # If edge1 is empty, delete it
                                if edge1.getElementSet().isEmpty():

                                    edge1.autoDisconnect()
                                    j = j - 1
                                    break

                    else:

                        k = k + 1
                
                j = j + 1

            i = i + 1

        # Generate report
        if reportsPath == None:
            writer = sys.stdout
        else:
            try:
                writer = open(reportsPath, 'w')
            except:
                print(f"No se pudo abrir el archivo {reportsPath}, se escribirá en stdout")
                writer = sys.stdout

        writer.write(f"\nSe encontraron las siguientes redundacias en el set de reglas:\n")
        for a in sorted(list(redundancies)):

            writer.write(f"\n{chain.getRuleForId(a[0])}\n{chain.getRuleForId(a[1])}\nRedundancia resuelta\n")

        writer.write(f"\nSe encontraron las siguientes inconsistencias en el set de reglas:\n")
        for b in sorted(list(inconsistencies)):
            writer.write(f"\n{chain.getRuleForId(b[0])}\n{chain.getRuleForId(b[1])}\n")
            writer.write(f"Por tener mayor prioridad la regla ID:{b[0]}, se conserva la decision {chain.getRuleForId(b[0]).getDecision()} para la interseccion entre ambas\n")

        if writer != sys.stdout:
            writer.close()


    def _achieveCompleteness(self, defaultDecision: str) -> None:
        """
        Check and achieve completeness in the nodes.

        Args:
            defaultDecision: Default decision for the paths not generated still.
        """

        for level in self._levels[:-1]:

            for node in level.getNodes():

                left = ElementSet.createElementSet(level.getField().getType(), [])

                for edge in node.getOutgoing():

                    left.remove(edge.getElementSet())

                if not left.isEmpty():
                    
                    newEdge = Edge([999], node, self._getDecisionNode(defaultDecision), left)
                    newEdge.autoConnect()


    def genFDD(self, chain: Chain, reportsPath: str = None) -> None:
        """
        Generates the FDD content.
        First generates the PreFDD, after sanitizes it to convert it to FDD.
        
        Args:
            chain: Chain from which the rules are extracted.
            reportsPath: Path to save sanity logs.
        """
        self._genPre(chain)
        self._sanityFirstLevels()
        self._sanityLastLevel(chain, reportsPath)
        self._achieveCompleteness(chain.getDefaultDecision())


    def reduction(self) -> None:
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
            
    def _removeSimpleNodes(self) -> bool:
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
    
    def _removeIsomorphicNodes(self) -> bool:
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


    def _mergeEdges(self) -> bool:
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
    

    def marking(self) -> None:
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

        # Step 0: Erase previous marking
        for level in self._levels:
            for node in level.getNodes():
                node.setLoad(0)
                for edge in node.getOutgoing():
                    edge.markEdge(False)
                    
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

                        # (b) Compute the load of v
                        node_load = sum(self._edgeLoad(e) * e.getDestination().getLoad() for e in node.getOutgoing())
                        node.setLoad(node_load)
                        changed = True
                        
    def _edgeLoad(self, edge) -> int:
        """
        Compute the load of an edge based on its marking and its element set.

        Args:
            edge: Edge to calculate the load.

        Return:
            The load for the given edge.
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
                        if len(element_set.getElements()) == 1: # EXCEPTION
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
    
    def addRuleToFDD(self, rule: Rule):
        """
        Add Rule to the FDD

        Args:
            rule (Rule): Rule to add

        Raises:
            TypeError: If the rule has an inexistent predicate.
        """

        # Check that all predicates in the Rule are in the fieldList. If anyone not are include raise an error.
        fields_names = [level.getField().getName() for level in self._levels]
        for predicate in rule.getPredicates():
            if predicate not in fields_names:
                raise TypeError(f"Predicate {predicate} isn't include in FieldList")

        nodes_next = [self._levels[0].getNodes()[0]]

        for i in range(len(self._levels[:-2])):

            level = self._levels[i]
            field = level.getField()

            nodes = nodes_next
            nodes_next = []
            elements = rule.getOption(field.getName())
            elementSet = ElementSet.createElementSet(field.getType(), elements if elements else [])

            for node in nodes:

                edges = []

                for outgoing in node.getOutgoing():

                    if elementSet.isOverlapping(outgoing.getElementSet()):

                        edges.append(outgoing)

                for edge in edges:
                    
                    intersectionSet = elementSet.intersectionSet(edge.getElementSet())

                    # TODO Lucho - quitar el random e implementar otra manera de nominar los nodos
                    newNode = Node(self._levels[i+1].getField().getName() + " added " + str(random.randint(10000, 20000)), self._levels[i+1])
                    newNode.autoConnect()

                    #Chequear que los nodos no vayan directamente a decision sin pasar por los otros lvls intermedios.
                    if edge.getDestination().getLevel() != self._levels[i+1]:

                        self._completeNode(edge, newNode)

                    else:

                        # Replicate all outgoing edges of destination node of edge1 in the new node.
                        for outEdge in edge.getDestination().getOutgoing():

                            copiedEdge = outEdge.replicate()
                            copiedEdge.setOrigin(newNode)
                            copiedEdge.autoConnect()

                    newEdge = Edge(edge.getId() + [rule.getId()], edge.getOrigin(), newNode, intersectionSet)
                    newEdge.autoConnect()

                    edge.getElementSet().remove(intersectionSet)

                    # If edge is empty, delete it
                    if edge.getElementSet().isEmpty():
                        
                        orphanNode = edge.getDestination()
                        edge.autoDisconnect()

                        # If after desconection the node no have any incomming edge, remove all his outgoing edges and delete it.
                        if len(orphanNode.getIncoming()) == 0:

                            while len(orphanNode.getOutgoing()) != 0:

                                orphanNode.getOutgoing()[0].autoDisconnect()

                            orphanNode.autoDisconnect()

                    # Agrego el nuevo nodo para continuarlo en el siguiente bucle
                    nodes_next.append(newNode)

        #For the last level, the edges don't go to new nodes
        for node in nodes_next:

            level = self._levels[-2]
            field = level.getField()

            elements = rule.getOption(field.getName())
            elementSet = ElementSet.createElementSet(field.getType(), elements if elements else [])

            edges = []

            for outgoing in node.getOutgoing():

                    if elementSet.isOverlapping(outgoing.getElementSet()):

                        edges.append(outgoing)

            for edge in edges:

                intersectionSet = elementSet.intersectionSet(edge.getElementSet())

                newEdge = Edge(edge.getId() + [rule.getId()], node, self._getDecisionNode(rule.getDecision()), intersectionSet)
                newEdge.autoConnect()

                edge.getElementSet().remove(intersectionSet)

                if edge.getElementSet().isEmpty():

                    edge.autoDisconnect()
         
    def _completeNode(self, edge: Edge, newNode: Node):

        if edge.getDestination().getLevel().getField().getName() != 'Decision':

            print(f"Error _completeNode(): Caso no reconocido, edge no lleva a Decision Field")

        else:

            newEdge = Edge([999], newNode, edge.getDestination(), ElementSet.createElementSet(newNode.getLevel().getField().getType(), []))
            newEdge.autoConnect()
