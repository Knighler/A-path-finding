import math
import queue
from math import trunc
import time

import pygame



def heuristic(node, goal):
    """
    Calculate the heuristic value from the current node to the goal.
    This can be Manhattan distance, Euclidean distance, or other based on the graph type.
    
    Parameters:
    node (tuple or object): Current node position.
    goal (tuple or object): Goal node position.
    
    Returns:
    float: The heuristic value.
    """
    x1,y1=node
    x2,y2=goal
    eu=math.sqrt((x2-x1)**2+(y2-y1)**2)
    return eu


def a_star(graph, start, goal):

    """
    Implement the A* algorithm to find the shortest path from start to goal.

    Parameters:
    graph (Graph): The graph or grid on which A* will be performed.
    start (tuple or object): The starting node.
    goal (tuple or object): The goal node.

    Returns:
    list: The shortest path from start to goal.
    float: The total cost of the path.
    """

    #priority queues
    next_moves = queue.PriorityQueue()
    solution=queue.PriorityQueue()

    #maze starter
    next_moves.put((1,start,0))
    solution.put((1,start))
    prority,next_move,gcost=next_moves.get()

    #costs
    hcost=0
    total_cost=0

    #visited list
    visited=[(start)]

    #backtrack dictionary
    came_from={}

    while next_move!=goal:
        for value in graph[next_move]:
            if (value[0],value[1]) not in visited :
                hcost=heuristic((value[0],value[1]),goal)
                current_gcost=value[2]+gcost
                total_cost=current_gcost+hcost

                next_moves.put((total_cost,(value[0],value[1]),current_gcost))
                solution.put((total_cost,(value[0],value[1])))
                visited.append((value[0],value[1]))
                came_from[(value[0],value[1])]=next_move


        priority,next_move,gcost=next_moves.get()



    return solution,reconstruct_path(came_from,goal),priority


def reconstruct_path(came_from, current):
    """
    Reconstruct the path from the start to the goal by backtracking from the goal node.
    
    Parameters:
    came_from (dict): Dictionary mapping nodes to their predecessors.
    current (tuple or object): The current node to backtrack from.
    
    Returns:
    list: The reconstructed path.
    """
    path=[current]
    while current in came_from:
        path.append(came_from[current])
        current=came_from[current]
    return path

# Example Test Cases

def  test_a_star():
    start = (0, 0)
    goal = (49, 49)
    maze = create_maze(50, 50)
    graph = create_graph(maze)
    solution, path,total_cost = a_star(graph, start, goal)
    path.reverse()
    print(path)
    print("Total Cost: ",total_cost)
    visualize_path(maze, path,total_cost)


def visualize_path(maze,path,total_cost):
    pygame.init()
    width=600
    height=600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("A*")

    obstacles_white = (255, 255, 255)
    background_black = (0, 0, 0)
    line_green= (0, 255, 0)
    line_red=(255,0,0)
    screen.fill(background_black)
    cell=width/50
    pixel_path=[]




    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if  maze[row][col]=='#':
                pygame.draw.rect(screen, obstacles_white, pygame.Rect(col * cell, row * cell, cell, cell))

    for coords in range(len(path)):
            pixel_path.append((path[coords][0]*cell+cell//2,path[coords][1]*cell+cell//2))


    for coords in range(1,len(pixel_path)):

        pygame.draw.line(screen, line_green, pixel_path[coords-1],pixel_path[coords], 7)
        pygame.display.flip()
        time.sleep(0.05)





    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.set_caption(f"A*                                                   Total Cost:: {total_cost}")
        pygame.display.flip()
    pass


import random

def create_maze(width, height, obstacle_percentage=0.2, weighted_percentage=0.1, seed=42):
    """
    Create a 50x50 maze with random obstacles and weighted paths, but the same maze will
    be generated each time because of a fixed random seed.
    
    Parameters:
    width (int): Width of the maze.
    height (int): Height of the maze.
    obstacle_percentage (float): Percentage of cells that are obstacles.
    weighted_percentage (float): Percentage of cells that have a higher traversal cost.
    seed (int): Random seed to ensure the maze is the same each time.
    
    Returns:
    list: A 2D grid representing the maze. 
          '1' represents normal paths, 
          '#' represents obstacles, 
          values 2-5 represent weighted paths.
    """
    # Set the random seed to ensure consistent maze generation
    random.seed(seed)
    
    maze = []
    
    for i in range(height):
        row = []
        for j in range(width):
            # Randomly decide if the cell is an obstacle
            if random.random() < obstacle_percentage:
                row.append('#')  # Obstacle
            else:
                # Randomly assign weighted paths
                if random.random() < weighted_percentage:
                    row.append(random.randint(2, 5))  # Weighted path
                else:
                    row.append(1)  # Normal path with cost 1
        maze.append(row)
    
    return maze


def print_maze(maze):
    """
    Prints the maze in a human-readable format.
    
    Parameters:
    maze (list): A 2D grid representing the maze.
    """
    for row in maze:
        print(' '.join(str(cell) for cell in row))


def get_neighbors(x, y, maze):
    """
    Get valid neighbors of a cell (x, y) in the maze.
    
    Parameters:
    x (int): X-coordinate of the cell.
    y (int): Y-coordinate of the cell.
    maze (list): The maze represented as a 2D grid.
    
    Returns:
    list: List of valid neighbors as (neighbor_x, neighbor_y, cost) tuples.
    """
    neighbors = []
    height = len(maze)
    width = len(maze[0])
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] != '#':
            neighbors.append((nx, ny, maze[ny][nx]))
    
    return neighbors


def create_graph(maze):
    """
    Create a graph from the maze where each cell is a key, and its neighbors (with weights) are the values.
    
    Parameters:
    maze (list): The maze represented as a 2D grid.
    
    Returns:
    dict: A dictionary representing the graph, where each key is a (x, y) tuple and the value is
          a list of neighbors with their respective costs [(neighbor_x, neighbor_y, cost), ...].
    """
    graph = {}
    
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] != '#':  # If the cell is not an obstacle
                graph[(x, y)] = get_neighbors(x, y, maze)
    
    return graph


def print_graph(graph):
    """
    Print the graph structure where each cell has a list of its neighbors with their weights.
    
    Parameters:
    graph (dict): The graph structure.
    """
    for node, neighbors in graph.items():
        print(f"Cell {node}: {neighbors}")



# Example: Create a 50x50 maze and build the graph
test_a_star()

