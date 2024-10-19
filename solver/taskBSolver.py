# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Brute force maze solver for all entrance, exit pairs
#
# __author__ = '<Your Name>
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.util import Coordinates
from maze.maze import Maze
from itertools import permutations
from typing import List, Tuple, Dict


class bruteForceSolver():
   
    def __init__(self):
        # TODO: Implement this for task B!
        self.all_solved = False
        self.entrance_exit_paths = {}  # Stores the optimal paths for each entrance-exit pair

    def solveMaze(self, maze: Maze, entrances: List[Coordinates], exits: List[Coordinates]):
        # TODO: Implement this for task B!
        min_total_cost = float('inf')
        best_paths = {}

        # Generate all permutations of exits for entrance-exit pairing
        for exit_permutation in permutations(exits):
            current_paths = {}
            visited_cells = set()
            total_cost = 0
            valid_paths = True

            # Attempt to find a path for each entrance paired with a respective exit
            for entrance, exit in zip(entrances, exit_permutation):
                path, path_cost = self.findShortestPath(maze, entrance, exit)

                # Check for overlap in paths
                path_set = set(path)
                if visited_cells & path_set:
                    valid_paths = False
                    break

                # Store path and add to total cost
                current_paths[(entrance, exit)] = path
                visited_cells.update(path_set)
                total_cost += path_cost

            # If paths are valid and have a lower cost, update best_paths
            if valid_paths and total_cost < min_total_cost:
                min_total_cost = total_cost
                best_paths = current_paths

            # Update solver state
        self.all_solved = bool(best_paths)
        self.entrance_exit_paths = best_paths  # Store the best paths in the expected attribute
        return best_paths

    def findShortestPath(self, maze: Maze, entrance: Coordinates, exit: Coordinates) -> Tuple[List[Coordinates], int]:
        # Dijkstra-style approach for finding shortest path between entrance and exit
        import heapq
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
