# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Greedy maze solver for all entrance, exit pairs
#
# __author__ = <Your Name>
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze
from typing import List, Tuple
import heapq




class greedySolver():
    
    def __init__(self):
       
        # TODO: Implement this for task C!
        self.entrance_exit_paths = {}  # Stores paths for each entrance-exit pair
        self.all_solved = False
        
    
    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]):
        # TODO: Implement this for task C!
        # Initialize variables to track visited cells
        visited_cells = set()
        paths = {}

        # For each entrance, calculate the shortest paths to all exits
        for entrance in entrances:
            # Use a priority queue to store paths and prioritize by path cost (greedy approach)
            exit_paths = []
            for exit in exits:
                path, cost = self.findShortestPath(maze, entrance, exit)
                if path:
                    heapq.heappush(exit_paths, (cost, id(exit), path, exit))  # Use id(exit) as a tie-breaker

            # Find the first non-overlapping path for this entrance
            while exit_paths:
                cost, _, path, exit = heapq.heappop(exit_paths)
                path_set = set(path)

                # Ensure no overlap with previously selected paths
                if visited_cells & path_set:
                    continue  # Skip overlapping paths
                # Otherwise, select this path and mark cells as visited
                paths[(entrance, exit)] = path
                visited_cells.update(path_set)
                break  # Move to the next entrance

        # Update attributes with the selected paths
        self.entrance_exit_paths = paths
        self.all_solved = len(paths) == len(entrances)  # True if all entrances have a path

    def findShortestPath(self, maze: Maze, entrance: Coordinates, exit: Coordinates) -> Tuple[List[Coordinates], int]:
        # Dijkstra-style approach for finding shortest path between entrance and exit
        distances = {coord: float('inf') for coord in maze.getCoords()}
        distances[entrance] = 0
        priority_queue = [(0, id(entrance), entrance)]
        predecessors = {entrance: None}

        while priority_queue:
            current_distance, _, current_cell = heapq.heappop(priority_queue)

            if current_cell == exit:
                break

            for neighbor in maze.neighbours(current_cell):
                # Check for a wall between current_cell and neighbor
                if maze.hasWall(current_cell, neighbor):
                    continue  # Skip this neighbor if there is a wall

                weight = maze.edgeWeight(current_cell, neighbor)
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_cell
                    heapq.heappush(priority_queue, (distance, id(neighbor), neighbor))

        # Backtrack to construct the path
        path = []
        step = exit
        while step is not None:
            path.append(step)
            step = predecessors.get(step)
        path.reverse()

        return path, distances[exit]
