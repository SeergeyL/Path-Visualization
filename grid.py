import random
import colors
from node import Node


class Grid:

    def __init__(self, width, height, node_size, window, font):
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
        self.font = font
        self.window = window
        self._grid = None
        self.start = None
        self.end = None
        self.show_weights = False
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

        # Assign nodes default value
        self.assign_weights_to_nodes(True)

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

        if self.show_weights:
            self.display_node_weights()

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

    def assign_weights_to_nodes(self, flag=False):
        """
        Assign weights to nodes in a grid

        :flag: if flag value False then node would be assigned default weight
        otherwise random value from 1 to 20
        """

        for x in range(self.rows):
            for y in range(self.cols):
                node = self._grid[x][y]
                node.assign_weight(use_default=flag)

    def display_node_weights(self):
        """
        Display nodes' weights on the grid. Weight of the node is not displayed on
        start/end node and wall node
        """

        for x in range(self.rows):
            for y in range(self.cols):
                node = self._grid[x][y]

                if node.color in (colors.START_NODE_COLOR, colors.END_NODE_COLOR, colors.WALL_COLOR):
                    continue

                text_surface = self.font.render(str(node.weight), True, colors.DEFAULT_TEXT_COLOR)

                # Calculates absolute position of the node center
                x_center = (node.x * node.size + (node.x + 1) * node.size) // 2
                y_center = (node.y * node.size + (node.y + 1) * node.size) // 2

                text_centered = text_surface.get_rect(center=(x_center, y_center))
                self.window.blit(text_surface, text_centered)

    def toggle_show_weights(self):
        """
        Toggles show_weigths attribute.
        if show_weigths set to True, weigths of nodes will be displayed during render.
        """

        self.show_weights = not self.show_weights
