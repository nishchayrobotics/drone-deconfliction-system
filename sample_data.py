import random
from mission_data import Waypoint, TimedWaypoint, DroneMission

def generate_waypoints(count, base_time, base_x, base_y, base_z, time_gap=6):
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

def get_sample_missions():
    scenarios = ["conflict", "no_conflict", "edge_case_same_spot_different_time"]
    chosen_scenario = random.choice(scenarios)
    print(f"\n Running Scenario: {chosen_scenario}\n")

    # Primary Drone
    primary = DroneMission(
        name="PrimaryDrone",
        start_time=0,
        end_time=200,
        waypoints=generate_waypoints(15, 0, 0, 0, 10)
    )

    other_drones = []

    for i in range(6):  # Total 6 drones
        name = f"Drone{i+1}"

        if chosen_scenario == "conflict" and i % 2 == 0:
            # Conflict: overlap in both time and space
            wp = generate_waypoints(15, 0, 0, 0, 10)
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
            wp = generate_waypoints(15, 100, random.randint(30, 60), random.randint(30, 60), 25)

        drone = DroneMission(
            name=name,
            start_time=wp[0].timestamp,
            end_time=wp[-1].timestamp,
            waypoints=wp
        )

        other_drones.append(drone)

    return primary, other_drones
