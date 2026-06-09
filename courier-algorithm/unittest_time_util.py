from datetime import datetime, timedelta

from graph import Graph
from time_util import TimeUtility

class UnitTestTimeUtility:
    '''Extended time utility for unit tests, used to determine the appropriate test delivery slots.'''

    __graph: Graph

    def __init__(self, graph: Graph):
        self.__graph = graph

    def timestamp_after_travelling(self, miles: float, start_time: datetime) -> datetime:
        '''Return the timestamp after travelling the provided distance in miles
        from the provided start time.
        Intended for unit tests.'''

        return start_time + TimeUtility.travel_time_for(miles)

    def timestamp_after_traversing(self, node1: str, node2: str, start_time: datetime) -> datetime:
        '''Return the timestamp after traversing between the given two nodes
        from the provided start time. Doesn't pathfind between non-adjacent nodes.
        Intended for unit tests.'''

        return self.timestamp_after_travelling(self.__graph.get_weight(node1, node2), start_time)
    
    def time_to_traverse(self, node1: str, node2: str) -> timedelta:
        '''Return the timedelta for the duration taken to traverse between the given two nodes.
        Doesn't pathfind between non-adjacent nodes.
        Intended for unit tests.'''

        return TimeUtility.travel_time_for(self.__graph.get_weight(node1, node2))