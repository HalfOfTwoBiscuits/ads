from datetime import datetime, timedelta
from pytest import fixture

from graph import Graph
from courier_routing import CourierRouter
from unittest_time_util import UnitTestTimeUtility

@fixture
def graph() -> Graph:
    '''Graph for use in unit tests of the routing algorithm.'''

    g = Graph(
        ["A", "B", "C", "D", "E"]
    )
    g.create_edge("A", "B", 2.0)
    g.create_edge("A", "C", 1.5)
    g.create_edge("A", "D", 4.0)
    g.create_edge("B", "C", 1.0)
    g.create_edge("B", "D", 3.25)
    g.create_edge("C", "E", 0.5)
    g.create_edge("D", "E", 2.5)

    return g

@fixture
def lateness_severity() -> float:
    return 5.0

@fixture
def enroute_benefit() -> float:
    return 2.0

@fixture
def enroute_mins_early_leeway() -> timedelta:
    return timedelta(minutes=5)

@fixture
def router(graph: Graph, lateness_severity: float, enroute_benefit: float, enroute_mins_early_leeway: timedelta) -> CourierRouter:
    '''CourierRouter object constructed using the graph fixture.
    For use in unit tests of the routing algorithm.'''

    return CourierRouter(graph, lateness_severity, enroute_benefit, enroute_mins_early_leeway)

@fixture
def now() -> datetime:
    '''Current timestamp at the start of the driver's work day.
    For use in unit tests of the routing algorithm.'''

    return datetime(year=2022, month=1, day=1, hour=8)

@fixture
def time_util(graph: Graph) -> UnitTestTimeUtility:
    return UnitTestTimeUtility(graph)

@fixture
def arbitrary_duration() -> timedelta:
    return timedelta(minutes=15)