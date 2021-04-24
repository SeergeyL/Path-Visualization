import pygame
import colors
from grid import Grid
from path_finding_algorithms import bfs, dfs, dijkstra, a_star
from utils import get_clicked_node_position, draw_path


WIDTH = 1200
HEIGHT = 600
NODE_SIZE = 25
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Visualizer")
FONT = 'Calibri'


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

    font = pygame.font.SysFont(FONT, NODE_SIZE // 2,  bold=True)
    grid_instance = Grid(WIDTH, HEIGHT, NODE_SIZE, WINDOW, font)

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

                # Assign nodes random weight
                if event.key == pygame.K_w:
                    grid_instance.assign_weights_to_nodes()

                # Toggle show weights
                if event.key == pygame.K_t:
                    grid_instance.toggle_show_weights()

                # BFS visualization
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