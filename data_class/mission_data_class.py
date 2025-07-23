from dataclasses import dataclass
from typing import List

@dataclass
class Waypoint:
    x: float
    y: float
    z: float = 0.0

@dataclass
class TimedWaypoint:
    waypoint: Waypoint
    timestamp: float

@dataclass
class DroneMission:
    name: str
    waypoints: List[TimedWaypoint]
    start_time: float
    end_time: float
