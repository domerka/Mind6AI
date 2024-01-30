from Player import *
import random


class Mind6:
    # Constructor
    def __init__(self, num_of_players):
        self.num_of_players = num_of_players
        self.board = [[], [], [], []]
        self.deck = []
        self.players = []
        for i in range(num_of_players):
            self.players.append(Player("Player" + str(i)))
        self.next_turn()

    def next_turn(self):
        self.deck = list(range(1, 105))
        self.shuffle_cards()
        self.draw_player_cards()
        self.draw_board_cards()

    def draw_player_cards(self):
        for i in range(len(self.players)):
            for _ in range(10):
                self.players[i].cards.append(self.deck.pop())

    def shuffle_cards(self):
        random.shuffle(self.deck)

    def draw_board_cards(self):
        self.board = [[], [], [], []]
        for i in range(4):
            self.board[i].append(self.deck.pop())

