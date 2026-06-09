from datetime import datetime
from statistics import fmean

from graph import Graph
from delivery import Delivery
from return_to_warehouse import ReturnToWarehouse
from time_util import TimeUtility
from exceptions import UnreachableNodeError

class CourierRouter:
    '''Class responsible for determining the optimal route for a delivery driver.'''

    __graph: Graph
    __lateness_severity: float
    __enroute_delivery_benefit: float
    __enroute_delivery_mins_early_leeway: int

    def __init__(
        self, area_graph: Graph,
        lateness_severity: float,
        enroute_delivery_benefit: float,
        enroute_delivery_mins_early_leeway: int
        ):
        self.__graph = area_graph
        self.__lateness_severity = lateness_severity
        self.__enroute_delivery_benefit = enroute_delivery_benefit
        self.__enroute_delivery_mins_early_leeway = enroute_delivery_mins_early_leeway

    def route_driver(
        self, starting_node: str,
        deliveries_to_make: list[Delivery],
        current_time: datetime
        ) -> list[str]:
        '''Return a list of nodes representing a route for the driver to follow.
        The route will minimise edge weight (which represents distance)
        and attempt to get all deliveries to the destination in their timeslot.'''

        # Sort deliveries from latest timeslot to soonest.
        # The priority is soonest to latest, but popping from
        # the end of a list is more efficient.
        # The end of the timeslot is used, rather than the beginning,
        # to prioritise deliveries whose slots will be over soon.
        assert type(deliveries_to_make) == list and type(deliveries_to_make[0]) == Delivery
        deliveries_to_make.sort(key=self.sort_key_for_deliveries, reverse=True)

        driver_location = starting_node
        full_route = [starting_node]

        # Add extra delivery for the return to warehouse at the end.
        # It uses a different class which, instead of having an actual timeslot,
        # always treats the delivery slot as after the provided time.
        # This prevents it from being delivered enroute.
        return_to_warehouse = ReturnToWarehouse(starting_node)
        deliveries_to_make.insert(0, return_to_warehouse)

        # Repeat until all deliveries have been addressed.
        while deliveries_to_make:
            next_delivery = deliveries_to_make.pop()

            # If the driver is already at the destination,
            # no pathfinding is needed.
            if next_delivery.destination_node == driver_location:
                continue

            # Initialise distance and route data for each node.
            nodes_to_explore = self.__graph.all_nodes
            shortest_distance = {}
            previous_node = {}
            for node in nodes_to_explore:
                shortest_distance[node] = float("inf")
                previous_node[node] = None
            shortest_distance[driver_location] = 0

            # The algorithm doesn't stop upon reaching the destination node, because
            # it may be possible to make other deliveries enroute and still arrive on time.
            # However, there's no point in traversing from the destination to other nodes,
            # because the output path leads to the destination - anything further is ignored.
            nodes_to_explore.remove(next_delivery.destination_node)

            # Use a dictionary to track whether each remaining delivery
            # can be made by following the route.
            route_delivers = {delivery : False for delivery in deliveries_to_make}
            route_delivers[next_delivery] = True
            
            while nodes_to_explore:
                # Find node with the shortest distance from start.
                current_node = min(nodes_to_explore, key=shortest_distance.__getitem__)
                nodes_to_explore.remove(current_node)

                # Iterate through adjacent nodes.
                for edge in self.__graph.adjacent_to(current_node):
                    # Get potential distance to reach the node, and time taken.
                    potential_distance = shortest_distance[current_node] + edge.weight
                    potential_time = current_time + TimeUtility.travel_time_for(potential_distance)

                    # If the delivery is late, penalise the route
                    # as if the driver travelled for the time it is late by,
                    # multiplied by a severity factor.
                    potential_distance += self.__late_delivery_penalty(next_delivery, current_time)
                    
                    # Identify any extra deliveries possible to make at this node.
                    extra_deliveries = []
                    for delivery in deliveries_to_make:
                        if delivery.destination_node == edge.node \
                            and delivery.expected_at(current_time, self.__enroute_delivery_mins_early_leeway) \
                            and not route_delivers[delivery]:

                            extra_deliveries.append(delivery)

                            # If an extra delivery is possible, incentivise as if
                            # the driver doesn't have to enter this node in future,
                            # multiplied by an benefit factor.
                            potential_distance -= self.__extra_delivery_bonus(delivery)

                    # If this is the best route found so far, store it.
                    if potential_distance < shortest_distance[edge.node]:
                        shortest_distance[edge.node] = potential_distance
                        previous_node[edge.node] = current_node
                        for delivery in extra_deliveries:
                            route_delivers[delivery] = True

            # Derive best route for the delivery.
            node = next_delivery.destination_node
            route_for_delivery = []

            # Starting from the destination, repeatedly insert the
            # previous node at the beginning of the list until the start is reached.
            while node != driver_location:
                route_for_delivery.insert(0, node)
                node = previous_node[node]

                # If there is no previous node in the path,
                # the destination is unreachable - throw an error.
                if node is None:
                    raise UnreachableNodeError(
                        f"Delivery destination at {next_delivery.destination_node} " 
                        f"is unreachable from driver location {driver_location}."
                    )

            # Remove extra deliveries from list.
            deliveries_to_make = [delivery for delivery in deliveries_to_make if not route_delivers[delivery]]
            
            # Add route for this delivery to the driver's full route.
            full_route += route_for_delivery

            # Set new location and time, and move onto the next soonest delivery.
            driver_location = next_delivery.destination_node
            current_time += TimeUtility.travel_time_for(
                shortest_distance[next_delivery.destination_node]
            )
            
        return full_route
                    

    def sort_key_for_deliveries(self, delivery: Delivery) -> datetime:
        '''Returns the key by which deliveries are sorted for priority - the end of their timeslot.
        This means deliveries with timeslots that end sooner are prioritised.'''

        return delivery.timeslot_end

    def __extra_delivery_bonus(self, delivery: Delivery) -> float:
        '''Amount subtracted from the total distance when an extra delivery can be made enroute.
        The average distance travelled by traversing to the delivery from an adjacent node,
        multiplied by a benefit factor.'''

        neighbours_distances_away = [
            edge.weight for edge in self.__graph.adjacent_to(delivery.destination_node)
        ]
        average_distance_away = fmean(neighbours_distances_away)
        return average_distance_away * self.__enroute_delivery_benefit

    def __late_delivery_penalty(self, delivery: Delivery, current_time: datetime) -> float:
        '''Amount added to the total distance to penalise for a late delivery.
        The distance that could be travelled in the number of minutes which
        the delivery is late by, multiplied by a severity factor.
        
        If the delivery is early or on time, the return value will be 0.0.'''

        minutes_late = delivery.minutes_late(current_time)
        if minutes_late > 0:
            return TimeUtility.distance_travelled_in(minutes_late) * self.__lateness_severity
        return 0.0