import itertools
import random

import pygame

TITLE = 'Pythons'
WIN_W, WIN_H = 720, 600
WIN_SIZE = WIN_W, WIN_H
BLOCK_W, BLOCK_H = 30, 30
BLOCK_SIZE = BLOCK_W, BLOCK_H
FPS = 5
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
MAP = tuple(
    itertools.product(range(0, WIN_W, BLOCK_W), range(0, WIN_H, BLOCK_H))
)


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode(WIN_SIZE)
    clock = pygame.time.Clock()

    red_block = pygame.Surface(BLOCK_SIZE)
    red_block.fill(RED)
    red_block = red_block.convert()

    green_block = pygame.Surface(BLOCK_SIZE)
    green_block.fill(GREEN)
    green_block = green_block.convert()

    xv, yv, ac = 1, 0, BLOCK_W
    center = WIN_W // 2, WIN_H // 2
    apple = 60, 60
    snake = [center, (center[0] - BLOCK_W, center[1])]
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    xv, yv = -1, 0
                elif event.key == pygame.K_RIGHT:
                    xv, yv = 1, 0
                elif event.key == pygame.K_UP:
                    xv, yv = 0, -1
                elif event.key == pygame.K_DOWN:
                    xv, yv = 0, 1

        head = (snake[0][0] + xv * ac), (snake[0][1] + yv * ac)
        snake.insert(0, head)

        if head == apple:
            apple = None
            while not apple:
                xy = random.choice(MAP)
                apple = xy if xy not in snake else None
        else:
            snake.pop()

        screen.fill(BLACK)
        screen.blit(red_block, apple)
        [screen.blit(green_block, xy) for xy in snake]
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
