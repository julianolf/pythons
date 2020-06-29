import itertools
import random

import pygame

# Set immutable values
TITLE = "PYTHONS"
BLOCK_W, BLOCK_H = 30, 30
BLOCK_SIZE = BLOCK_W, BLOCK_H
WIN_W, WIN_H = BLOCK_W * 24, BLOCK_H * 20 + BLOCK_H
WIN_SIZE = WIN_W, WIN_H
MAP = tuple(
    itertools.product(range(0, WIN_W, BLOCK_W), range(BLOCK_H, WIN_H, BLOCK_H))
)
FONT_NAME = "Courier"
FONT_SIZE = 45
FONT_SIZE_SMALL = 20


class Game:
    """Pythons.

    Yet another Snake game.
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
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        self.font_small = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)

        self.clock = pygame.time.Clock()
        self.fps = 5
        self.running = False
        self.xv, self.yv, self.ac = 1, 0, BLOCK_W
        center = WIN_W // 2, (WIN_H - BLOCK_H) // 2
        self.snake = [center, (center[0] - BLOCK_W, center[1])]
        self.apple = 60, 60
        self.score = 0
        self.score_pos = WIN_W / 2, 2

        self.white_bar = pygame.Surface((WIN_W, BLOCK_H))
        self.white_bar.fill((255, 255, 255))
        self.white_bar = self.white_bar.convert()
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
            self.score += 10
            self.apple = None
            while not self.apple:
                xy = random.choice(MAP)
                self.apple = xy if xy not in self.snake else None
        else:
            self.snake.pop()

        if (
            head[0] < 0
            or head[0] >= WIN_W
            or head[1] < BLOCK_H
            or head[1] >= WIN_H
        ):
            self.running = False

        if head in self.snake[1:]:
            self.running = False

        if self.fps % 100 == 0:
            self.fps += 5

    def draw(self):
        """Draws everything on screen."""
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.red_block, self.apple)
        [self.screen.blit(self.green_block, xy) for xy in self.snake]
        self.screen.blit(self.white_bar, (0, 0))
        score = self.font.render(str(self.score), True, (0, 0, 0))
        score_rect = score.get_rect()
        score_rect.midtop = self.score_pos
        self.screen.blit(score, score_rect)
        pygame.display.flip()

    def draw_text(self, font, text, position, color, center=False):
        """Draws text on screen."""
        obj = font.render(text, True, color)
        obj_rect = obj.get_rect()
        x, y = position
        if center:
            x -= obj_rect.width // 2
            y -= obj_rect.height // 2
        obj_rect.topleft = x, y
        self.screen.blit(obj, obj_rect)

    def loop(self):
        """Game main loop.

        Keeps repeating the same sequence of steps
        until the player dies or quit the game.
        """
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.update()
            self.draw()

    def splash(self):
        """Show splash screen."""
        self.screen.fill((0, 0, 0))

        block = pygame.Surface(BLOCK_SIZE)
        block.fill((0, 0, 255))
        blue_block = block.convert()
        block.fill((255, 255, 0))
        yellow_block = block.convert()
        w10, w11, w12, w13 = [BLOCK_W * w for w in range(10, 14)]
        h2, h3, h4, h5, h6, h7 = [BLOCK_H * h for h in range(2, 8)]
        h1_2 = BLOCK_H // 1.2
        blues = [
            (w11, h2 + h1_2),
            (w12, h2 + h1_2),
            (w12, h3),
            (w10, h4),
            (w11, h4),
            (w12, h4),
            (w10, h5),
        ]
        yellows = [
            (w13, h4),
            (w11, h5),
            (w12, h5),
            (w13, h5),
            (w11, h6),
            (w11, h7 - h1_2),
            (w12, h7 - h1_2),
        ]
        [self.screen.blit(blue_block, xy) for xy in blues]
        [self.screen.blit(yellow_block, xy) for xy in yellows]

        title_pos = (WIN_W // 2, WIN_H // 2)
        title_color = (255, 255, 255)
        self.draw_text(self.font, TITLE, title_pos, title_color, center=True)

        ctrl_str = "Use the [arrow] keys to move"
        ctrl_pos = title_pos[0], title_pos[1] + BLOCK_H
        ctrl_color = (255, 255, 255)
        self.draw_text(
            self.font_small, ctrl_str, ctrl_pos, ctrl_color, center=True
        )

        start_str = "Press any key to start"
        start_pos = title_pos[0], WIN_H - BLOCK_H
        ctrl_color = (255, 255, 255)
        self.draw_text(
            self.font_small, start_str, start_pos, ctrl_color, center=True
        )

        pygame.display.flip()

        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    return

    def run(self):
        """Starts the game."""
        self.running = True
        self.splash()
        self.loop()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
