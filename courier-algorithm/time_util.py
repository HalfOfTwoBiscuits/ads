from datetime import datetime, timedelta

from graph import Graph

class TimeUtility:
    '''Utility that finds travel time for distances and vice versa.'''

    # Average speed on rural roads was 23.7mph in 2022.
    # Source: https://www.gov.uk/government/statistics/travel-time-measures-for-the-strategic-road-network-and-local-a-roads-january-to-december-2022/travel-time-measures-for-local-a-roads-january-to-december-2022-report
    AVG_MPH = 24

    @classmethod
    def travel_time_for(cls, miles: float) -> timedelta:
        '''Return the time taken to travel this
        distance in miles, as a timedelta.'''

        return timedelta(hours=miles / cls.AVG_MPH)

    @classmethod
    def distance_travelled_in(cls, time: timedelta | int) -> float:
        '''Return the distance that a driver could travel
        in the provided time, as a float in miles.
        If the argument is an integer it is taken as a number of minutes.'''

        if isinstance(time, int):
            return time / 60 * cls.AVG_MPH

        return time.total_seconds() / 3600 * cls.AVG_MPH
    
    @classmethod
    def timestamp_after_travelling(cls, miles: float, start_time: datetime) -> datetime:
        '''Return the timestamp after travelling the provided distance in miles
        from the provided start time.
        Intended for unit tests.'''

        return start_time + cls.travel_time_for(miles)

    @classmethod
    def timestamp_after_traversing(cls, graph: Graph, node1: str, node2: str, start_time: datetime) -> datetime:
        '''Return the timestamp after traversing between the given two nodes
        from the provided start time. Doesn't pathfind between non-adjacent nodes.
        Intended for unit tests.'''

        return cls.timestamp_after_travelling(graph.get_weight(node1, node2), start_time)
    
    @classmethod
    def time_to_traverse(cls, graph: Graph, node1: str, node2: str) -> timedelta:
        '''Return the timedelta for the duration taken to traverse between the given two nodes.
        Doesn't pathfind between non-adjacent nodes.
        Intended for unit tests.'''

        return cls.travel_time_for(graph.get_weight(node1, node2))