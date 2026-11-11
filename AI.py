import random
from colorama import Fore, Back, Style, init
from copy import deepcopy

try:
    from Board import Board
except ModuleNotFoundError:
    print("Board.py is not found.")
    pass


TRIALS = 2000


class AI:
    def __init__(self, board):
        self.STYLES = board.STYLES
        self.board = board

    def run_experimental_analysis(self, trials):
        # play out the rest of the leg a bunch of times and count who wins
        counts = {}
        for color in self.board.STYLES:
            counts[color] = [0, 0]

        for i in range(trials):
            sim_board = deepcopy(self.board)
            remaining_colors = list(sim_board.pyramid.remaining_dice)
            while len(remaining_colors) > 0:
                color = random.choice(remaining_colors)
                remaining_colors.remove(color)
                value = random.choice(sim_board.pyramid.DIE_VALUES)
                sim_board.dice_tents.append((color, value))
                sim_board.move_camel((color, value))

            first, second = sim_board.get_rankings()
            counts[first][0] = counts[first][0] + 1
            counts[second][1] = counts[second][1] + 1

        results = {}
        for color in counts:
            results[color] = (counts[color][0] / trials, counts[color][1] / trials)
        return results

    def get_ticket_EV(self, ticket_value, prob_first, prob_second):
        prob_other = 1 - prob_first - prob_second
        return ticket_value * prob_first + prob_second - prob_other

    def get_roll_EV(self, trials=TRIALS):
        probs = self.run_experimental_analysis(trials)
        roll_evs = {}
        for color in self.board.STYLES:
            if color in self.board.ticket_tents and len(self.board.ticket_tents[color]) > 0:
                ticket_value = self.board.ticket_tents[color][0]
            else:
                ticket_value = 0
            roll_evs[color] = self.get_ticket_EV(ticket_value, probs[color][0], probs[color][1])
        return roll_evs

    def choose_best_ticket(self, trials=TRIALS):
        # figure out which ticket currently has the best expected value
        probs = self.run_experimental_analysis(trials)
        best_color = None
        best_ev = -999
        for color in self.board.ticket_tents:
            tickets = self.board.ticket_tents[color]
            if len(tickets) == 0:
                continue
            ticket_value = tickets[0]
            ev = self.get_ticket_EV(ticket_value, probs[color][0], probs[color][1])
            if ev > best_ev:
                best_ev = ev
                best_color = color
        return best_color, best_ev

    def choose_best_action(self, trials=TRIALS):
        # the computer bets if the best ticket beats rolling, otherwise it rolls
        best_color, best_ev = self.choose_best_ticket(trials)
        if best_color is None or best_ev <= 1:
            return "r", None, 0.0
        return "b", best_color, best_ev

    def __str__(self):
        exper = self.run_experimental_analysis(TRIALS)
        roll_evs = self.get_roll_EV(TRIALS)

        stats_str = " Experimental\n"
        stats_str += "   1st   2nd\n"
        for c in exper:
            row = (self.STYLES[c] + c + Style.RESET_ALL, exper[c][0], exper[c][1])
            stats_str += "{: >1} {: >5.2f} {: >5.2f}".format(*row) + "\n"

        stats_str += "\nExpected Value\n"
        for color in self.board.STYLES:
            stats_str += self.STYLES[color] + color + Style.RESET_ALL + ": " + "{:.2f}".format(roll_evs[color]) + "\n"

        advice_str = "Available bets: "
        best_ev = -10
        best_camel = "x"
        for color in self.board.ticket_tents:
            tickets_left = self.board.ticket_tents[color]
            if len(tickets_left) > 0:
                top_ticket_value = tickets_left[0]
                ev = self.get_ticket_EV(top_ticket_value, exper[color][0], exper[color][1])
                if ev > best_ev:
                    best_ev = ev
                    best_camel = color
                advice_str += "(" + color + ")" + self.STYLES[color] + str(top_ticket_value) + Style.RESET_ALL + " EV:{:.2f} ".format(ev)
            else:
                advice_str += "(" + color + ")" + self.STYLES[color] + "X" + Style.RESET_ALL + " "

        advice_str += "\nAI Advice: "
        if best_ev > 1:
            advice_str += "  Bet on " + self.STYLES[best_camel] + best_camel + Style.RESET_ALL + " with an expected value of {:.2f}\n".format(best_ev)
        else:
            advice_str += "  No camel has an EV > 1. You should roll instead of bet.\n"

        return stats_str + advice_str


if __name__ == "__main__":
    STYLES = {
        "r": Back.RED + Style.BRIGHT,
        "b": Back.BLUE + Style.BRIGHT,
        "g": Back.GREEN + Style.BRIGHT,
        "y": Back.YELLOW + Style.BRIGHT,
        "p": Back.MAGENTA
    }
    game_board = Board(STYLES)
    ai = AI(game_board)
    print(game_board)
    for i in range(3):
        rolled_die = game_board.roll_die()
        game_board.move_camel(rolled_die)
    print(game_board)
    print(ai)
    print(game_board)
