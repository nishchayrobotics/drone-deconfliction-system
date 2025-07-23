from data_class.mission_data_class import DroneMission
from typing import List, Dict, Any, Tuple, Union
import math
import logging

# Set up logging
logger = logging.getLogger(__name__)

def distance(p1: Any, p2: Any) -> float:
    """
    Calculate the 3D Euclidean distance between two waypoints with robust error handling.
    
    Computes the straight-line distance between two points in 3D space
    using the standard Euclidean distance formula: √[(x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²]
    
    Args:
        p1 (Any): First waypoint object with x, y, z coordinate attributes.
        p2 (Any): Second waypoint object with x, y, z coordinate attributes.
    
    Returns:
        float: The 3D Euclidean distance between the two waypoints in meters.
    
    Raises:
        AttributeError: If waypoint objects don't have required x, y, z attributes.
        ValueError: If coordinate values are not finite numbers.
        TypeError: If coordinate values are not numeric types.
    """
    # Input validation for p1
    if not hasattr(p1, 'x') or not hasattr(p1, 'y') or not hasattr(p1, 'z'):
        raise AttributeError("First waypoint must have x, y, z attributes")
    
    # Input validation for p2
    if not hasattr(p2, 'x') or not hasattr(p2, 'y') or not hasattr(p2, 'z'):
        raise AttributeError("Second waypoint must have x, y, z attributes")
    
    # Validate coordinate types and values for p1
    for coord_name, coord_value in [('x', p1.x), ('y', p1.y), ('z', p1.z)]:
        if not isinstance(coord_value, (int, float)):
            raise TypeError(f"First waypoint {coord_name} must be numeric, got {type(coord_value)}")
        if not math.isfinite(coord_value):
            raise ValueError(f"First waypoint {coord_name} must be a finite number, got {coord_value}")
    
    # Validate coordinate types and values for p2
    for coord_name, coord_value in [('x', p2.x), ('y', p2.y), ('z', p2.z)]:
        if not isinstance(coord_value, (int, float)):
            raise TypeError(f"Second waypoint {coord_name} must be numeric, got {type(coord_value)}")
        if not math.isfinite(coord_value):
            raise ValueError(f"Second waypoint {coord_name} must be a finite number, got {coord_value}")
    
    return math.sqrt(
        (p1.x - p2.x)**2 +
        (p1.y - p2.y)**2 +
        (p1.z - p2.z)**2
    )

def validate_waypoint_coordinates(waypoint: Any) -> None:
    """
    Validate a waypoint object for spatial coordinates only.
    
    Args:
        waypoint: Waypoint object with x, y, z coordinates
        
    Raises:
        AttributeError: If waypoint lacks required coordinate attributes
        TypeError: If coordinate values are not numeric
        ValueError: If coordinate values are not finite numbers
    """
    required_coords = ['x', 'y', 'z']
    
    for coord in required_coords:
        if not hasattr(waypoint, coord):
            raise AttributeError(f"Waypoint missing required coordinate: {coord}")
        
        value = getattr(waypoint, coord)
        if not isinstance(value, (int, float)):
            raise TypeError(f"Waypoint {coord} must be numeric, got {type(value)}")
        if not math.isfinite(value):
            raise ValueError(f"Waypoint {coord} must be a finite number, got {value}")

