from sample_data import get_sample_missions
from conflict_checker import check_conflicts
from visualizer_4d import animate_mission

primary, others = get_sample_missions()
result = check_conflicts(primary, others)

print("Status:", result['status'])
if result['conflicts']:
    for c in result['conflicts']:
        print(f"Conflict with {c['with']} at {c['location']} z={c['altitude']} at {c['time']}s")

# Run animation with result-aware titles
animate_mission(primary, others, result)