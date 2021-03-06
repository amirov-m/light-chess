#!/usr/bin/python3

from engine.game import Game
from entities.board import Board


def main():
    _ = Board.create_start_board()
    _ = Game.create_start_game()


if __name__ == "__main__":
    main()
