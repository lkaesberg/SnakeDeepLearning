import time

import pygame

from train.snake_gym import SnakeGym
from stable_baselines3 import PPO


def main():
    width = 50
    height = 50
    restart = False
    train = True

    snake_gym = SnakeGym(width, height, 20)
    if restart:
        model = PPO("MlpPolicy", snake_gym, verbose=1)
    else:
        model = PPO.load("snake", snake_gym)
    if train:
        model.learn(total_timesteps=600000)
        model.save("snake")
    obs = snake_gym.reset()
    last_time = time.time()
    while not pygame.key.get_pressed()[pygame.K_ESCAPE]:
        if time.time() - last_time > 0.2:
            action, _states = model.predict(obs)
            obs, rewards, done, info = snake_gym.step(action)
            for line in obs:
                for point in line:
                    print(point[0], end="")
                print()
            print()
            last_time = time.time()
        snake_gym.render()


if __name__ == '__main__':
    main()
