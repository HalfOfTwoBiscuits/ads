from weighted_edge import WeightedEdge

from exceptions import NodeNotFoundError, EdgeNotFoundError

class Graph:
    '''Object representing an undirected, weighted graph.
    Edges are represented using an adjacency list.
    For simplicity, nodes are represented as strings.'''

    __nodes: list[str]
    __adjacency: dict[str:list[WeightedEdge]]

    def __init__(self, nodes: list[str]):
        self.__nodes = nodes
        self.__adjacency = {node : [] for node in nodes}

    def create_edge(self, node1: str, node2: str, weight: float):
        '''Method used to create an edge between two nodes
        when setting up the graph.'''

        try:
            node1_adjacency = self.__adjacency[node1]
            node2_adjacency = self.__adjacency[node2]
        except KeyError:
            raise NodeNotFoundError(
                f"Couldn't create edge between {node1} and {node2} "
                "because one or both of those nodes don't exist. "
                f"Full list of nodes: {self.__nodes}"
            )
        else:
            node1_adjacency.append(WeightedEdge(node2, weight))
            node2_adjacency.append(WeightedEdge(node1, weight))

    @property
    def all_nodes(self) -> list[str]:
        '''Returns a list of all nodes.'''

        return self.__nodes

    def adjacent_to(self, node: str) -> list[WeightedEdge]:
        '''Returns a list of WeightedEdge objects for the
        nodes adjacent to the given node.

        The adjacent node and edge weight can be retrieved through
        the `node` and `weight` properties of the WeightedEdge.'''

        try:
            return self._adjacency[node]
        except KeyError:
            raise NodeNotFoundError(
                f"Couldn't get nodes adjacent to {node} "
                f"because {node} doesn't exist. "
                f"Full list of nodes: {self.__nodes}"
            )
        
    def get_weight(self, node1: str, node2: str) -> float:
        '''Get the weight of the edge between the given two nodes.
        If either doesn't exist, raise NodeNotFoundError.
        If there is no edge between them, raise EdgeNotFoundError.
        For use in unit tests.'''

        edges = self.adjacent_to(node1)
        self.adjacent_to(node2) # Result is not used. For raising an error if node2 doesn't exist.

        for edge in edges:
            if edge == node2:
                return edge.weight
        else:
            raise EdgeNotFoundError(
                f"Couldn't get weight of edge between {node1} and {node2} "
                "because there is no edge between those two nodes."
            )