# A* Pathfinding Visualizer

This project implements the A* (A-star) pathfinding algorithm on a 2D maze and visualizes the shortest path using `pygame`. The maze includes obstacles and weighted paths to simulate real-world terrain.

## Features

- A* algorithm implementation with a Euclidean heuristic
- Randomly generated 50x50 grid maze with customizable obstacles and weighted paths
- Real-time visualization of the shortest path
- Adjustable parameters for maze generation



## Requirements

- Python 3.x
- pygame

You can install `pygame` using:

```bash
pip install pygame
```

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/a-star-visualizer.git
    cd a-star-visualizer
    ```

2. Run the script:
    ```bash
    python A_Star.py
    ```

The window will display the maze and animate the path from the start `(0, 0)` to the goal `(49, 49)`.

## File Overview

- **`A_Star.py`**: Main script containing:
  - A* algorithm (`a_star`)
  - Maze and graph generation
  - Path reconstruction and visualization
- **Functions**:
  - `create_maze()`: Generates the 2D maze
  - `create_graph()`: Converts maze to graph format
  - `a_star()`: Runs the pathfinding
  - `visualize_path()`: Uses `pygame` to show the path in real-time

## Maze Representation

- `'1'`: Normal path  
- `'#'`: Obstacle  
- `2-5`: Weighted paths (higher traversal cost)


