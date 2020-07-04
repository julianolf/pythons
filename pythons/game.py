import itertools
import os
import random

import pygame

# Set immutable values
TITLE = "PYTHONS"
BLOCK_W, BLOCK_H = 30, 30
BLOCK_SIZE = BLOCK_W, BLOCK_H
WIN_W, WIN_H = BLOCK_W * 24, BLOCK_H * 20 + BLOCK_H
WIN_SIZE = WIN_W, WIN_H
CENTER_W, CENTER_H = WIN_W // 2, WIN_H // 2
WIN_CENTER = CENTER_W, CENTER_H
MAP = tuple(
    itertools.product(range(0, WIN_W, BLOCK_W), range(BLOCK_H, WIN_H, BLOCK_H))
)
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
FONT_PATH = os.path.join(ASSETS_PATH, "font")
FONT = os.path.join(FONT_PATH, "museo_moderno.ttf")
FONT_M = os.path.join(FONT_PATH, "museo_moderno_medium.ttf")


class Color:
    """Color palette."""

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


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

        self.clock = pygame.time.Clock()
        self.score_pos = CENTER_W, BLOCK_H // 2

        self.white_bar = pygame.Surface((WIN_W, BLOCK_H))
        self.white_bar.fill((255, 255, 255))
        self.white_bar = self.white_bar.convert()
        self.block = pygame.Surface(BLOCK_SIZE)
        self.block.fill(Color.RED)
        self.red_block = self.block.convert()
        self.block.fill(Color.GREEN)
        self.green_block = self.block.convert()

    def reset(self):
        """(Re)Set controlling variables."""
        self.fps = 5
        self.running = True
        self.alive = True
        self.xv, self.yv, self.ac = 1, 0, BLOCK_W
        center = CENTER_W, (WIN_H - BLOCK_H) // 2
        self.snake = [center, (center[0] - BLOCK_W, center[1])]
        self.apple = 60, 60
        self.score = 0

    def events(self):
        """Handles player input events.

        Check if the player has hit a key, if it did it,
        check if the key is mapped to an action.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    return
                elif event.key == pygame.K_LEFT:
                    if (self.xv, self.yv) != (1, 0):
                        self.xv, self.yv = -1, 0
                        return
                elif event.key == pygame.K_RIGHT:
                    if (self.xv, self.yv) != (-1, 0):
                        self.xv, self.yv = 1, 0
                        return
                elif event.key == pygame.K_UP:
                    if (self.xv, self.yv) != (0, 1):
                        self.xv, self.yv = 0, -1
                        return
                elif event.key == pygame.K_DOWN:
                    if (self.xv, self.yv) != (0, -1):
                        self.xv, self.yv = 0, 1
                        return

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
            self.alive = False

        if head in self.snake[1:]:
            self.alive = False

        if self.fps % 100 == 0:
            self.fps += 5

    def draw(self):
        """Draws everything on screen."""
        self.screen.fill(Color.BLACK)
        self.screen.blit(self.red_block, self.apple)
        [self.screen.blit(self.green_block, xy) for xy in self.snake]
        self.screen.blit(self.white_bar, (0, 0))
        self.draw_text(str(self.score), self.score_pos, size=32)
        pygame.display.flip()

    def draw_text(
        self,
        text,
        position,
        font=FONT,
        size=16,
        color=Color.BLACK,
        centered=True,
    ):
        """Draws text on screen."""
        _font = pygame.font.Font(font, size)
        _text = _font.render(text, True, color)
        _rect = _text.get_rect()
        x, y = position
        if centered:
            x -= _rect.width // 2
            y -= _rect.height // 2
        _rect.topleft = x, y
        self.screen.blit(_text, _rect)

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
            self.game_over()

    def splash(self):
        """Show splash screen."""
        self.screen.fill(Color.BLACK)

        self.block.fill(Color.BLUE)
        blue_block = self.block.convert()
        self.block.fill(Color.YELLOW)
        yellow_block = self.block.convert()
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

        self.draw_text(
            TITLE, WIN_CENTER, font=FONT_M, size=48, color=Color.WHITE
        )

        ctrl = "Use the [arrow] keys to move"
        ctrl_pos = CENTER_W, CENTER_H + (BLOCK_H * 1.3)
        self.draw_text(ctrl, ctrl_pos, color=Color.WHITE)

        start = "Press any key to start"
        start_pos = CENTER_W, WIN_H - BLOCK_H
        self.draw_text(start, start_pos, color=Color.WHITE)

        pygame.display.flip()
        self.wait_keydown()

    def game_over(self):
        """Show game over screen."""
        if self.alive:
            return

        self.screen.fill(Color.BLACK)
        self.draw_text(
            "GAME OVER", WIN_CENTER, font=FONT_M, size=48, color=Color.WHITE
        )
        again = "Press any key to play again"
        again_pos = CENTER_W, WIN_H - BLOCK_H
        self.draw_text(again, again_pos, color=Color.WHITE)

        pygame.display.flip()
        self.wait_keydown()

        if self.running:
            self.reset()

    def wait_keydown(self):
        """Wait until a key is pressed or the windown is closed."""
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    return

    def run(self):
        """Starts the game."""
        self.reset()
        self.splash()
        self.loop()
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
