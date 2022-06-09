import random
import time

import pygame
from game.snake import Snake


class Board:
    def __init__(self, width, height, speed=0.2, scale=10, human=True, render=True):
        self.render = render
        self.width = width * scale
        self.height = height * scale
        if render:
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.init()
            pygame.display.set_caption('Snake - DeepLearning')
            pygame.display.flip()
            self.font = pygame.font.Font(pygame.font.get_default_font(), 32)
        self.width_tiles = width
        self.height_tiles = height
        self.scale = scale
        self.snake = Snake(width // 2, height // 2)
        self.human = human
        self.speed = speed

        self.turn = 0  # 0: forward, 1: left, 2: right

        self.apple = (random.randint(0, self.width_tiles - 1), random.randint(0, self.height_tiles - 1))

        self.snake_head_color = pygame.Color(255, 255, 255)
        self.snake_body_color = pygame.Color(100, 100, 100)
        self.background_color = pygame.Color(0, 0, 0)
        self.apple_color = pygame.Color(255, 0, 0)

    def start(self):
        if self.human:
            self.last_keys = pygame.key.get_pressed()

        running = True
        last_time = time.time()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    running = False
            self.reset_screen()

            if self.human:
                self.human_input()
            current_time = time.time()
            if current_time - last_time > self.speed:
                last_time = current_time
                if self.turn == 1:
                    self.snake.turn_left()
                elif self.turn == 2:
                    self.snake.turn_right()
                self.turn = 0
                self.snake.forward()
            self.snake_logic()
            self.apple_logic()
            if self.render:
                self.draw_snake()
                self.draw_apple()
                self.draw_score()
                self.update_screen()

    def reset_screen(self):
        self.screen.fill(self.background_color)

    def update_screen(self):
        pygame.display.update()

    def apple_logic(self):
        if (self.snake.x, self.snake.y) == self.apple:
            self.apple = (random.randint(0, self.width_tiles - 1), random.randint(0, self.height_tiles - 1))
            self.snake.eat(1)
            return 1
        return 0

    def is_snake_alive(self):
        if (self.snake.x, self.snake.y) in self.snake.tail:
            return False
        if self.snake.x > self.width_tiles or self.snake.x < 0:
            return False
        if self.snake.y > self.height_tiles or self.snake.y < 0:
            return False
        return True

    def snake_logic(self):
        if not self.is_snake_alive():
            self.reset()
            return False
        return True

    def draw_snake(self):
        self._draw_rect(self.snake_head_color, (self.snake.x, self.snake.y))
        for body_part in self.snake.tail:
            self._draw_rect(self.snake_body_color, body_part)

    def draw_apple(self):
        self._draw_rect(self.apple_color, self.apple)

    def draw_score(self):
        text = self.font.render(str(self.snake.length), False, (0, 255, 0))
        self.screen.blit(text, (0, 0))

    def _draw_rect(self, color, pos):
        pygame.draw.rect(self.screen, color,
                         (pos[0] * self.scale, pos[1] * self.scale, self.scale, self.scale))

    def human_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not self.last_keys[pygame.K_LEFT]:
            self.turn = 1
        elif keys[pygame.K_RIGHT] and not self.last_keys[pygame.K_RIGHT]:
            self.turn = 2
        self.last_keys = keys

    def reset(self):
        self.snake = Snake(self.width_tiles // 2, self.height_tiles // 2)
        self.apple = (random.randint(0, self.width_tiles - 1), random.randint(0, self.height_tiles - 1))
