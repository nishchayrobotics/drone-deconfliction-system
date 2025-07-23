import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import List, Dict, Tuple, Optional, Any
from data_class.mission_data_class import DroneMission


def animate_mission(
    primary: DroneMission, 
    others: List[DroneMission], 
    conflict_result: Optional[Dict[str, Any]] = None
) -> None:
    """
    Animate multiple drone missions in 4D space (3D position + time).
    
    This function creates an interactive 3D animation showing drone trajectories
    and real-time positions. It visualizes potential spatial-temporal conflicts
    between multiple drones operating in shared airspace.
    
    Args:
        primary (DroneMission): The primary drone mission to visualize.
            Must contain waypoints with x, y, z coordinates and timestamps.
        others (List[DroneMission]): List of additional DroneMission objects 
            representing other drones in the simulation.
        conflict_result (Optional[Dict[str, Any]]): Dictionary containing conflict 
            detection results. If present and contains {'status': 'conflict detected'},
            the title will be displayed in red, otherwise green.
    
    Returns:
        None: Displays an interactive matplotlib animation window.
    
    Example:
        >>> primary_drone = DroneMission("Drone_A", waypoints_list)
        >>> other_drones = [DroneMission("Drone_B", waypoints_b)]
        >>> conflict_info = {"status": "conflict detected"}
        >>> animate_mission(primary_drone, other_drones, conflict_info)
    
    Notes:
        - Animation updates every 500ms with 2-second time steps
        - Supports up to 8 drones with distinct colors
        - Axis limits are fixed: X[0,70], Y[0,70], Z[0,50]
        - Position matching uses ±1 second tolerance
    """
    fig: Figure = plt.figure(figsize=(10, 8))
    ax: Axes = fig.add_subplot(111, projection='3d')

    all_drones: List[DroneMission] = [primary] + others
    drone_colors: List[str] = ['b', 'g', 'm', 'c', 'y', 'k', 'orange', 'purple']
    drone_paths: Dict[str, Tuple[List[float], List[float], List[float]]] = {}

    # Prepare all full paths first
    for idx, drone in enumerate(all_drones):
        xs: List[float] = [wp.waypoint.x for wp in drone.waypoints]
        ys: List[float] = [wp.waypoint.y for wp in drone.waypoints]
        zs: List[float] = [wp.waypoint.z for wp in drone.waypoints]
        drone_paths[drone.name] = (xs, ys, zs)

    # Build static legend handles
    legend_handles: List[Any] = []
    for idx, drone in enumerate(all_drones):
        color: str = drone_colors[idx % len(drone_colors)]
        dummy_line, = ax.plot([], [], [], color=color, label=drone.name)
        legend_handles.append(dummy_line)

    max_time: float = max(wp.timestamp for d in all_drones for wp in d.waypoints)

    def get_position_at_time(drone: DroneMission, current_time: float) -> Optional[Any]:
        """
        Find drone's position at a specific time.
        
        Searches through the drone's waypoints to find a position that matches
        the given time within a tolerance window.
        
        Args:
            drone (DroneMission): The drone mission object containing waypoints.
            current_time (float): The target timestamp to find position for.
        
        Returns:
            Optional[Any]: The waypoint position if found within ±1 second
            tolerance, otherwise None.
        
        Notes:
            - Uses ±1 second tolerance for timestamp matching
            - Returns the first matching waypoint found
        """
        for wp in drone.waypoints:
            if abs(wp.timestamp - current_time) <= 1:
                return wp.waypoint
        return None

    def update(frame_time: int) -> None:
        """
        Update function for animation frames.
        
        Called by FuncAnimation for each frame to update the 3D plot display.
        Clears the previous frame and redraws all drone paths, current positions,
        and plot elements.
        
        Args:
            frame_time (int): Current simulation time in seconds for this frame.
        
        Returns:
            None: Modifies the matplotlib axis object in place.
        
        Side Effects:
            - Clears and redraws the entire 3D plot
            - Updates plot title with current time and conflict status
            - Draws drone trajectories as dashed lines
            - Plots current drone positions as colored dots
            - Updates legend display
        """
        ax.clear()
        ax.set_xlim(0, 70)
        ax.set_ylim(0, 70)
        ax.set_zlim(0, 50)

        title: str = f"4D Drone Conflict Simulation – Time: {frame_time}s"
        if conflict_result and conflict_result['status'] == 'conflict detected':
            ax.set_title(title, color='red')
        else:
            ax.set_title(title, color='green')

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Altitude (Z)")

        for idx, drone in enumerate(all_drones):
            color: str = drone_colors[idx % len(drone_colors)]
            xs, ys, zs = drone_paths[drone.name]

            # Draw full path (static)
            ax.plot(xs, ys, zs, color=color, linestyle='--', linewidth=1.5, alpha=0.5)

            # Draw current position as blinking dot
            pos: Optional[Any] = get_position_at_time(drone, frame_time)
            if pos:
                ax.scatter(pos.x, pos.y, pos.z, color=color, s=60)

        # Draw legend only once using static dummy handles
        ax.legend(handles=legend_handles, loc='upper left')

    ani: FuncAnimation = FuncAnimation(
        fig, 
        update, 
        frames=range(0, int(max_time) + 1, 2), 
        interval=500
    )
    plt.show()
