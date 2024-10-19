# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Kruskal's maze generator.
#
# __author__ = <Your name>
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze import Maze
from maze.util import Coordinates




class KruskalMazeGenerator():
    """
    Kruskal's algorithm maze generator.  
    TODO: Complete the implementation (Task A)
    """


    def generateMaze(self, maze:Maze):
        # TODO: Implement this method for task A.
        # TODO: Implement this method for task A.
        """
        Generate a maze using Kruskal's algorithm, which orders walls by weight and selectively removes them to ensure connectivity.
        """
        walls = []  # List to store (weight, cell1, cell2)
        # Retrieve all edges with weights and sort them
        for cell in maze.getCoords():
            for neighbor in maze.neighbours(cell):
                weight = maze.edgeWeight(cell, neighbor)
                walls.append((weight, cell, neighbor))

        # Sort walls by weight
        walls.sort(key=lambda x: x[0])

        # Initialize union-find structure
        parent = {}
        rank = {}

        def find(coord):
            if parent[coord] != coord:
                parent[coord] = find(parent[coord])
            return parent[coord]

        def union(coord1, coord2):
            root1 = find(coord1)
            root2 = find(coord2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                else:
                    parent[root1] = root2
                    if rank[root1] == rank[root2]:
                        rank[root2] += 1

        # Initialize the union-find sets for all cells
        for cell in maze.getCoords():
            parent[cell] = cell
            rank[cell] = 0

        # Process walls
        for weight, cell1, cell2 in walls:
            # Check if both cells are within the maze boundaries
            if not (cell1.getRow() in [-1, maze.rowNum()] or cell2.getRow() in [-1, maze.rowNum()] or
                    cell1.getCol() in [-1, maze.colNum()] or cell2.getCol() in [-1, maze.colNum()]):
                # Only remove the wall if it connects two different components
                if find(cell1) != find(cell2):
                    union(cell1, cell2)
                    maze.removeWall(cell1, cell2)