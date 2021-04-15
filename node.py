import pygame
import colors


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
        :param grid: instance of the class grid
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