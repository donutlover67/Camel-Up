A Python command-line implementation of the board game Camel Up.
Built with starter code from Jane Street AMP, I created a custom pyramid/dice system, 
a stacking-camel race track, and a betting-ticket economy.

Goal: Play solo against a computer opponent that uses a Monte Carlo simulation to estimate each 
camel's odds of finishing 1st/2nd and picks the highest expected-value bet, or play 
locally with 2+ human players. 

Features:

Full round simulation: shake the pyramid, move camels, track stacked positions
Betting ticket system with variable payouts based on final camel rankings.

AI opponent powered by ~2,000-trial Monte Carlo rollouts to compute win probabilities 
and expected value.

In-game "advice" mode so human players can see the same odds the AI sees.

*The board renders in the terminal with colorama for colored 
camels, dice, and betting tickets.*

run code:
pip install colorama
python CamelUp.py
