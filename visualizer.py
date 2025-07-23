import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mission_data import DroneMission

def plot_missions(primary: DroneMission, others: list, conflicts=[]):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot Primary Drone Path
    x = [wp.waypoint.x for wp in primary.waypoints]
    y = [wp.waypoint.y for wp in primary.waypoints]
    z = [wp.waypoint.z for wp in primary.waypoints]
    ax.plot(x, y, z, 'bo-', label=primary.name)

    # Other Drones
    for drone in others:
        x = [wp.waypoint.x for wp in drone.waypoints]
        y = [wp.waypoint.y for wp in drone.waypoints]
        z = [wp.waypoint.z for wp in drone.waypoints]
        ax.plot(x, y, z, '--', label=drone.name)

    # Conflicts
    for c in conflicts:
        x, y = c['location']
        ax.scatter(x, y, c.get('altitude', 0), c='r', marker='x', s=100)
        ax.text(x+0.5, y+0.5, c.get('altitude', 0)+0.5,
                f"{c['with']} @ {c['time']}s", color='red')

    ax.set_title("3D Drone Missions & Conflicts")
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Altitude (Z)')
    ax.legend()
    plt.show()
