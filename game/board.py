import pygame
from game.snake import Snake

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = Snake(width//2,height//2)


    def start(self):
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake - DeepLearning')
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
