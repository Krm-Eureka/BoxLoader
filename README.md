# BoxLoader

## Features
1. Strict Priority Order for box placement.
2. Support ≥ Adaptive Threshold (45–50%).
3. Tightest Fit and Lowest Edge Waste placement strategy.
4. No 3D Rotation (only L×W and W×L orientations).
5. Layer-Based Placement.
6. Configurable GAP between boxes.
7. Exhaustive Priority placement.
8. 3D Visualization with volume utilization and pickup points.
9. Export placed and unplaced boxes to CSV.
10. Volume Utilization (%) displayed in 3D visualization.
11. Support for multiple container types (e.g., F15, F9, Pallet).

## Usage
Run `main.py` to start the program. Outputs include:
- `placed.csv`: Boxes successfully placed.
- `unplaced.csv`: Boxes that could not be placed.
