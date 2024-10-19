# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Dijkstra's maze solver.
#
# __author__ =  <Wanjun Shi>
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from maze.util import Coordinates
from maze.maze import Maze
import heapq


class DijkstraSolver():
    def __init__(self):
        # TODO: Implement this for task A!
        self.m_solverPath = None  # To store the found path


    def solveMaze(self, maze: Maze, entrance: Coordinates):
        # TODO: Implement this for task A!
        # Obtain the list of all exits
        exits = maze.getExits()
        shortest_path = None
        shortest_distance = float('inf')

        # Iterate over all exits to find the closest one
        for exit in exits:
            path, distance = self.findShortestPath(maze, entrance, exit)
            # Update the shortest path if a closer exit is found
            if distance < shortest_distance:
                shortest_path = path
                shortest_distance = distance

        # Store the shortest path found
        self.m_solverPath = shortest_path

    def findShortestPath(self, maze: Maze, entrance: Coordinates, exit: Coordinates):
        # Dijkstra’s algorithm initialization
        distances = {coord: float('inf') for coord in maze.getCoords()}
        distances[entrance] = 0
        priority_queue = [(0, id(entrance), entrance)]  # Include id() as a unique tie-breaker
        predecessors = {entrance: None}
        visited = set()  # Track nodes whose shortest paths are confirmed

        while priority_queue:
            # Extract the node with the smallest distance
            current_distance, _, current_cell = heapq.heappop(priority_queue)

            # If we reach the exit, stop early
            if current_cell == exit:
                break

            # Skip processing if the node has already been visited
            if current_cell in visited:
                continue
            visited.add(current_cell)

            # Explore neighbors
            for neighbor in maze.neighbours(current_cell):
                # Check for walls between the current cell and the neighbor
                if maze.hasWall(current_cell, neighbor):
                    continue  # Skip this neighbor if there is a wall

                # Calculate the distance to the neighbor
                weight = maze.edgeWeight(current_cell, neighbor)
                new_distance = current_distance + weight

                # Update the distance if a shorter path is found
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_cell
                    heapq.heappush(priority_queue,
                                   (new_distance, id(neighbor), neighbor))  # Use id() to avoid comparison issues

        # Backtrack from exit to entrance to retrieve the path
        path = []
        step = exit
        while step is not None:
            path.append(step)
            step = predecessors.get(step)
        path.reverse()

        return path, distances[exit]
