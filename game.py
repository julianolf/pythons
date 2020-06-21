import itertools
import random

import pygame

# Set immutable values
TITLE = 'Blockade'
WIN_W, WIN_H = 720, 600
WIN_SIZE = WIN_W, WIN_H
BLOCK_W, BLOCK_H = 30, 30
BLOCK_SIZE = BLOCK_W, BLOCK_H
FPS = 5
MAP = tuple(
    itertools.product(range(0, WIN_W, BLOCK_W), range(0, WIN_H, BLOCK_H))
)


class Game:
    """Blockade.

    Yet another Snake game.

    `Blockade` refers to the very first electronic game to introduce
    the basic mechanics used in almost all snake-like games.

    With that said, despite of the name this
    is not a port of the Blockade game.
    """

    def __init__(self):
        """Performs game initialization.

        - Initialize game engine
        - Configure window
        - Set initial controlling variables
        - Create drawable objects
        """
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode(WIN_SIZE)

        self.clock = pygame.time.Clock()
        self.running = False
        self.xv, self.yv, self.ac = 1, 0, BLOCK_W
        center = WIN_W // 2, WIN_H // 2
        self.snake = [center, (center[0] - BLOCK_W, center[1])]
        self.apple = 60, 60

        self.red_block = pygame.Surface(BLOCK_SIZE)
        self.red_block.fill((255, 0, 0))
        self.red_block = self.red_block.convert()
        self.green_block = pygame.Surface(BLOCK_SIZE)
        self.green_block.fill((0, 255, 0))
        self.green_block = self.green_block.convert()

    def events(self):
        """Handles player input events.

        Check if the player has hit a key, if it did it,
        check if the key is mapped to an action.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT:
                    if (self.xv, self.yv) != (1, 0):
                        self.xv, self.yv = -1, 0
                elif event.key == pygame.K_RIGHT:
                    if (self.xv, self.yv) != (-1, 0):
                        self.xv, self.yv = 1, 0
                elif event.key == pygame.K_UP:
                    if (self.xv, self.yv) != (0, 1):
                        self.xv, self.yv = 0, -1
                elif event.key == pygame.K_DOWN:
                    if (self.xv, self.yv) != (0, -1):
                        self.xv, self.yv = 0, 1

    def update(self):
        """Updates elements position and status.

        Here is where the game mechanics is built.
        - Update snake position
        - Check if the snake has eaten the apple
        - Put a new apple in a random position if it was ate
        - If the head of the snake leaves the screen the game is over
        - If the head of the snake hits its own body the game is over
        """
        head = (
            (self.snake[0][0] + self.xv * self.ac),
            (self.snake[0][1] + self.yv * self.ac),
        )
        self.snake.insert(0, head)

        if head == self.apple:
            self.apple = None
            while not self.apple:
                xy = random.choice(MAP)
                self.apple = xy if xy not in self.snake else None
        else:
            self.snake.pop()

        if head[0] < 0 or head[0] >= WIN_W or head[1] < 0 or head[1] >= WIN_H:
            self.running = False

        if head in self.snake[1:]:
            self.running = False

    def draw(self):
        """Draws everything on screen."""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.red_block, self.apple)
        [self.screen.blit(self.green_block, xy) for xy in self.snake]
        pygame.display.flip()

    def loop(self):
        """Game main loop.

        Keeps repeating the same sequence of steps
        until the player dies or quit the game.
        """
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def run(self):
        """Starts the game."""
        self.running = True
        self.loop()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
