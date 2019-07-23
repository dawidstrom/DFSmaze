#!/usr/bin/env python3

import random as rand
import pdb
import time


# Maze tiles.
empty_tile = '*'
wall_tile = '█'


class Pos:
    def __init__(self, pos: (int,int)):
        self.x = pos[0]
        self.y = pos[1]
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Pos(self.x+other.x, self.y+other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        return str( (self.x, self.y) )

class Maze:
    """
    Class for string based maze.
    """
    def __init__(self, size):
        self.maze = []
        for row in range(size[1]):
            row_str = []
            for col in range(size[0]):
                row_str.append(wall_tile)
            self.maze.append(row_str)
    
    def get(self, pos: Pos) -> str:
        return self.maze[pos.y][pos.x]

    def set(self, pos: Pos, value: str):
        self.maze[pos.y][pos.x] = value

    def valid_directions(self, position: Pos, visited: [Pos], goal: Pos) -> [Pos]:
        # Only allow one entrance to goal.
        if position == goal:
            return []

        up = position + Pos(0,-2)
        down = position + Pos(0,2)
        left = position + Pos(-2,0)
        right = position + Pos(2,0)

        directions = [up, down, left, right]
        valid_dirs = []

        for direction in directions:
            # Check if inside maze.
            if direction.x >= 0 and direction.x < len(self.maze[0]) and \
                    direction.y >= 0 and direction.y < len(self.maze):
                # Check if not visited.
                if direction not in visited:
                    valid_dirs.append(direction)

        return valid_dirs

    def clear_path(self, start: Pos, stop: Pos, goal: Pos):
        if stop != goal: # Don't update tile at goal.
            self.set(stop, empty_tile)
        midway = Pos( (start.x+stop.x)//2, (start.y+stop.y)//2 )
        self.set(midway, empty_tile) # Break wall.

    def generate_dfs(self, start: Pos, goal: Pos):
        """
        Generates maze using dfs, connecting the start and goal positions.
        Requires the start and goal positions to have an even positional value
        for x and y and that they are within the bounds of the maze.
        
        start: Start of maze.
        goal: Goal of maze. Will have only one path.
        """
        self.set(start, 'S')
        self.set(goal, 'G')


        # Add all unexplored positions into pool of unvisited positions.
        unvisited = []
        for y in range(len(self.maze)):
            for x in range(len(self.maze[0])):
                pos = Pos(x,y)
                if x%2 == 0 and y%2 == 0 and pos != start and pos != goal:
                    unvisited.append(pos)

        # Start DFS from start position.
        position = start
        visited = []
        searchable = []

        #TODO: Remove duplicates/paths which have the same destination position
        #in searchable.

        # Continue until all positions have been connected.
        while unvisited: # While not empty.
            visited.append(position)
            directions = self.valid_directions(position, visited, goal)

            # If there exists a path that can be connected.
            if len(directions) > 0:
                new_position = rand.choice(directions)

                # Queue unexplored directions.
                directions.remove(new_position)
                searchable.extend([(position,x) for x in directions])

                # Update maze/connect path.
                self.clear_path(position, new_position, goal)
                position = new_position # Update current position.

                # Mark position as visited, skip goal position.
                if position != goal: # Goal is not in unvisited.
                    unvisited.remove(position)
            else: # Path stuck.
                # Explore unvisited path.
                if searchable:
                    position = searchable.pop()[0]


    def print(self):
        for y in self.maze:
            for x in y:
                print(x, end="")
            print()


if __name__ == '__main__':
    maze = Maze((39,29))
    maze.generate_dfs(Pos(0,0), Pos(38,28))
    maze.print()
