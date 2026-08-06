from colorama import Fore, Back, Style, init
import copy

try:
    from Board import Board
except ModuleNotFoundError:
    print("Board.py is not found.")
    pass
try:
    from Player import Player
except ModuleNotFoundError:
    print("Player.py is not found.")
    pass
try:
    from AI import AI
except ModuleNotFoundError:
    print("AI.py is not found.")
    pass


class CamelUp:
    def __init__(self, camel_styles, player_list):
        self.STYLES = camel_styles
        self.board = Board(self.STYLES)
        self.players = player_list
        self.ai = AI(self.board)

    def get_player_move(self, player):
        # computer players just ask the AI what to do
        if player.is_computer:
            action, ticket_color, ev = self.ai.choose_best_action()
            if action == 'b' and ticket_color:
                print(player.name + " chooses to bet on " + self.STYLES[ticket_color] + ticket_color + Style.RESET_ALL + " (EV: {:.2f})".format(ev))
            else:
                print(player.name + " chooses to roll.")
            return action

        print(player.name + "-", end=" ")
        choice = "not_an_option"
        while choice.lower() not in ["b", "r", "a"]:
            choice = input("(B)et or (R)oll or (A)dvice? ").lower()
        return choice

    def get_player_bet(self, player):
        if player.is_computer:
            ticket_color, ticket_ev = self.ai.choose_best_ticket()
            if ticket_color is None:
                print(player.name + " has no bets available and will roll instead.")
                return None
            print(player.name + " takes the " + self.STYLES[ticket_color] + ticket_color + Style.RESET_ALL + " ticket (EV: {:.2f})".format(ticket_ev))
            return ticket_color.lower()

        available_tickets = "Available bets: "
        for color in self.board.ticket_tents:
            tickets_left = self.board.ticket_tents[color]
            if len(tickets_left) > 0:
                top_ticket_value = tickets_left[0]
                available_tickets += "(" + color + ")" + self.STYLES[color] + str(top_ticket_value) + Style.RESET_ALL + " "
            else:
                available_tickets += "(" + color + ")" + self.STYLES[color] + "X" + Style.RESET_ALL + " "
        print(available_tickets)

        ticket_color = "not_an_option"
        while ticket_color.lower() not in self.STYLES.keys() or len(self.board.ticket_tents[ticket_color]) <= 0:
            ticket_color = input("Which betting ticket would you like to take?\n").lower()

        return ticket_color.lower()

    def play_leg(self):
        curr_player = 0
        while not self.board.is_leg_finished():
            player = self.players[curr_player]
            move = 'x'
            while move not in ['r', 'b', 'a']:
                move = self.get_player_move(player)

            if move == "a":
                print(self.display_with_advice())
                continue

            if move == "r":
                rolled_die = self.board.roll_die()
                self.board.move_camel(rolled_die)
                player.update_money(1)
            elif move == "b":
                ticket_color = self.get_player_bet(player)
                if ticket_color is not None:
                    ticket = self.board.take_ticket(ticket_color)
                    player.add_bet(ticket)

            print(self)
            curr_player = (curr_player + 1) % len(self.players)

    def process_leg_payouts(self):
        # first place pays the ticket value, second place pays $1, everyone else loses $1
        first, second = self.board.get_rankings()
        for player in self.players:
            for bet in player.bets:
                camel_color = bet[0]
                ticket_value = bet[1]
                if camel_color == first:
                    player.update_money(ticket_value)
                elif camel_color == second:
                    player.update_money(1)
                else:
                    player.update_money(-1)
        return first, second

    def __str__(self):
        game_str = str(self.board)
        for player in self.players:
            game_str += str(player) + "\n"
        return game_str

    def display_with_advice(self):
        game_str = str(self.board)
        game_str += "\n" + str(self.ai) + "\n"
        for player in self.players:
            game_str += str(player) + "\n"
        return game_str


def prompt_game_mode():
    STYLES = {
        "r": Back.RED + Style.BRIGHT,
        "b": Back.BLUE + Style.BRIGHT,
        "g": Back.GREEN + Style.BRIGHT,
        "y": Back.YELLOW + Style.BRIGHT,
        "p": Back.MAGENTA
    }

    print("Welcome to Camel Up!")
    mode = ""
    while mode not in ["1", "2"]:
        mode = input("Select mode:\n  1) Single Player vs Computer\n  2) Multi Player\nEnter 1 or 2: ").strip()

    players = []
    if mode == "1":
        human_name = input("Enter your name: ").strip()
        if human_name == "":
            human_name = "Player 1"
        players.append(Player(human_name, STYLES))

        computer_name = input("Enter a name for the computer opponent (or press Enter for 'Computer'): ").strip()
        if computer_name == "":
            computer_name = "Computer"
        players.append(Player(computer_name, STYLES, is_computer=True))
    else:
        num_players = 0
        while num_players < 2:
            entry = input("How many players? ").strip()
            if entry.isdigit():
                num_players = int(entry)
            if num_players < 2:
                print("Please enter a number of players of 2 or more.")

        for i in range(num_players):
            name = input("Enter name for player " + str(i + 1) + ": ").strip()
            if name == "":
                name = "Player " + str(i + 1)
            players.append(Player(name, STYLES))

    return players, STYLES


if __name__ == "__main__":
    init(autoreset=True)
    players, STYLES = prompt_game_mode()
    game = CamelUp(STYLES, players)
    print(game)
    game.play_leg()
    first, second = game.process_leg_payouts()

    print(game.STYLES[first] + first + Style.RESET_ALL + " comes in 1st🥇🥇🥇!")
    print(game.STYLES[second] + second + Style.RESET_ALL + " comes in 2nd🥈🥈🥈!")

    for player in game.players:
        print(player.name + " ended the leg with " + str(player.money) + " coins.")
