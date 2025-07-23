# Drone Deconfliction System 🚁


## 🚀 Features

- ✅ **Spatial & Temporal Conflict Detection**
- ✅ **Conflict Explanation** (Location, Drone, and Time)
- ✅ **Sample Mission Generator** with multiple drones
- ✅ **2D & 4D Visualizations** using `matplotlib.animation`
- ✅ **Scenario Switching**: conflict, no-conflict, edge-case

## 📂 File Structure

├── sample_data.py # Auto-generated sample missions

├── mission_data.py # Data structure for missions

├── conflict_checker.py # Logic to detect spatial/temporal conflicts

├── visualizer.py # 2D visualization ( optional )

├── visualizer_4d.py # 4D animation (space + time)

├── main.py # Entry script to run selected scenarios

## 🧪 Scenarios

Choose in `sample_data.py`:
- `"conflict"`
- `"no_conflict"`
- `"edge_case_same_spot_different_time"`

## 📸 Output

- Blinking drones
- Persistent path line
- Dynamic titles (red for conflict, green for safe)
- Auto-generated sample missions

## 🧠 Built With

- Python 3.10+
- `matplotlib`
- `random`
- `dataclasses`

## 🤖 Author

**Nishchay Choudha**  
BTech, Electronics & Communication Engineering  
[VIT Vellore] | Robotics Scholar at RWTH Aachen University

---

## 🔗 GitHub

[https://github.com/nishchayrobotics/drone-deconfliction-system](https://github.com/nishchayrobotics/drone-deconfliction-system)
