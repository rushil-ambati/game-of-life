import pygame

BLACK = (0, 0, 0)
GRAY = (32, 32, 32)
WHITE = (255, 255, 255)


def show_grid(grid):
    for x in range(SIZE):
        for y in range(SIZE):
            colour = WHITE if grid[x][y] else GRAY

            rect = pygame.Rect(x*SQUARE_SIZE, y*SQUARE_SIZE,
                               SQUARE_SIZE//1.02, SQUARE_SIZE//1.02)
            pygame.draw.rect(SCREEN, colour, rect)


def square_clicked(pos):
    x = round(pos[0], 1)//SQUARE_SIZE
    y = round(pos[1], 1)//SQUARE_SIZE
    grid[x][y] = not grid[x][y]


def find_no_of_live_neighbours(x, y):
    n = 0
    for i in range(max(x-1, 0), min(x+1, SIZE-1)+1):
        for j in range(max(y-1, 0), min(y+1, SIZE-1)+1):
            if grid[i][j] and (i, j) != (x, y):
                n += 1
    return n


def update_grid():
    lns = [[0 for x in range(SIZE)] for y in range(SIZE)]
    for x in range(SIZE):
        for y in range(SIZE):
            lns[x][y] = find_no_of_live_neighbours(x, y)

    for x in range(SIZE):
        for y in range(SIZE):
            if grid[x][y]:
                if lns[x][y] < 2 or lns[x][y] > 3:
                    grid[x][y] = False
            else:
                if lns[x][y] == 3:
                    grid[x][y] = True


def configure():
    config = False
    inp_valid = False
    while not inp_valid:
        config_inp = input(
            "Would you like to configure the grid/window sizes (y/n)? ")
        if config_inp.lower() == 'y':
            inp_valid = True
            config = True
        elif config_inp.lower() == 'n':
            inp_valid = True
        else:
            print("Invalid input - please select y/n.")

    if config:
        inp_valid = False
        while not inp_valid:
            size_inp = int(input("Grid size: "))
            win_size_inp = int(input("Window size: "))
            if size_inp > 0 and win_size_inp > 0:
                inp_valid = True
                return size_inp, win_size_inp
            else:
                print("Invalid input - please select integer values greater than zero.")
    else:
        return 15, 600


if __name__ == "__main__":
    print("""
    === Conway's Game of Life ===
    Controls:
        p: Play/Pause (program begins in paused state)
        Left click: Create live cell (while paused)
        Space: Step through incrementally (while paused)
        Up/Down arrows: Increase/Decrease FPS (while playing)
    """)

    global SIZE, WINDOW_SIZE
    SIZE, WINDOW_SIZE = configure()

    global SQUARE_SIZE
    SQUARE_SIZE = WINDOW_SIZE // SIZE

    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    CLOCK = pygame.time.Clock()

    SCREEN.fill(BLACK)

    grid = [[False for x in range(SIZE)] for y in range(SIZE)]

    play = False
    fps = 30
    while True:
        show_grid(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not play:
                square_clicked(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    play = not play
                    if play:
                        fps = 3
                        print("Playing")
                    else:
                        print("Paused")
                if not play and event.key == pygame.K_SPACE:
                    update_grid()
                if play and event.key == pygame.K_UP:
                    fps += 1
                if play and event.key == pygame.K_DOWN:
                    fps -= min(fps, 1)

        pygame.display.update()
        CLOCK.tick(fps if play else 30)
        if play:
            update_grid()
