import random
from colorama import Fore, Back, Style, init

try:
    from Pyramid import Pyramid
except ModuleNotFoundError:
    print("Pyramid.py is not found.")
    pass


class Board:
    def __init__(self, STYLES):
        self.TRACK_LENGTH = 16
        self.STYLES = STYLES

        self.track = []
        for i in range(self.TRACK_LENGTH):
            self.track.append([])

        self.pyramid = Pyramid(self.STYLES)
        self.place_camels()
        self.ticket_tents = {}
        self.dice_tents = []
        self.reset_leg()

    def place_camels(self):
        # stack all 5 camels in random order on the first spot of the track
        self.track = []
        for i in range(self.TRACK_LENGTH):
            self.track.append([])

        starting_camels = list(self.STYLES.keys())
        random.shuffle(starting_camels)
        self.track[0] = starting_camels

    def reset_leg(self):
        # new leg = fresh dice and fresh betting tickets, camels stay put
        self.pyramid.reset_leg()
        self.ticket_tents = {}
        for color in self.STYLES.keys():
            self.ticket_tents[color] = [5, 3, 2, 2]
        self.dice_tents = []

    def roll_die(self):
        roll = self.pyramid.shake()
        self.dice_tents.append(roll)
        return roll

    def move_camel(self, die):
        if not die or len(die) != 2:
            return

        color = die[0]
        steps = die[1]
        if steps <= 0 or color not in self.STYLES:
            return

        # find the tile the camel is on, pick it (and anyone stacked on top) up
        for tile_index in range(len(self.track)):
            stack = self.track[tile_index]
            if color in stack:
                camel_index = stack.index(color)
                moved_camels = stack[camel_index:]
                self.track[tile_index] = stack[:camel_index]

                new_spot = tile_index + steps
                if new_spot >= self.TRACK_LENGTH:
                    # camel crossed the finish line, just park it on the last tile
                    new_spot = self.TRACK_LENGTH - 1

                self.track[new_spot] = self.track[new_spot] + moved_camels
                return

    def take_ticket(self, color):
        if color not in self.ticket_tents:
            return (color, 0)
        if len(self.ticket_tents[color]) == 0:
            return (color, 0)
        value = self.ticket_tents[color].pop(0)
        return (color, value)

    def is_leg_finished(self):
        # once all 5 dice have rolled, the leg is over
        return len(self.dice_tents) >= 5

    def get_rankings(self):
        # walk backwards from the end of the track to see who is winning
        for i in range(self.TRACK_LENGTH - 1, -1, -1):
            if len(self.track[i]) != 0:
                first = self.track[i][-1]
                if len(self.track[i]) > 1:
                    second = self.track[i][-2]
                    return (first, second)

                for j in range(i - 1, -1, -1):
                    if len(self.track[j]) != 0:
                        second = self.track[j][-1]
                        return (first, second)

        return ("", "")

    def __str__(self):
        board_string = ""
        ticket_string = "Ticket Tents: "
        for ticket_color in self.ticket_tents:
            if len(self.ticket_tents[ticket_color]) > 0:
                next_ticket_value = str(self.ticket_tents[ticket_color][0])
            else:
                next_ticket_value = 'X'
            ticket_string = ticket_string + self.STYLES[ticket_color] + next_ticket_value + Style.RESET_ALL + " "
        board_string = board_string + ticket_string + "\t\t"

        dice_string = "Dice Tents: "
        for die in self.dice_tents:
            dice_string = dice_string + self.STYLES[die[0]] + str(die[1]) + Style.RESET_ALL + " "
        for i in range(5 - len(self.dice_tents)):
            dice_string = dice_string + Back.WHITE + " " + Style.RESET_ALL + " "

        board_string = board_string + dice_string + "\n"

        for row in range(4, -1, -1):
            row_str = [" "] * 16
            for i in range(len(self.track)):
                for camel_place in range(len(self.track[i])):
                    camel = self.track[i][camel_place]
                    if camel_place == row:
                        row_str[i] = self.STYLES[camel] + camel + Style.RESET_ALL
            board_string = board_string + "🌴 " + "   ".join(row_str) + " |🏁\n"

        bottom_row = "   "
        for i in range(1, 10):
            bottom_row = bottom_row + str(i) + "   "
        for i in range(10, 17):
            bottom_row = bottom_row + str(i) + "  "
        board_string = board_string + bottom_row

        return board_string


if __name__ == "__main__":
    STYLES = {
        "r": Back.RED + Style.BRIGHT,
        "b": Back.BLUE + Style.BRIGHT,
        "g": Back.GREEN + Style.BRIGHT,
        "y": Back.YELLOW + Style.BRIGHT,
        "p": Back.MAGENTA
    }
    board = Board(STYLES)
    print(str(board) + "\n")
    board.move_camel(("r", 2))
    print(str(board) + "\n")

    num_rolls = 2
    for i in range(num_rolls):
        rolled_die = board.roll_die()
        board.move_camel(rolled_die)
        print(str(rolled_die) + " was shaken from the pyramid")
    print(board.pyramid)
    ticket = board.take_ticket(rolled_die[0])
    print("Player took a " + rolled_die[0] + " ticket: " + str(ticket))
    print(board)

    first, second = board.get_rankings()
    print("First place: " + first + ", Second place: " + second)
    print("\nResetting leg...")
    board.reset_leg()
    print(board)
