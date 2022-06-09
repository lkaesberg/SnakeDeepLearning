import pygame

from game.board import Board


def main():
    board = Board(200, 200, 0.1)
    board.start()


if __name__ == '__main__':
    main()
