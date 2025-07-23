import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from mission_data import DroneMission

def animate_mission(primary: DroneMission, others: list, conflict_result=None):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    all_drones = [primary] + others
    drone_colors = ['b', 'g', 'm', 'c', 'y', 'k', 'orange', 'purple']
    drone_paths = {}

    # Prepare all full paths first
    for idx, drone in enumerate(all_drones):
        xs = [wp.waypoint.x for wp in drone.waypoints]
        ys = [wp.waypoint.y for wp in drone.waypoints]
        zs = [wp.waypoint.z for wp in drone.waypoints]
        drone_paths[drone.name] = (xs, ys, zs)

    # Build static legend handles
    legend_handles = []
    for idx, drone in enumerate(all_drones):
        color = drone_colors[idx % len(drone_colors)]
        dummy_line, = ax.plot([], [], [], color=color, label=drone.name)
        legend_handles.append(dummy_line)

    max_time = max(wp.timestamp for d in all_drones for wp in d.waypoints)

    def get_position_at_time(drone, current_time):
        for wp in drone.waypoints:
            if abs(wp.timestamp - current_time) <= 1:
                return wp.waypoint
        return None

    def update(frame_time):
        ax.clear()
        ax.set_xlim(0, 70)
        ax.set_ylim(0, 70)
        ax.set_zlim(0, 50)

        title = f"4D Drone Conflict Simulation – Time: {frame_time}s"
        if conflict_result and conflict_result['status'] == 'conflict detected':
            ax.set_title(title, color='red')
        else:
            ax.set_title(title, color='green')

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Altitude (Z)")

        for idx, drone in enumerate(all_drones):
            color = drone_colors[idx % len(drone_colors)]
            xs, ys, zs = drone_paths[drone.name]

            # Draw full path (static)
            ax.plot(xs, ys, zs, color=color, linestyle='--', linewidth=1.5, alpha=0.5)

            # Draw current position as blinking dot
            pos = get_position_at_time(drone, frame_time)
            if pos:
                ax.scatter(pos.x, pos.y, pos.z, color=color, s=60)

        # Draw legend only once using static dummy handles
        ax.legend(handles=legend_handles, loc='upper left')

    ani = FuncAnimation(fig, update, frames=range(0, int(max_time) + 1, 2), interval=500)
    plt.show()
