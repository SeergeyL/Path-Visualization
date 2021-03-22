import random
import pygame
import colors
from queue import Queue, PriorityQueue


WIDTH = 1200
HEIGHT = 600
NODE_SIZE = 25
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Visualizer")


class Node:

    def __init__(self, x, y, node_size):
        """
        :param x: column of the node in a Grid
        :param y: row of the node in a Grid
        :param node_size: cell size, which should be displayed on the screen
        """
        self.x = x
        self.y = y
        self.size = node_size
        self.color = colors.DEFAULT_COLOR
        self.distance = float("inf")
        self._neighbors = None


    @property
    def neighbors(self):
        return self._neighbors


    def _display_visited_node(self, surface):
        """ Display node with custom border """

        pygame.draw.rect(surface, self.color,
                         (self.x * self.size, self.y * self.size, self.size, self.size))

        pygame.draw.rect(surface, colors.NODE_BORDER_COLOR,
                         (self.x * self.size, self.y * self.size, self.size, self.size), 1)


    def display_node(self, surface):

        if self.color == colors.PROCESSED_NODE_COLOR:
            self._display_visited_node(surface)
            return

        span = 0
        if self.color == colors.DEFAULT_COLOR:
            span = 1

        pygame.draw.rect(surface, self.color,
                         (self.x * self.size, self.y * self.size, self.size, self.size), span)


    def change_color(self, color):
        """ Change node's color if it is not start or end node """

        if self.color not in (colors.START_NODE_COLOR, colors.END_NODE_COLOR):
            self.color = color


    def get_neighbors(self, grid):
        """
        Updates node's neighbors
        :param grid: initialized instance of the class grid
        """
        rows = grid.rows
        cols = grid.cols
        ways = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        neighbors = []
        for dx, dy in ways:
            if 0 <= self.x + dx < cols and 0 <= self.y + dy < rows:
                neighbors.append(grid.grid[self.y + dy][self.x + dx])

        self._neighbors = neighbors


    def __lt__(self, other):
        return False


class Grid:

    def __init__(self, width, height, node_size, window):
        """
        :param width: width of the screen
        :param height: height of the screen
        :param node_size: cell size with which it will be displayed on the screen
        :param window: main window of the program on which the grid will be displayed
        """
        self.width = width
        self.height = height
        self.node_size = node_size
        self.cols = width // node_size
        self.rows = height // node_size
        self.window = window
        self._grid = None
        self.start = None
        self.end = None


    def init(self):
        """
        Prepares the grid for work, set start and end node in random places,
        updates all Node's neighbors in a grid
        """

        # Grid init
        self._grid = self._generate_grid()
        self.get_nodes_neighbors()

        # Setting start and end node
        x_start = random.randint(0, self.rows - 1)
        y_start = random.randint(0, self.cols - 1)

        x_end = random.randint(0, self.rows - 1)
        y_end = random.randint(0, self.cols - 1)

        self.start = self._grid[x_start][y_start]
        self.end = self._grid[x_end][y_end]

        self.start.change_color(colors.START_NODE_COLOR)
        self.end.change_color(colors.END_NODE_COLOR)


    @property
    def grid(self):
        if not self._grid:
            self._grid = self._generate_grid()
        return self._grid


    def _generate_grid(self):
        """
        Generate grid with specified constructor parameters
        :return: list[list[Node]]
        """
        grid = []
        rows = self.rows
        cols = self.cols
        for y in range(rows):
            row = []
            for x in range(cols):
                node = Node(x, y, self.node_size)
                row.append(node)

            grid.append(row)

        return grid


    def display_grid(self):
        """ Display grid on the screen which is specified in a constructor """

        if not self._grid:
            self._grid = self._generate_grid()


        for x in range(self.rows):
            for y in range(self.cols):
                node = self._grid[x][y]
                node.display_node(self.window)


    def get_nodes_neighbors(self):
        """ Updates node's neighbors """

        for row in self._grid:
            for node in row:
                node.get_neighbors(self)


    def refresh_grid(self):
        """ Reset all nodes initial state """

        for x in range(self.rows):
            for y in range(self.cols):
                node = self._grid[x][y]
                if node.color != colors.WALL_COLOR:
                    node.distance = float("inf")
                    node.change_color(colors.DEFAULT_COLOR)

        self.start.change_color(colors.START_NODE_COLOR)
        self.end.change_color(colors.END_NODE_COLOR)


def bfs(grid):
    """
    Gets the initialised instance of the Grid class and find the path
    from grid.start to grid.end node, showing the process of BFS on a screen.

    :param grid: initialized instance of class Grid.
    grid = Grid(width, height, node_size)
    grid.init()

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
    Gets the initialised instance of the Grid class and find the path
    from grid.start to grid.end node, showing the process of DFS on a screen.

    :param grid: initialized instance of class Grid.
    grid = Grid(width, height, node_size)
    grid.init()

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
    Gets the initialised instance of the Grid class and find the path
    from grid.start to grid.end node, showing the process of Dijkstra on a screen.

    :param grid: initialized instance of class Grid.
    grid = Grid(width, height, node_size)
    grid.init()

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
    Gets the initialised instance of the Grid class and find the path
    from grid.start to grid.end node, showing the process of A* on a screen.

    :param grid: initialized instance of class Grid.
    grid = Grid(width, height, node_size)
    grid.init()

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
    :return: path from start to end node in list
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
    grid_instance.init()


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
                    grid_instance.init()

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