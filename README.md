# Crafting Simulator

## Overview
This Python program simulates a crafting system based on specified recipes. It allows users to determine how to achieve a desired goal state of inventory items by applying various crafting recipes. 

## Features
- **State Management**: Tracks the current inventory and its state.
- **Recipe Checking**: Validates if crafting recipes can be applied based on current inventory.
- **Heuristic Search**: Finds the most efficient path to reach the desired goal state using a heuristic approach.

## Getting Started

### Requirements
- Python 3.x
- JSON file (`crafting.json`) with crafting recipes and inventory details.

### Structure
- **`Recipe`**: A named tuple representing a crafting recipe with attributes: `name`, `check`, `effect`, and `cost`.
- **`State`**: A custom class extending `OrderedDict` to manage inventory states with hashing capabilities.
- **Functions**:
  - `make_checker(rule)`: Returns a function to check if a state meets the recipe's requirements.
  - `make_effector(rule)`: Returns a function that updates the state based on the recipe's effect.
  - `make_goal_checker(goal)`: Returns a function that checks if the goal state has been met.
  - `graph(state)`: Generates possible crafting actions based on the current state.
  - `heuristic(state)`: Evaluates the cost of reaching the goal from the current state.
  - `search(graph, state, is_goal, limit, heuristic)`: Executes the search for a path to the goal state.

## Usage

1. **Prepare the JSON File**: Create a `crafting.json` file containing:
   - **Items**: List of all items available.
   - **Initial**: Inventory with the initial amounts of each item.
   - **Goal**: Desired inventory state at the end.
   - **Recipes**: Crafting rules that define how items can be crafted.

   Example structure of `crafting.json`:
   ```json
   {
       "Items": ["wood", "stone", "iron", ...],
       "Initial": {"wood": 10, "stone": 5, ...},
       "Goal": {"iron_pickaxe": 1, ...},
       "Recipes": {
           "craft stone_pickaxe at bench": {
               "Consumes": {"wood": 3, "stone": 2},
               "Produces": {"stone_pickaxe": 1},
               "Time": 5
           },
           ...
       }
   }
2. Run the Script: Execute the Python script. It will read the crafting.json file, check the current state, and search for a plan to reach the goal.
```bash
python crafting_simulator.py

3. Output: The resulting crafting plan will be printed, showing the sequence of actions and resulting states.

## Limitations
- The search has a time limit (default: 30 seconds), which may restrict finding solutions for complex scenarios.
- Heuristic evaluations can be adjusted for optimization.

## License
- This project is licensed under the MIT License.


