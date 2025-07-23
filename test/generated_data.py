import random
from data_class.mission_data_class import Waypoint, TimedWaypoint, DroneMission
from typing import List, Tuple, Literal


def generate_waypoints(
    count: int, 
    base_time: float, 
    base_x: float, 
    base_y: float, 
    base_z: float, 
    time_gap: float = 6
) -> List[TimedWaypoint]:
    """
    Generate a sequence of waypoints with randomized spatial variations.
    
    Creates a list of TimedWaypoint objects that form a drone's flight path.
    Each waypoint is positioned with slight random variations from a base trajectory,
    creating realistic flight patterns with temporal spacing.
    
    Args:
        count (int): Number of waypoints to generate for the mission.
        base_time (float): Starting timestamp for the first waypoint in seconds.
        base_x (float): Base X coordinate that waypoints will deviate from.
        base_y (float): Base Y coordinate that waypoints will deviate from.
        base_z (float): Base altitude (Z coordinate) that waypoints will vary around.
        time_gap (float, optional): Time interval between consecutive waypoints
            in seconds. Defaults to 6 seconds.
    
    Returns:
        List[TimedWaypoint]: A list of waypoints with coordinates and timestamps,
        where each waypoint includes:
        - Spatial position with random variations from base coordinates
        - Sequential timestamps separated by time_gap intervals
    
    Example:
        >>> waypoints = generate_waypoints(5, 0, 10, 20, 30, time_gap=8)
        >>> len(waypoints)
        5
        >>> waypoints[0].timestamp
        0
        >>> waypoints[1].timestamp
        8
    
    Notes:
        - X and Y coordinates increase progressively with random variations (1-3 units)
        - Z coordinate varies randomly within ±2 units of base_z
        - Timestamps are strictly sequential with consistent time gaps
        - Uses random.uniform() for smooth coordinate variations
    """
    return [
        TimedWaypoint(
            waypoint=Waypoint(
                base_x + i * random.uniform(1, 3),
                base_y + i * random.uniform(1, 3),
                base_z + random.uniform(-2, 2)
            ),
            timestamp=base_time + i * time_gap
        )
        for i in range(count)
    ]


def get_sample_missions() -> Tuple[DroneMission, List[DroneMission]]:
    """
    Generate sample drone missions for testing conflict detection scenarios.
    
    Creates a primary drone mission and multiple other drone missions based on
    randomly selected scenarios. This function is designed for testing and
    demonstrating different conflict detection cases in drone airspace management.
    
    Returns:
        Tuple[DroneMission, List[DroneMission]]: A tuple containing:
        - DroneMission: The primary drone mission starting at origin (0,0,10)
        - List[DroneMission]: List of 6 additional drone missions with scenarios
          determined by the randomly chosen test case
    
    Scenarios:
        - **conflict**: Even-numbered drones (0, 2, 4) follow the same path as primary
          at the same time, creating spatial-temporal conflicts
        - **no_conflict**: All drones operate in different areas (coordinates 30-60)
          and different time windows (starting at t=100)
        - **edge_case_same_spot_different_time**: Even-numbered drones follow the
          same spatial path as primary but with 40-second time offset
    
    Example:
        >>> primary, others = get_sample_missions()
        >>> primary.name
        'PrimaryDrone'
        >>> len(others)
        6
        >>> others[0].name
        'Drone1'
    
    Mission Characteristics:
        - **Primary drone**: 15 waypoints, starts at (0,0,10), mission duration 0-200s
        - **Conflict drones**: Same path as primary, potential conflicts
        - **Safe drones**: Different area (30-60 range), later time window (100s+)
        - **Edge case drones**: Same path, time-shifted by 40 seconds
    
    Notes:
        - Randomly selects one of three predefined scenarios each run
        - Prints the chosen scenario for debugging and demonstration
        - All missions have 15 waypoints with 6-second intervals
        - Uses deterministic patterns within each scenario for reproducible testing
        - Mission start/end times are automatically calculated from waypoint timestamps
    """
    scenarios: List[Literal["conflict", "no_conflict", "edge_case_same_spot_different_time"]] = [
        "conflict", 
        "no_conflict", 
        "edge_case_same_spot_different_time"
    ]
    chosen_scenario: str = random.choice(scenarios)
    print(f"\n Running Scenario: {chosen_scenario}\n")

    # Primary Drone
    primary: DroneMission = DroneMission(
        name="PrimaryDrone",
        start_time=0,
        end_time=200,
        waypoints=generate_waypoints(15, 0, 0, 0, 10)
    )

    other_drones: List[DroneMission] = []

    for i in range(6):  # Total 6 drones
        name: str = f"Drone{i+1}"

        if chosen_scenario == "conflict" and i % 2 == 0:
            # Conflict: overlap in both time and space
            wp: List[TimedWaypoint] = generate_waypoints(15, 0, 0, 0, 10)
        elif chosen_scenario == "edge_case_same_spot_different_time" and i % 2 == 0:
            # Same path as primary, but different times
            wp = [
                TimedWaypoint(
                    waypoint=primary.waypoints[j].waypoint,
                    timestamp=primary.waypoints[j].timestamp + 40  # shift time
                )
                for j in range(15)
            ]
        else:
            # No conflict: different area or time
            wp = generate_waypoints(
                15, 
                100, 
                random.randint(30, 60), 
                random.randint(30, 60), 
                25
            )

        drone: DroneMission = DroneMission(
            name=name,
            start_time=wp[0].timestamp,
            end_time=wp[-1].timestamp,
            waypoints=wp
        )

        other_drones.append(drone)

    return primary, other_drones