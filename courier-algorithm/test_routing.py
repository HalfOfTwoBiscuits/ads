from pytest import raises
from datetime import datetime, timedelta

from delivery import Delivery
from courier_routing import CourierRouter
from unittest_time_util import UnitTestTimeUtility

class TestRouting:

    def test_simple_route(self, router: CourierRouter, time_util: UnitTestTimeUtility, now: datetime, arbitrary_duration: timedelta):
        '''Test that the algorithm can find the optimal route for deliveries
        when the deliveries are positioned such that taking the shortest route
        to each delivery in turn will mean they all arrive within the timeslot,
        and each delivery is adjacent to the previous.'''

        # Deliveries: Start at A, B -> D -> E, then back to A.
        delivery_1_time = time_util.timestamp_after_traversing("A", "B", now)
        delivery_2_time = time_util.timestamp_after_traversing("B", "D", delivery_1_time)
        delivery_3_time = time_util.timestamp_after_traversing("D", "E", delivery_2_time)
        
        delivery1 = Delivery("B", delivery_1_time, arbitrary_duration),
        delivery2 = Delivery("D", delivery_2_time, arbitrary_duration),
        delivery3 = Delivery("E", delivery_3_time, arbitrary_duration)

        route = router.route_driver("A", [delivery1, delivery2, delivery3], now)
        assert route == ["A", "B", "D", "E", "C", "A"]

    def test_route_with_non_adjacent(self, router: CourierRouter, time_util: UnitTestTimeUtility, now: datetime, arbitrary_duration: timedelta):
        '''Test that the algorithm can find the optimal route for deliveries
        when the deliveries are positioned such that taking the shortest route
        to each delivery in turn will mean they all arrive within the timeslot,
        but some deliveries are not adjacent to the previous one, requiring a
        longer route that visits some nodes more than once.'''

        # Deliveries: Start at E, B via C -> D -> C via E, then back to E.
        via_c_time = time_util.timestamp_after_traversing("E", "C", now)
        delivery_1_time = time_util.timestamp_after_traversing("C", "B", via_c_time)
        delivery_2_time = time_util.timestamp_after_traversing("B", "D", delivery_1_time)
        via_e_time = time_util.timestamp_after_traversing("D", "E", delivery_2_time)
        delivery_3_time = time_util.timestamp_after_traversing("E", "C", via_e_time)

        deliveries = [
            Delivery("B", delivery_1_time, arbitrary_duration),
            Delivery("D", delivery_2_time, arbitrary_duration),
            Delivery("C", delivery_3_time, arbitrary_duration)
        ]

        route = router.route_driver("E", deliveries, now)
        assert route == ["E", "C", "B", "D", "E", "C", "E"]

    def test_overlapping_timeslots_allow_enroute(self, router: CourierRouter, time_util: UnitTestTimeUtility, now: datetime):
        '''Test that the algorithm can find the optimal route for deliveries
        when the deliveries are positioned such that taking the shortest route
        to each delivery in turn would mean they all arrive within the timeslot,
        but the timeslots overlap such that other deliveries could be made enroute,
        resulting in a shorter route without becoming late.'''

        # Start at A.
        # Timeslot-order route: C -> D via E -> B
        # Optimal, shortest route: C -> B -> D
        delivery_1_time = time_util.timestamp_after_traversing("A", "C", now)
        delivery_2_time = time_util.timestamp_after_traversing("B", "C", delivery_1_time)
        delivery_3_time = delivery_2_time - timedelta(minutes=1)

        # Duration for delivery_1 makes it late unless it's delivered first, to discourage detouring too soon,
        # duration for delivery_2 and 3 means they won't be late regardless of whether the detour is taken.
        delivery_1_duration = time_util.time_to_traverse("A", "B")
        delivery_2_duration = time_util.time_to_traverse("C", "E") + \
            time_util.time_to_traverse("E", "D") + time_util.time_to_traverse("D", "B")
        delivery_3_duration = max(
            time_util.time_to_traverse("B", "D"), 
            time_util.time_to_traverse("C", "E") + time_util.time_to_traverse("C", "D")
        )

        deliveries = [
            Delivery("C", delivery_1_time, delivery_1_duration),
            Delivery("B", delivery_2_time, delivery_2_duration),
            Delivery("D", delivery_3_time, delivery_3_duration)
        ]

        route = router.route_driver("A", deliveries, now)
        assert route == ["A", "C", "B", "D", "A"]

    def test_multi_delivery_to_same_node(self, router: CourierRouter, time_util: UnitTestTimeUtility, now: datetime, arbitrary_duration: timedelta):
        '''Test that the algorithm can find the optimal route for deliveries
        when there are multiple deliveries to the same node.'''
    
    def test_minimise_lateness(self, router: CourierRouter, time_util: UnitTestTimeUtility, now: datetime, arbitrary_duration: timedelta):
        '''Test that, when deliveries are positioned such that taking the shortest route to each in turn
        would lead to some deliveries being late, the algorithm uses detours to minimise the total number of minutes late for deliveries.'''
        ...