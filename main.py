import pygame
import colors
from queue import Queue, PriorityQueue
from grid import Grid


WIDTH = 1200
HEIGHT = 600
NODE_SIZE = 25
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Visualizer")


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

            if node.distance + 1 < neighbor.distance:

                neighbor.change_color(colors.PROCESSING_NODE_COLOR)
                neighbor.distance = node.distance + 1
                path[neighbor] = node
                pq.put((neighbor.distance, neighbor))

        grid.display_grid()
        pygame.display.update()

    if not found:
        return []

    return restore_path(path, grid.end)


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

            if node.distance + 1 + h < neighbor.distance:

                neighbor.change_color(colors.PROCESSING_NODE_COLOR)
                neighbor.distance = node.distance + 1 + h
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


def restore_path(came_from, end):
    """
    :param came_from: dict which stores information about previous node for all visited nodes
    :param end: target node
    :return path: list of nodes which represt the path from start to end node
    """
    path = [end]
    current = came_from[end]
    while current:
        path.append(current)
        current = came_from[current]

    return path[::-1]


def draw_path(path, grid):
    for node in path:
        node.color = colors.PATH_COLOR
        grid.display_grid()
        pygame.time.delay(35)
        pygame.display.update()


def get_clicked_node_position(grid):
    x, y = pygame.mouse.get_pos()
    return x // grid.node_size, y // grid.node_size


def handle_mouse_events(grid_instance):

    # Handle left mouse button click
    if pygame.mouse.get_pressed()[0]:
        col, row = get_clicked_node_position(grid_instance)
        node = grid_instance.grid[row][col]
        node.change_color(colors.WALL_COLOR)

    # Handle right mouse button click
    if pygame.mouse.get_pressed()[2]:
        col, row = get_clicked_node_position(grid_instance)
        node = grid_instance.grid[row][col]
        node.change_color(colors.DEFAULT_COLOR)


def main():
    pygame.init()

    grid_instance = Grid(WIDTH, HEIGHT, NODE_SIZE, WINDOW)


    # Mainloop of the program
    run = True
    while run:

        WINDOW.fill(colors.WHITE)
        grid_instance.display_grid()

        handle_mouse_events(grid_instance)

        # Handle keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                # Clear the screen
                if event.key == pygame.K_c:
                    grid_instance.setup()

                # Refresh the grid
                if event.key == pygame.K_r:
                    grid_instance.refresh_grid()

                # BFS visialization
                if event.key == pygame.K_1:
                    path = bfs(grid_instance)
                    draw_path(path, grid_instance)

                # DFS visualization
                if event.key == pygame.K_2:
                    path = dfs(grid_instance)
                    draw_path(path, grid_instance)

                # Dijkstra visualization
                if event.key == pygame.K_3:
                    path = dijkstra(grid_instance)
                    draw_path(path, grid_instance)

                # A* visualization
                if event.key == pygame.K_4:
                    path = a_star(grid_instance)
                    draw_path(path, grid_instance)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()