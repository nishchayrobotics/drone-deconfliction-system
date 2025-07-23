# automated_test_runner.py
import os
import json
import sys
import traceback
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime

from core.conflict_checker import check_conflicts
from data_class.mission_data_class import DroneMission, TimedWaypoint, Waypoint

@dataclass
class TestResult:
    test_id: str
    test_name: str
    expected: str
    actual: str
    passed: bool
    execution_time: float
    error_message: str = None
    conflict_details: List[Dict] = None

class DroneConflictTestRunner:
    def __init__(self, test_scenarios_file: str = 'test_scenarios.json'):
        """Initialize the test runner with test scenarios from JSON file."""
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # If the file path is relative, make it relative to the script directory
        if not os.path.isabs(test_scenarios_file):
            self.test_scenarios_file = os.path.join(script_dir, test_scenarios_file)
        else:
            self.test_scenarios_file = test_scenarios_file
            
        self.test_results: List[TestResult] = []
        self.scenarios = self.load_test_scenarios()
        
    def load_test_scenarios(self) -> Dict:
        """Load test scenarios from JSON file."""
        try:
            with open(self.test_scenarios_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Provide more helpful error message
            print(f"Error: Test scenarios file '{self.test_scenarios_file}' not found.")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
            print("Please ensure test_scenarios.json is in the same directory as automated_test_runner.py")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{self.test_scenarios_file}': {e}")
            sys.exit(1)
    
    def create_mission_from_json(self, mission_data: Dict) -> DroneMission:
        """Convert JSON mission data to DroneMission object."""
        waypoints = []
        for wp_data in mission_data['waypoints']:
            waypoint = Waypoint(
                x=wp_data['waypoint']['x'],
                y=wp_data['waypoint']['y'],
                z=wp_data['waypoint']['z']
            )
            timed_waypoint = TimedWaypoint(
                waypoint=waypoint,
                timestamp=wp_data['timestamp']
            )
            waypoints.append(timed_waypoint)
        
        return DroneMission(
            name=mission_data['name'],
            waypoints=waypoints,
            start_time=mission_data['start_time'],
            end_time=mission_data['end_time']
        )
    
    def run_single_test(self, scenario: Dict) -> TestResult:
        """Run a single test scenario."""
        start_time = datetime.now()
        
        try:
            # Create primary mission
            primary_mission = self.create_mission_from_json(scenario['primary_mission'])
            
            # Create other missions
            other_missions = []
            for mission_data in scenario['other_missions']:
                mission = self.create_mission_from_json(mission_data)
                other_missions.append(mission)
            
            # Run conflict detection
            result = check_conflicts(
                primary_mission, 
                other_missions,
                safety_radius=self.scenarios['metadata'].get('safety_radius', 2.0)
            )
            
            # Calculate execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Determine if test passed
            expected = scenario['expected_result']
            actual = result['status']
            passed = (expected == actual) or (expected == 'conflict_detected' and actual == 'conflict detected')
            
            return TestResult(
                test_id=scenario['id'],
                test_name=scenario['name'],
                expected=expected,
                actual=actual,
                passed=passed,
                execution_time=execution_time,
                conflict_details=result.get('conflicts', [])
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return TestResult(
                test_id=scenario['id'],
                test_name=scenario['name'],
                expected=scenario['expected_result'],
                actual='ERROR',
                passed=False,
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def run_all_tests(self) -> List[TestResult]:
        """Run all test scenarios."""
        print("=" * 80)
        print("DRONE CONFLICT DETECTION - AUTOMATED TEST SUITE")
        print("=" * 80)
        print(f"Test Suite Version: {self.scenarios['metadata']['version']}")
        print(f"Safety Radius: {self.scenarios['metadata']['safety_radius']}")
        print(f"Time Threshold: {self.scenarios['metadata']['time_threshold']}")
        print(f"Total Test Cases: {len(self.scenarios['scenarios'])}")
        print("=" * 80)
        
        for i, scenario in enumerate(self.scenarios['scenarios'], 1):
            print(f"\nRunning Test {i}/{len(self.scenarios['scenarios'])}: {scenario['id']} - {scenario['name']}")
            print(f"Description: {scenario['description']}")
            
            result = self.run_single_test(scenario)
            self.test_results.append(result)
            
            # Print immediate result
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"Result: {status} (Expected: {result.expected}, Got: {result.actual})")
            print(f"Execution Time: {result.execution_time:.4f}s")
            
            if result.error_message:
                print(f"Error: {result.error_message}")
            
            if result.conflict_details:
                print(f"Conflicts Found: {len(result.conflict_details)}")
                for conflict in result.conflict_details:
                    print(f"  - With {conflict['with']} at {conflict['location']} (altitude: {conflict['altitude']}) at time {conflict['time']}")
        
        return self.test_results
    
    def generate_test_report(self) -> str:
        """Generate a comprehensive test report."""
        if not self.test_results:
            return "No test results available. Run tests first."
        
        passed_tests = [r for r in self.test_results if r.passed]
        failed_tests = [r for r in self.test_results if not r.passed]
        error_tests = [r for r in self.test_results if r.error_message]
        
        total_time = sum(r.execution_time for r in self.test_results)
        
        report = []
        report.append("\n" + "=" * 80)
        report.append("TEST EXECUTION SUMMARY")
        report.append("=" * 80)
        report.append(f"Total Tests: {len(self.test_results)}")
        report.append(f"Passed: {len(passed_tests)} ({len(passed_tests)/len(self.test_results)*100:.1f}%)")
        report.append(f"Failed: {len(failed_tests)} ({len(failed_tests)/len(self.test_results)*100:.1f}%)")
        report.append(f"Errors: {len(error_tests)}")
        report.append(f"Total Execution Time: {total_time:.4f}s")
        report.append(f"Average Test Time: {total_time/len(self.test_results):.4f}s")
        
        if failed_tests:
            report.append("\n" + "=" * 40)
            report.append("FAILED TESTS DETAILS")
            report.append("=" * 40)
            for test in failed_tests:
                report.append(f"\n❌ {test.test_id}: {test.test_name}")
                report.append(f"   Expected: {test.expected}")
                report.append(f"   Actual: {test.actual}")
                if test.error_message:
                    report.append(f"   Error: {test.error_message}")
        
        return "\n".join(report)
    
    def save_results_json(self, filename: str = 'test_results.json'):
        """Save test results to JSON file."""
        results_data = {
            "metadata": {
                "test_run_timestamp": datetime.now().isoformat(),
                "total_tests": len(self.test_results),
                "passed_tests": len([r for r in self.test_results if r.passed]),
                "failed_tests": len([r for r in self.test_results if not r.passed]),
                "total_execution_time": sum(r.execution_time for r in self.test_results)
            },
            "results": []
        }
        
        for result in self.test_results:
            results_data["results"].append({
                "test_id": result.test_id,
                "test_name": result.test_name,
                "expected": result.expected,
                "actual": result.actual,
                "passed": result.passed,
                "execution_time": result.execution_time,
                "error_message": result.error_message,
                "conflict_details": result.conflict_details
            })
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2)
        
        print(f"\nTest results saved to: {filename}")

def main():
    """Main function to run the automated tests."""
    runner = DroneConflictTestRunner()
    
    # Run all tests
    results = runner.run_all_tests()
    
    # Generate and print report
    report = runner.generate_test_report()
    print(report)
    
    # Save results to JSON
    runner.save_results_json()
    
    # Exit with appropriate code
    failed_count = len([r for r in results if not r.passed])
    sys.exit(1 if failed_count > 0 else 0)

if __name__ == "__main__":
    main()
