from typing import Tuple

import gym
import numpy as np
import numpy.linalg.linalg
import pygame
from gym import spaces

from game.board import Board


class SnakeGym(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, width, height, scale=10):
        super(SnakeGym, self).__init__()
        self.action_space = spaces.Discrete(3)
        self.view_x = 51
        self.view_y = 51
        self.observation_space = spaces.Box(0, 2, (self.view_x, self.view_y, 2), dtype=np.int)
        self.steps_since_eat = 1
        self.game = Board(width, height, scale=scale, render=True)
        self.last_distance = 0

    def step(self, action):
        if action == 1:
            self.game.snake.turn_left()
        elif action == 2:
            self.game.snake.turn_right()
        self.game.snake.forward()
        done = not self.game.snake_logic()
        ate = self.game.apple_logic()
        if ate:
            self.steps_since_eat = 1
        else:
            self.steps_since_eat += 1
        proximity_reward = 1 / max(numpy.linalg.norm(np.array(self.game.apple) - np.array(self.game.snake.get_pos())),
                                   1)
        change_distance = proximity_reward - self.last_distance
        self.last_distance = proximity_reward
        reward = (change_distance) + (proximity_reward * (10 / self.steps_since_eat)) + (ate * 10)
        if done:
            reward = -100
        obs = self._next_observation()
        self.render()
        print("\r" + str(reward), end="")
        return obs, reward, done, {}

    def render(self, mode="human"):
        if mode == "human":
            pygame.event.pump()
            self.game.reset_screen()
            self.game.draw_snake()
            self.game.draw_apple()
            self.game.draw_score()
            self.game.update_screen()

    def reset(self):
        self.game.reset()
        return self._next_observation()

    def _next_observation(self):
        snake_view = np.zeros((self.view_x, self.view_y, 2))
        snake_view[self.view_x // 2, self.view_y // 2, 0] = 1
        self._place_rect(snake_view, 2, self.game.apple, 1)
        for body in self.game.snake.tail:
            self._place_rect(snake_view, 2, body)
        self._place_border(snake_view)

        snake_view = np.rot90(snake_view, -self.game.snake.direction)

        return snake_view

    def _place_rect(self, view, value, pos, channel=0):
        x = pos[0] - self.game.snake.x + self.view_x // 2
        y = pos[1] - self.game.snake.y + self.view_y // 2

        if 0 <= x < self.view_x and 0 <= y < self.view_y:
            view[x, y, channel] = value
            return view
        return view

    def _place_border(self, view):
        for x in range(self.view_x):
            for y in range(self.view_y):
                x_pos = x + self.game.snake.x - self.view_x // 2
                y_pos = y + self.game.snake.y - self.view_y // 2
                if x_pos == -1 or x_pos == self.game.width_tiles or y_pos == -1 or y_pos == self.game.height_tiles:
                    view[x, y, 0] = 1
        return view
