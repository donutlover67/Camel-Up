from colorama import Fore, Back, Style, init


class Player:
    def __init__(self, name, camel_styles, is_computer=False):
        # everybody starts with 3 coins
        self.money = 3
        self.bets = []
        self.name = name
        self.STYLES = camel_styles
        self.is_computer = is_computer

    def update_money(self, amount):
        # amount can be positive (win) or negative (loss)
        self.money = self.money + amount

    def add_bet(self, ticket):
        self.bets.append(ticket)

    def reset_leg(self):
        # clear out betting tickets when a new leg starts
        self.bets = []

    def __str__(self):
        player_string = "\n" + self.name + " has " + str(self.money) + " coins."
        if len(self.bets) > 0:
            bets_string = ""
            for bet in self.bets:
                bets_string = bets_string + self.STYLES[bet[0]] + str(bet[1]) + Style.RESET_ALL + " "
            player_string = player_string + " Betting Tickets: " + bets_string
        return player_string


if __name__ == "__main__":
    STYLES = {
        "r": Back.RED + Style.BRIGHT,
        "b": Back.BLUE + Style.BRIGHT,
        "g": Back.GREEN + Style.BRIGHT,
        "y": Back.YELLOW + Style.BRIGHT,
        "p": Back.MAGENTA
    }
    player = Player("Dave", STYLES)
    player.add_bet(('y', 5))
    player.add_bet(('b', 3))
    player.update_money(-1)
    print(player)
