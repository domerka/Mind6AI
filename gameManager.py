import tkinter
import tkinter as tk
from Mind6 import *


class GameManager:

    # Constructor
    def __init__(self):
        self.board_uis = []
        self.player_uis = {}

    def start(self):
        # Create window
        window = tk.Tk()
        # Set window size
        window.geometry("1000x600")

        # Create the game with the number of players
        mind6game = Mind6(4)

        # Display the players and their cards
        self.initialize_players(window, mind6game.num_of_players, mind6game.players, mind6game)

        # Displays the board
        self.initialize_board(window, mind6game.board)

        # Bind the function to the Enter key press event
        window.bind("<Return>", lambda event: self.play_turn(event, window, mind6game))

        # Run it until closed
        window.mainloop()

    def play_turn(self, event, window, mind6game):
        players = mind6game.players
        board = mind6game.board
        played_cards = {}

        # Each player chooses a card to play
        # This is what the AI has a say on
        for i in range(len(players)):
            played_cards[i] = players[i].cards.pop()

        # Sort the cards
        sorted_dict = dict(sorted(played_cards.items(), key=lambda item: item[1]))

        # Put the cards on the board
        while len(sorted_dict) > 0:
            player, smallest_card = list(sorted_dict.items())[0]
            del sorted_dict[player]

            # Which row it goes into
            row_index = -1
            diff = 105
            for i in range(len(board)):
                compare_card = board[i][-1]
                if smallest_card > compare_card:
                    if (smallest_card - compare_card) < diff:
                        diff = smallest_card - compare_card
                        row_index = i

            # No row was selected --> the player chooses which row to take
            # Its coded so the row wih the least amount of points is taken
            if row_index == -1:
                board_index = 0
                min_board_val = self.calculate_cards_worth(board[0])
                for i in range(1, 4):
                    board_val = self.calculate_cards_worth(board[i])
                    if board_val < min_board_val:
                        board_index = i
                        min_board_val = board_val

                cards_to_take = board[board_index]
                board[board_index] = [smallest_card]
                mind6game.players[player].points += min_board_val
            # Row has no more spaces left --> player takes the cards
            elif len(board[row_index]) == 5:
                cards_to_take = board[row_index]
                board[row_index] = [smallest_card]
                points_to_add = self.calculate_cards_worth(cards_to_take)
                mind6game.players[player].points += points_to_add
            # The card just slides to the end of the row
            else:
                board[row_index].append(smallest_card)

        self.update_board_ui(board)
        self.update_player_ui(players)

    def calculate_cards_worth(self, cards):
        points = 0
        for card in cards:
            if card == 55:
                points += 7
            elif (card == 11 or card == 22 or card == 33 or card == 44
                  or card == 66 or card == 77 or card == 88 or card == 99):
                points += 5
            elif (card == 10 or card == 20 or card == 30 or card == 40 or card == 60
                  or card == 70 or card == 80 or card == 90 or card == 100):
                points += 3
            elif (card == 5 or card == 15 or card == 25 or card == 35 or card == 45
                  or card == 65 or card == 75 or card == 85 or card == 95):
                points += 2
            else:
                points += 1
        return points

    def initialize_board(self, window, board):
        for i in range(4):
            board_frame = tk.Frame(window)
            board_frame.grid(row=i, column=1, padx=10, pady=10)
            board_label = tk.Label(board_frame, text=board[i][0], font=("Helvetica", 10))
            board_label.grid(row=0, column=0, padx=10, pady=10)
            self.board_uis.append(board_label)

    def update_board_ui(self, board):
        for i in range(len(self.board_uis)):
            text = ""
            for card in board[i]:
                text += str(card) + "  "
            self.board_uis[i].config(text=text)

    def initialize_players(self, window, num_of_players, players, mind6game):
        for i in range(num_of_players):
            player = players[i]
            player_frame = tk.Frame(window)
            player_frame.grid(row=i, column=0, padx=10, pady=10)
            name_label = tk.Label(player_frame, text=player.name, font=("Helvetica", 10))
            name_label.grid(row=0, column=0, padx=10, pady=10)

            point_label = tk.Label(player_frame, text=player.points, font=("Helvetica", 10))
            point_label.grid(row=0, column=1, padx=10, pady=10)
            player.point_label = point_label

            cards = player.cards
            for j in range(len(cards)):
                self.initialize_player_cards(j, cards[j], player_frame, player)

    def update_player_ui(self, players):
        for player in players:
            player.point_label.config(text=player.points)
            for card_label in player.card_labels:
                if int(card_label.cget("text")) not in player.cards:
                    card_label.destroy()
                    break

    def initialize_player_cards(self, i, num, parent_frame, player):
        card_label = tk.Label(parent_frame, text=num, font=("Helvetica", 10))
        card_label.grid(row=1, column=i, padx=5, pady=5)
        player.card_labels.append(card_label)


if __name__ == "__main__":
    manager = GameManager()
    manager.start()
