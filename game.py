from classes import Game
from time import sleep


def play(rounds=50):
    game = Game()
    for i in range(rounds):
        game.good_morning()
        print(game.stats)
        print()


if __name__ == '__main__':
    play()