def check_conflicts(
    primary: DroneMission, 
    others: List[DroneMission], 
    safety_radius: float = 2.0,
    time_threshold: float = 5.0
) -> Dict[str, Union[str, List[Dict[str, Any]]]]:
    """
    Check for spatial and temporal conflicts between drone missions with robust error handling.
    
    Analyzes the primary drone's mission against other drone missions to identify
    potential conflicts where drones would be too close in both space and time.
    A conflict occurs when two drones are within the safety radius at similar times.
    
    Args:
        primary (DroneMission): The primary drone mission to check for conflicts.
            Must contain waypoints with coordinates and timestamps.
        others (List[DroneMission]): List of other drone missions to compare against.
            Each mission should contain waypoints with spatial and temporal data.
        safety_radius (float, optional): Minimum safe separation distance in meters.
            Defaults to 2.0 meters. Must be positive.
        time_threshold (float, optional): Maximum time difference in seconds for
            temporal conflict detection. Defaults to 5.0 seconds. Must be non-negative.
    
    Returns:
        Dict[str, Union[str, List[Dict[str, Any]]]]: Conflict analysis results containing:
            - 'status': str - Either "conflict detected" or "clear"
            - 'conflicts': List[Dict[str, Any]] - List of conflict details
    
    Raises:
        TypeError: If primary is not DroneMission or others is not a list of DroneMissions
        ValueError: If safety_radius <= 0 or time_threshold < 0
    """
    # Input validation - Type checks
    if not isinstance(primary, DroneMission):
        raise TypeError("primary must be a DroneMission instance")
    
    if not isinstance(others, list):
        raise TypeError("others must be a list")
    
    for i, other in enumerate(others):
        if not isinstance(other, DroneMission):
            raise TypeError(f"others[{i}] must be a DroneMission instance, got {type(other)}")
    
    # Parameter validation
    if not isinstance(safety_radius, (int, float)):
        raise TypeError("safety_radius must be numeric")
    if safety_radius <= 0:
        raise ValueError("safety_radius must be positive")
    
    if not isinstance(time_threshold, (int, float)):
        raise TypeError("time_threshold must be numeric")
    if time_threshold < 0:
        raise ValueError("time_threshold must be non-negative")
    
    # Handle empty missions
    if not hasattr(primary, 'waypoints') or not primary.waypoints:
        logger.info("Primary mission has no waypoints")
        return {"status": "clear", "conflicts": []}
    
    # Check if all other missions are empty
    valid_others = [other for other in others if hasattr(other, 'waypoints') and other.waypoints]
    if not valid_others:
        logger.info("No other missions with waypoints found")
        return {"status": "clear", "conflicts": []}
    
    conflicts: List[Dict[str, Any]] = []
    
    # Validate primary mission waypoints - FIXED VERSION
    try:
        for timed_wp in primary.waypoints:
            # Validate the waypoint coordinates (x, y, z)
            if hasattr(timed_wp, 'waypoint'):
                validate_waypoint_coordinates(timed_wp.waypoint)
            # Validate the timestamp
            if hasattr(timed_wp, 'timestamp'):
                if not isinstance(timed_wp.timestamp, (int, float)):
                    raise TypeError(f"Timestamp must be numeric, got {type(timed_wp.timestamp)}")
                if not math.isfinite(timed_wp.timestamp):
                    raise ValueError(f"Timestamp must be finite, got {timed_wp.timestamp}")
    except (AttributeError, TypeError, ValueError) as e:
        logger.error(f"Invalid waypoint in primary mission: {e}")
        raise ValueError(f"Primary mission contains invalid waypoint: {e}")
    
    # Check conflicts with controlled exception handling
    for other in valid_others:
        try:
            # Validate other mission waypoints - FIXED VERSION
            for timed_wp in other.waypoints:
                if hasattr(timed_wp, 'waypoint'):
                    validate_waypoint_coordinates(timed_wp.waypoint)
                if hasattr(timed_wp, 'timestamp'):
                    if not isinstance(timed_wp.timestamp, (int, float)):
                        raise TypeError(f"Timestamp must be numeric, got {type(timed_wp.timestamp)}")
                    if not math.isfinite(timed_wp.timestamp):
                        raise ValueError(f"Timestamp must be finite, got {timed_wp.timestamp}")
            
            # Perform conflict detection for this mission
            for wp1 in primary.waypoints:
                for wp2 in other.waypoints:
                    try:
                        # Check temporal proximity
                        time_diff = abs(wp1.timestamp - wp2.timestamp)
                        if time_diff <= time_threshold:
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
                    except (AttributeError, TypeError, ValueError) as e:
                        logger.warning(f"Error processing waypoint pair in {other.name}: {e}")
                        continue
                        
        except (AttributeError, TypeError, ValueError) as e:
            logger.warning(f"Skipping mission {getattr(other, 'name', 'Unknown')}: {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error processing mission {getattr(other, 'name', 'Unknown')}: {e}")
            continue
    
    # Return results
    if conflicts:
        return {"status": "conflict detected", "conflicts": conflicts}
    return {"status": "clear", "conflicts": []}
