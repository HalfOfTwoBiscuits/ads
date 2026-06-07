from datetime import datetime
from abc import ABC, abstractmethod

class AbstractDestination(ABC):
    '''Abstract base class for Delivery and ReturnToWarehouse.'''
    
    __destination: str
    
    def __init__(self, destination_node: str):
        self.__destination = destination_node

    @property
    def destination_node(self) -> str:
        '''Returns the driver's destination node.'''
        return self.__destination

    @abstractmethod
    def expected_at(self, time: datetime, leeway_mins: int) -> bool:
        '''Returns a boolean for whether the driver is expected there at
        the given time. A leeway in minutes is also provided.'''
        ...

    @abstractmethod
    def minutes_late(self, time: datetime) -> int:
        '''Returns the number of minutes late the driver would be
        they arrived at the provided datetime.'''
        ...

    @abstractmethod
    def minutes_early(self, time: datetime) -> int:
        '''Returns the number of minutes early the driver would be
        they arrived at the provided datetime.'''
        ...