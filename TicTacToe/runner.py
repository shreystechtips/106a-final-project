from player import Player
from game import Game
from random_bot import RandomBot
from human_bot import HumanBot

def main():
    xbot = RandomBot(Player.x)
    obot = HumanBot(Player.o)
    game = Game(1)
    game.play(xbot, obot)

if __name__ == '__main__':
    main()