from mission_data import DroneMission
import math

def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x)**2 +
        (p1.y - p2.y)**2 +
        (p1.z - p2.z)**2
    )

def check_conflicts(primary: DroneMission, others: list, safety_radius=2.0):
    conflicts = []

    for other in others:
        for wp1 in primary.waypoints:
            for wp2 in other.waypoints:
                if abs(wp1.timestamp - wp2.timestamp) <= 5:
                    d = distance(wp1.waypoint, wp2.waypoint)
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
