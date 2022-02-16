from classes import Game
from time import sleep


def play(rounds=50):
    game = Game(6)
    for i in range(rounds):
        game.good_morning()
        print(game.stats.T)
        print()
    for miner in game.miners:
        print(miner.probs)


if __name__ == '__main__':
    play(500)
