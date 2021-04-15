import random
import colors
from node import Node


class Grid:

    def __init__(self, width, height, node_size, window):
        """
        :param width: width of the screen
        :param height: height of the screen
        :param node_size: cell size on the screen
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
        self.setup()


    def setup(self):
        """
        Prepares grid for work
        """

        # Create grid
        self._grid = self._generate_grid()

        # Updates nodes neighbors
        self.get_nodes_neighbors()

        # Set start and end node
        self._set_start_and_end_node()


    def _set_start_and_end_node(self):
        """
        Set start and end node in random places
        """

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
        """ Reset all nodes to initial state """

        for x in range(self.rows):
            for y in range(self.cols):
                node = self._grid[x][y]
                if node.color != colors.WALL_COLOR:
                    node.distance = float("inf")
                    node.change_color(colors.DEFAULT_COLOR)

        self.start.change_color(colors.START_NODE_COLOR)
        self.end.change_color(colors.END_NODE_COLOR)