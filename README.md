# Hog-Dice-Game

Once you have downloaded the files, if you wish to play against a friend, enter the command: python3 hog_gui.py into your terminal and if you wish to play against a computer strategy, enter the command: python3 hog_gui.py -f into your terminal.

In Hog, two players alternate turns trying to be the first to end a turn with at least 100 total points. On each turn, the current player chooses some number of dice to roll, up to 10. That player's score for the turn is the sum of the dice outcomes. However, the following special rules apply:

Pig Out: If any of the dice outcomes is a 1, the current player's score for the turn is 1.
  Example 1: The current player rolls 7 dice, 5 of which are 1's. They score 1 point for the turn.
  Example 2: The current player rolls 4 dice, all of which are 3's. Since Pig Out did not occur, they score 12 points for the turn.

Free Bacon: A player who chooses to roll zero dice scores 2 * tens - ones, or 1, whichever is higher; where tens, ones are the digits of the opponent's score.
  Example 1: The opponent has 46 points, and the current player chooses to roll zero dice. 2 * 4 - 6 = 2; which is greater than 1, so the     current player gains 2 points.
  Example 2: The opponent has 73 points, and the current player chooses to roll zero dice. 2 * 7 - 3 = 11; which is greater than 1, so the   current player gains 11 points.
 
Swine Swap: After points for the turn are added to the current player's score, if the absolute difference between the last two digits of the current score and the last two digits of the opponent's score are the same, the scores are swapped.
  Example: The current player has a total score of 41 and the opponent has 83. The current player rolls two dice that total 8. The player's   new score is 49, and the opponent's score is 83. The absolute difference between the digits of the current score is |4 - 9| = |-5| = 5;     the absolute difference between the digits of the opponent's score is |8 - 3| = |5| = 5. The scores are swapped. The current player now     has 83 points and the opponent 49.
  

