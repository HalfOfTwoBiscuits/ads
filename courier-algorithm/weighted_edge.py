from dataclasses import dataclass

@dataclass
class WeightedEdge:
    '''Dataclass used to represent the adjacency of a node along a weighted edge.
    It only stores one node, not two: the other node is represented as
    a key in the Graph.__adjacency dictionary.
    
    For the courier routing graph, the edges represent roads,
    and the weight is their length in miles.'''
    
    node: str
    weight: float