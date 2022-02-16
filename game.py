from classes import Game
from time import sleep
import numpy as np


def play(rounds=50):
    thieves = []
    game = Game(8)
    for i in range(rounds):
        game.good_morning()
    print(game.stats.T)
    print()
    for miner in game.miners:
        print(miner.probs)


if __name__ == '__main__':
    play(500)
