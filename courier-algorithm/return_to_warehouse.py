from datetime import datetime

from abstract_destination import AbstractDestination

class ReturnToWarehouse(AbstractDestination):
    def expected_at(self, time: datetime, leeway_mins: int) -> bool:
        '''Always returns False. The return to warehouse is always last
        and should never be expected at a different time.'''

        return False

    def minutes_late(self, time: datetime) -> int:
        '''Always returns 0. When returning to the warehouse,
        the goal is simply to find the fastest route, so
        penalising routes for lateness is not necessary.'''

        return 0