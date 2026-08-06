import random
from colorama import Fore, Back, Style, init


class Pyramid:
    def __init__(self, camel_styles):
        # the dice colors just come from whatever camels are in the game
        self.STYLES = camel_styles
        self.DIE_VALUES = [1, 2, 3]
        self.DIE_COLORS = list(self.STYLES.keys())
        self.remaining_dice = []
        self.reset_leg()

    def shake(self):
        # grab a random color that hasn't rolled yet, roll it 1-3
        if len(self.remaining_dice) > 0:
            dice_choice = random.choice(self.remaining_dice)
            self.remaining_dice.remove(dice_choice)
            dice_value = random.choice(self.DIE_VALUES)
            return (dice_choice, dice_value)
        return ("", 0)

    def reset_leg(self):
        # put every color back in the pyramid
        self.remaining_dice = list(self.STYLES.keys())

    def __str__(self):
        dice_str = "Remaining dice: "
        for die in self.remaining_dice:
            dice_str = dice_str + self.STYLES[die] + die + Style.RESET_ALL + " "
        return dice_str


if __name__ == "__main__":
    STYLES = {
        "r": Back.RED + Style.BRIGHT,
        "b": Back.BLUE + Style.BRIGHT,
        "g": Back.GREEN + Style.BRIGHT,
        "y": Back.YELLOW + Style.BRIGHT,
        "p": Back.MAGENTA
    }
    pyramid = Pyramid(STYLES)
    print(pyramid)
    num_rolls = 3
    for i in range(num_rolls):
        rolled_die = pyramid.shake()
        print(str(rolled_die) + " was shaken from the pyramid")
    print(pyramid)
