from datetime import datetime, timedelta

from abstract_destination import AbstractDestination

class Delivery(AbstractDestination):
    '''Object representing a delivery to make to a specific node within a timeslot.'''

    __timeslot_start: datetime
    __timeslot_end: datetime

    def __init__(self, destination_node: str, timeslot_start: datetime, timeslot_duration: timedelta):
        super().__init__(destination_node)
        self.__timeslot_start = timeslot_start
        self.__timeslot_end = timeslot_start + timeslot_duration

    @property
    def timeslot_end(self) -> datetime:
        '''Returns the datetime object for the end of the delivery slot.'''

        return self.__timeslot_end

    @property
    def timeslot_start(self) -> datetime:
        '''Returns the datetime object for the start of the delivery slot.
        Not used in the algorithm, but it is included for maintainability.'''

        return self.__timeslot_start

    def expected_at(self, time: datetime, leeway_mins: int) -> bool:
        '''Returns True if the provided datetime is after the start of the timeslot,
        or before it within the provided leeway in minutes.

        It doesn't check the end of the timeslot, because if the courier
        is at the location and the delivery slot has started, they should make the delivery
        - if they leave without doing that, the delivery will only get later.'''

        return time >= self.__timeslot_start - timedelta(minutes=leeway_mins)

    def minutes_late(self, time: datetime) -> int:
        '''Returns the number of minutes late the delivery would be
        if it arrived at the provided datetime.
        
        If the delivery would be early or on time, the return value is 0.'''

        lateness = time - self.__timeslot_end
        minutes_late = lateness.total_seconds() // 60
        return max(0, minutes_late)