import pygame
import colors


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


def _draw_path(path, grid):
    for node in path:
        node.color = colors.PATH_COLOR
        grid.display_grid()
        pygame.time.delay(35)
        pygame.display.update()


def get_clicked_node_position(grid):
    x, y = pygame.mouse.get_pos()
    return x // grid.node_size, y // grid.node_size


def draw_path(find_path):
    def inner(grid):
        if grid.found_path:
            return

        path = find_path(grid)
        grid.found_path = True
        _draw_path(path, grid)

    return inner
