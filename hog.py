
from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    pig = False
    roll = 0
    sum = 0
    while roll < num_rolls:
    	numb = dice()
    	if numb == 1:
    		pig = True
    	sum += numb
    	roll += 1
    if pig == True:
    	return 1
    else:
    	return sum


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    tens = score // 10
    ones = score % 10
    if 2*tens - ones > 1:
    	return 2*tens - ones
    else:
    	return 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    if num_rolls == 0:
    	return free_bacon(opponent_score)
    else:
    	return roll_dice(num_rolls, dice)


def is_swap(player_score, opponent_score):
    """
    Return whether the current player's score has the same absolute
    difference between its last two digits as the opponent's score.
    """
    playerones = player_score % 10
    player_score = player_score // 10
    playertens = player_score % 10
    oppones = opponent_score % 10
    opponent_score = opponent_score // 10
    opptens = opponent_score % 10

    if abs(playertens - playerones) == abs(opptens - oppones):
    	return True
    else:
    	return False


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def silence(score0, score1):
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    while score0 < goal and score1 < goal:
    	score0 += take_turn(strategy0(score0,score1), score1, dice)
    	if is_swap(score0, score1) == True:
    		score0, score1 = score1, score0
    	if score0 < goal and score1 < goal:
    		score1 += take_turn(strategy1(score1,score0), score0, dice)
    		if is_swap(score1, score0) == True:
    			score0, score1 = score1, score0

    	say = say(score0, score1)

    return score0, score1



def say_scores(score0, score1):
	"""A commentary function that announces the score for each player."""
	print("Player 0 now has", score0, "and Player 1 now has", score1)
	return say_scores

def announce_lead_changes(previous_leader=None):
	"""Return a commentary function that announces lead changes.

	>>> f0 = announce_lead_changes()
	>>> f1 = f0(5, 0)
	Player 0 takes the lead by 5
	>>> f2 = f1(5, 12)
	Player 1 takes the lead by 7
	>>> f3 = f2(8, 12)
	>>> f4 = f3(8, 13)
	>>> f5 = f4(15, 13)
	Player 0 takes the lead by 2
	"""
	def say(score0, score1):
		if score0 > score1:
			leader = 0
		elif score1 > score0:
			leader = 1
		else:
			leader = None
		if leader != None and leader != previous_leader:
			print('Player', leader, 'takes the lead by', abs(score0 - score1))
		return announce_lead_changes(leader)
	return say

def both(f, g):
	"""Return a commentary function that says what f says, then what g says.

	>>> h0 = both(say_scores, announce_lead_changes())
	>>> h1 = h0(10, 0)
	Player 0 now has 10 and Player 1 now has 0
	Player 0 takes the lead by 10
	>>> h2 = h1(10, 6)
	Player 0 now has 10 and Player 1 now has 6
	>>> h3 = h2(6, 17) # Player 0 gets 7 points, then Swine Swap applies
	Player 0 now has 6 and Player 1 now has 17
	Player 1 takes the lead by 11
	"""
	def say(score0, score1):
		return both(f(score0, score1), g(score0, score1))
	return say


def announce_highest(who, previous_high=0, previous_score=0):
	"""Return a commentary function that announces when WHO's score
	increases by more than ever before in the game.

	>>> f0 = announce_highest(1) # Only announce Player 1 score gains
	>>> f1 = f0(12, 0)
	>>> f2 = f1(12, 11)
	11 point(s)! That's the biggest gain yet for Player 1
	>>> f3 = f2(20, 11)
	>>> f4 = f3(13, 20) # Player 1 gets 2 points, then Swine Swap applies
	>>> f5 = f4(20, 35) # Player 0 gets 22 points, then Swine Swap applies
	15 point(s)! That's the biggest gain yet for Player 1
	>>> f6 = f5(20, 47) # Player 1 gets 12 points; not enough for a new high
	>>> f7 = f6(21, 47)
	>>> f8 = f7(21, 77)
	30 point(s)! That's the biggest gain yet for Player 1
	>>> f9 = f8(77, 22) # Swap!
	>>> f10 = f9(33, 77) # Swap!
	55 point(s)! That's the biggest gain yet for Player 1
	"""
	assert who == 0 or who == 1, 'The who argument should indicate a player.'
	
	def highest(score0, score1):
		nonlocal previous_high, previous_score, who
		if who==0:
			score = score0
		else:
			score = score1

		if score-previous_score>previous_high:
			high = score-previous_score
			print(high, "point(s)! That's the biggest gain yet for Player", who)
		else:
			high = previous_high
		return announce_highest(who, high, score)

	return highest


