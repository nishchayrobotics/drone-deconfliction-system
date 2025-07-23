import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import List, Dict, Any, Union, Tuple
from data_class.mission_data_class import DroneMission


def plot_missions(
    primary: DroneMission, 
    others: List[DroneMission], 
    conflicts: List[Dict[str, Any]] = None
) -> None:
    """
    Plot multiple drone missions and their conflicts in 3D space.
    
    Creates a static 3D visualization showing drone flight paths and conflict
    locations. The primary drone is displayed with a solid blue line and markers,
    while other drones are shown with dashed lines. Conflicts are marked with
    red 'X' symbols and labeled with conflict details.
    
    Args:
        primary (DroneMission): The primary drone mission to visualize.
            Must contain waypoints with x, y, z coordinates.
        others (List[DroneMission]): List of additional DroneMission objects
            representing other drones in the simulation.
        conflicts (List[Dict[str, Any]], optional): List of conflict dictionaries.
            Each conflict dict should contain:
            - 'location': Tuple[float, float] - (x, y) coordinates
            - 'with': str - Name of conflicting drone
            - 'time': float - Timestamp of conflict
            - 'altitude': float (optional) - Z coordinate, defaults to 0
    
    Returns:
        None: Displays a matplotlib 3D plot window.
    
    Example:
        >>> primary_drone = DroneMission("Drone_A", waypoints_list)
        >>> other_drones = [DroneMission("Drone_B", waypoints_b)]
        >>> conflict_data = [
        ...     {
        ...         'location': (25.5, 30.2),
        ...         'with': 'Drone_B',
        ...         'time': 15.0,
        ...         'altitude': 20.0
        ...     }
        ... ]
        >>> plot_missions(primary_drone, other_drones, conflict_data)
    
    Notes:
        - Primary drone path is displayed as blue circles connected by solid lines
        - Other drone paths are displayed as dashed lines with default colors
        - Conflict markers are red 'X' symbols with text labels
        - Plot includes legend, axis labels, and title
        - Requires matplotlib with 3D plotting support
    """
    if conflicts is None:
        conflicts = []
    
    fig: Figure = plt.figure(figsize=(10, 8))
    ax: Axes = fig.add_subplot(111, projection='3d')

    # Plot Primary Drone Path
    x: List[float] = [wp.waypoint.x for wp in primary.waypoints]
    y: List[float] = [wp.waypoint.y for wp in primary.waypoints]
    z: List[float] = [wp.waypoint.z for wp in primary.waypoints]
    ax.plot(x, y, z, 'bo-', label=primary.name)

    # Other Drones
    for drone in others:
        x = [wp.waypoint.x for wp in drone.waypoints]
        y = [wp.waypoint.y for wp in drone.waypoints]
        z = [wp.waypoint.z for wp in drone.waypoints]
        ax.plot(x, y, z, '--', label=drone.name)

    # Conflicts
    for c in conflicts:
        conflict_x: float
        conflict_y: float
        conflict_x, conflict_y = c['location']
        conflict_altitude: float = c.get('altitude', 0)
        
        ax.scatter(
            conflict_x, 
            conflict_y, 
            conflict_altitude, 
            c='r', 
            marker='x', 
            s=100
        )
        ax.text(
            conflict_x + 0.5, 
            conflict_y + 0.5, 
            conflict_altitude + 0.5,
            f"{c['with']} @ {c['time']}s", 
            color='red'
        )

    ax.set_title("3D Drone Missions & Conflicts")
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Altitude (Z)')
    ax.legend()
    plt.show()