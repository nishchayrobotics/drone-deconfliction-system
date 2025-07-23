from data_class.mission_data_class import DroneMission
from typing import List, Dict, Any, Tuple, Union
import math


def distance(p1: Any, p2: Any) -> float:
    """
    Calculate the 3D Euclidean distance between two waypoints.
    
    Computes the straight-line distance between two points in 3D space
    using the standard Euclidean distance formula: √[(x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²]
    
    Args:
        p1 (Any): First waypoint object with x, y, z coordinate attributes.
        p2 (Any): Second waypoint object with x, y, z coordinate attributes.
    
    Returns:
        float: The 3D Euclidean distance between the two waypoints in meters.
    
    Example:
        >>> waypoint_a = Waypoint(x=10.0, y=20.0, z=30.0)
        >>> waypoint_b = Waypoint(x=13.0, y=24.0, z=30.0)
        >>> distance(waypoint_a, waypoint_b)
        5.0
    
    Notes:
        - Assumes both waypoints have numeric x, y, z attributes
        - Returns distance in the same units as the input coordinates
        - Uses math.sqrt for precise floating-point calculation
    """
    return math.sqrt(
        (p1.x - p2.x)**2 +
        (p1.y - p2.y)**2 +
        (p1.z - p2.z)**2
    )


def check_conflicts(
    primary: DroneMission, 
    others: List[DroneMission], 
    safety_radius: float = 2.0
) -> Dict[str, Union[str, List[Dict[str, Any]]]]:
    """
    Check for spatial and temporal conflicts between drone missions.
    
    Analyzes the primary drone's mission against other drone missions to identify
    potential conflicts where drones would be too close in both space and time.
    A conflict occurs when two drones are within the safety radius at similar times.
    
    Args:
        primary (DroneMission): The primary drone mission to check for conflicts.
            Must contain waypoints with coordinates and timestamps.
        others (List[DroneMission]): List of other drone missions to compare against.
            Each mission should contain waypoints with spatial and temporal data.
        safety_radius (float, optional): Minimum safe separation distance in meters.
            Defaults to 2.0 meters. Conflicts are detected when drones are closer
            than this distance.
    
    Returns:
        Dict[str, Union[str, List[Dict[str, Any]]]]: Conflict analysis results containing:
            - 'status': str - Either "conflict detected" or "clear"
            - 'conflicts': List[Dict[str, Any]] - List of conflict details, where each
              conflict dict contains:
                - 'with': str - Name of the conflicting drone
                - 'location': Tuple[float, float] - (x, y) coordinates of conflict
                - 'altitude': float - Z coordinate of conflict location
                - 'time': float - Timestamp when conflict occurs
                - 'distance': float - Actual separation distance at conflict
    
    Example:
        >>> primary_drone = DroneMission("Drone_A", waypoints_a)
        >>> other_drones = [DroneMission("Drone_B", waypoints_b)]
        >>> result = check_conflicts(primary_drone, other_drones, safety_radius=3.0)
        >>> if result['status'] == 'conflict detected':
        ...     print(f"Found {len(result['conflicts'])} conflicts")
    
    Algorithm:
        1. Compare each waypoint in the primary mission against every waypoint
           in each other mission
        2. Check temporal proximity: waypoints within ±5 seconds are considered
        3. Check spatial proximity: calculate 3D distance between waypoints
        4. Record conflict if distance < safety_radius and time difference ≤ 5s
    
    Notes:
        - Uses ±5 second time window for temporal conflict detection
        - Conflicts are recorded from the primary drone's perspective
        - Multiple conflicts can be detected with the same drone at different times
        - Returns empty conflicts list when no conflicts are found
    """
    conflicts: List[Dict[str, Any]] = []

    for other in others:
        for wp1 in primary.waypoints:
            for wp2 in other.waypoints:
                # Check temporal proximity (within 5 seconds)
                if abs(wp1.timestamp - wp2.timestamp) <= 5:
                    # Calculate spatial distance
                    d: float = distance(wp1.waypoint, wp2.waypoint)
                    
                    # Check if within safety radius
                    if d < safety_radius:
                        conflicts.append({
                            "with": other.name,
                            "location": (wp1.waypoint.x, wp1.waypoint.y),
                            "altitude": wp1.waypoint.z,
                            "time": wp1.timestamp,
                            "distance": d
                        })

    if conflicts:
        return {"status": "conflict detected", "conflicts": conflicts}
    return {"status": "clear", "conflicts": []}
