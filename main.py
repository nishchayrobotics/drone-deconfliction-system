from typing import List, Dict, Any
from test.generated_data import get_sample_missions
from core.conflict_checker import check_conflicts
from visualizer.visualizer_4d import animate_mission


def main() -> None:
    """
    Main function to demonstrate drone mission conflict detection and visualization.
    
    This function orchestrates the complete workflow for drone mission analysis:
    1. Generates sample drone missions with various scenarios
    2. Analyzes missions for spatial-temporal conflicts
    3. Displays conflict results in console output
    4. Launches 4D animation visualization with conflict-aware display
    
    The function integrates three main components:
    - Mission generation (test scenarios)
    - Conflict detection (safety analysis)
    - 4D visualization (animated display)
    
    Returns:
        None: Outputs results to console and displays interactive animation.
    
    Example Output:
        Running Scenario: conflict
        
        Status: conflict detected
        Conflict with Drone1 at (2.5, 1.8) z=11.2 at 12.0s
        Conflict with Drone3 at (5.1, 4.2) z=9.8 at 24.0s
        
        [Opens 4D animation window with red title indicating conflicts]
    
    Notes:
        - Scenario selection is randomized each run
        - Console output shows all detected conflicts with details
        - Animation title color reflects conflict status (red/green)
        - Animation continues until all waypoints are completed
    """
    # Generate sample missions based on random scenario
    primary, others = get_sample_missions()
    
    # Analyze missions for conflicts
    result: Dict[str, Any] = check_conflicts(primary, others)

    # Display conflict analysis results
    print("Status:", result['status'])
    if result['conflicts']:
        conflict: Dict[str, Any]
        for conflict in result['conflicts']:
            print(f"Conflict with {conflict['with']} at {conflict['location']} "
                  f"z={conflict['altitude']} at {conflict['time']}s")

    # Launch 4D visualization with conflict-aware display
    animate_mission(primary, others, result)


if __name__ == "__main__":
    main()
