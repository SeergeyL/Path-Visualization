import pygame
import colors
from queue import Queue, PriorityQueue
from utils import restore_path, draw_path


@draw_path
def bfs(grid):
    """
    Gets instance of the class Grid and find the path
    from grid.start to grid.end node, showing the process of BFS on a screen.

    :param grid: instance of class Grid.
    :return: the path from grid.start node to grid.end node
    """

    q = Queue()
    q.put(grid.start)
    visited = {grid.start: None}

    found = False
    while q:

        if found:
            break

        node = q.get()
        node.change_color(colors.PROCESSED_NODE_COLOR)

        for neighbor in node.neighbors:
            if neighbor.color == colors.WALL_COLOR:
                continue

            if neighbor == grid.end:
                found = True

            if neighbor not in visited:

                neighbor.change_color(colors.PROCESSING_NODE_COLOR)

                visited[neighbor] = node
                q.put(neighbor)

        grid.display_grid()
        pygame.display.update()

    if not found:
        return []

    return restore_path(visited, grid.end)


@draw_path
def dfs(grid):
    """
    Gets instance of the class Grid and find the path
    from grid.start to grid.end node, showing the process of DFS on a screen.

    :param grid: instance of class Grid.
    :return: the path from grid.start node to grid.end node
    """

    visited = {grid.start: None}
    stack = [grid.start]

    found = False
    while stack:

        if found:
            break

        node = stack.pop()
        node.change_color(colors.PROCESSED_NODE_COLOR)

        for neighbor in node.neighbors:
            if neighbor.color == colors.WALL_COLOR:
                continue

            if neighbor == grid.end:
                found = True

            if neighbor not in visited:

                neighbor.change_color(colors.PROCESSED_NODE_COLOR)

                visited[neighbor] = node
                stack.append(neighbor)

        grid.display_grid()
        pygame.display.update()

    if not found:
        return []

    return restore_path(visited, grid.end)


@draw_path
def dijkstra(grid):
    """
    Gets instance of the class Grid and find the path
    from grid.start to grid.end node, showing the process of Dijkstra on a screen.

    :param grid: instance of class Grid.
    :return: the path from grid.start node to grid.end node
    """

    pq = PriorityQueue()
    grid.start.distance = 0
    pq.put([grid.start.distance, grid.start])

    visited = set()
    path = {grid.start: None}

    found = False
    while not pq.empty():

        if found:
            break

        node = pq.get()[1]
        if node in visited: continue
        else: visited.add(node)

        node.change_color(colors.PROCESSED_NODE_COLOR)

        for neighbor in node.neighbors:
            if neighbor.color == colors.WALL_COLOR:
                continue

            if neighbor == grid.end:
                found = True

            cost = neighbor.weight
            if node.distance + cost < neighbor.distance:

                neighbor.change_color(colors.PROCESSING_NODE_COLOR)
                neighbor.distance = node.distance + cost
                path[neighbor] = node
                pq.put((neighbor.distance, neighbor))

        grid.display_grid()
        pygame.display.update()

    if not found:
        return []

    return restore_path(path, grid.end)


@draw_path
def a_star(grid):
    """
    Gets instance of the class Grid and find the path
    from grid.start to grid.end node, showing the process of A* on a screen.

    :param grid: instance of class Grid.
    :return: the path from grid.start node to grid.end node
    """

    pq = PriorityQueue()
    grid.start.distance = 0
    pq.put([grid.start.distance, grid.start])

    visited = set()
    path = {grid.start: None}

    found = False
    while not pq.empty():

        if found:
            break

        node = pq.get()[1]
        if node in visited:
            continue
        else:
            visited.add(node)

        node.change_color(colors.PROCESSED_NODE_COLOR)

        for neighbor in node.neighbors:
            if neighbor.color == colors.WALL_COLOR:
                continue

            if neighbor == grid.end:
                found = True

            h = heuristic(node, grid.end)

            cost = neighbor.weight
            if node.distance + cost + h < neighbor.distance:

                neighbor.change_color(colors.PROCESSING_NODE_COLOR)
                neighbor.distance = node.distance + cost + h
                path[neighbor] = node
                pq.put((neighbor.distance, neighbor))

        grid.display_grid()
        pygame.display.update()

    if not found:
        return []

    return restore_path(path, grid.end)


def heuristic(current, end):
    """ Calculates Manhattan distance between current and end nodes for A* algorithm """

    return abs(current.x - end.x) + abs(current.y - end.y)