def always_roll(n):
	"""Return a strategy that always rolls N dice.

	A strategy is a function that takes two total scores as arguments (the
	current player's score, and the opponent's score), and returns a number of
	dice that the current player will roll this turn.

	>>> strategy = always_roll(5)
	>>> strategy(0, 0)
	5
	>>> strategy(99, 99)
	5
	"""
	def strategy(score, opponent_score):
		return n
	return strategy


def make_averaged(fn, num_samples=1000):
	"""Return a function that returns the average value of FN when called.

	To implement this function, you will have to use *args syntax, a new Python
	feature introduced in this project.  See the project description.

	>>> dice = make_test_dice(4, 2, 5, 1)
	>>> averaged_dice = make_averaged(dice, 1000)
	>>> averaged_dice()
	3.0
	"""
	def averaged(*args):
		counter = 0
		total = 0
		while counter<num_samples:
			total += fn(*args)
			counter += 1
		return total/num_samples
	return averaged


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
	"""Return the number of dice (1 to 10) that gives the highest average turn
	score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
	Assume that the dice always return positive outcomes.

	>>> dice = make_test_dice(1, 6)
	>>> max_scoring_num_rolls(dice)
	1
	"""
	roll = 1
	largest, rollnum = 0, 0
	while roll<=10:
		if make_averaged(roll_dice, num_samples)(roll, dice)>largest:
			largest, rollnum = make_averaged(roll_dice, num_samples)(roll, dice), roll
		roll += 1
	return rollnum


def winner(strategy0, strategy1):
	"""Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
	score0, score1 = play(strategy0, strategy1)
	if score0 > score1:
		return 0
	else:
		return 1


def average_win_rate(strategy, baseline=always_roll(4)):
	"""Return the average win rate of STRATEGY against BASELINE. Averages the
	winrate when starting the game as player 0 and as player 1.
	"""
	win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
	win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

	return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
	"""Run a series of strategy experiments and report results."""
	if True:  # Change to False when done finding max_scoring_num_rolls
		six_sided_max = max_scoring_num_rolls(six_sided)
		print('Max scoring num rolls for six-sided dice:', six_sided_max)

	if False:  # Change to True to test always_roll(8)
		print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

	if False:  # Change to True to test bacon_strategy
		print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

	if False:  # Change to True to test swap_strategy
		print('swap_strategy win rate:', average_win_rate(swap_strategy))

	if False:  # Change to True to test final_strategy
		print('final_strategy win rate:', average_win_rate(final_strategy))

	"*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
	"""This strategy rolls 0 dice if that gives at least MARGIN points, and
	rolls NUM_ROLLS otherwise.
	"""
	if free_bacon(opponent_score) >= margin:
		return 0
	else:
		return num_rolls


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
	"""This strategy rolls 0 dice when it triggers a beneficial swap. It also
	rolls 0 dice if it gives at least MARGIN points and does not trigger a
	non-beneficial swap. Otherwise, it rolls NUM_ROLLS.
	"""
	if score<opponent_score:
		if free_bacon(opponent_score)>=margin or is_swap(free_bacon(opponent_score)+score, opponent_score):
			return 0
		else:
			return num_rolls
	else:
		if free_bacon(opponent_score)>=margin and not is_swap(free_bacon(opponent_score)+score, opponent_score):
			return 0
		else:
			return num_rolls


def final_strategy(score, opponent_score):
	rolling = 8
	freebacon = free_bacon(opponent_score)
	swap = opponent_score - score
	def winning():
		if max(rolling, freebacon) == freebacon:
			if is_swap(score+free_bacon(opponent_score),opponent_score):
				return 6
			if is_swap(score+free_bacon(opponent_score), opponent_score + 1):
				return 6
			else:
				return 0
		if is_swap(score+1, opponent_score):
			return 1
		return 6

	def losing():
		if max(rolling, freebacon, swap) == swap:
			if is_swap(score+1, opponent_score):
				return 10
			if is_swap(score + free_bacon(opponent_score), opponent_score):
				return 0
			if finder(score, opponent_score):
				return finder(score, opponent_score)
		if max(rolling, freebacon) == freebacon:
			return 0
		return 6
	if score > opponent_score:
		return winning()
	return losing()

def finder(score, opponent_score):
	n = 1
	a, b, c, d, e = 3, 6, 7, 8, 9
	if is_swap(score+3, opponent_score):
		return 1
	if is_swap(score+6, opponent_score):
		return 2
	if is_swap(score+7, opponent_score):
		return 3
	if is_swap(score+8, opponent_score):
		return 4
	if is_swap(score+9, opponent_score):
		return 6
	return 0
	


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
	"""Read in the command-line argument and calls corresponding functions.	"""
	
	import argparse
	parser = argparse.ArgumentParser(description="Play Hog")
	parser.add_argument('--run_experiments', '-r', action='store_true',
						help='Runs strategy experiments')

	args = parser.parse_args()

	if args.run_experiments:
		run_experiments()