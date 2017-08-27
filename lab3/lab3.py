# 6.034 Fall 2010 Lab 3: Games
# Name: <Your Name>
# Email: <Your Email>

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 3

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 2

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)

## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    if board.is_win() == board.get_current_player_id(): return 1000;
    if board.is_win() == board.get_other_player_id(): return -1000;
    if board.is_game_over(): return 0;
    return 4 - board.longest_chain(board.get_current_player_id());

## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.

def alphabeta_helper(board,depth,eval_fn,get_next_moves_fn,is_terminal_fn,alphabeta):
    if is_terminal_fn(depth,board):
        return eval_fn(board);
    alphabeta.append(NEG_INFINITY);
    for move, new_board in get_next_moves_fn(board):
        val = -1 * alphabeta_helper(new_board, depth - 1, eval_fn,
                                            get_next_moves_fn, is_terminal_fn,alphabeta);
        alphabeta[-1] = max(alphabeta[-1],val);
        if -alphabeta[-1] <= alphabeta[-2]: break;
    return alphabeta.pop();

def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):


    best_val = None

    alphabeta = [NEG_INFINITY];
    for move, new_board in get_next_moves_fn(board):
        val = -1 * alphabeta_helper(new_board, depth - 1, eval_fn,
                                            get_next_moves_fn,
                                            is_terminal_fn,alphabeta)
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)
        alphabeta[0] = max(alphabeta[0],val);
    return best_val[1]


## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
alphabeta_player = lambda board: alpha_beta_search(board,
                                                   depth=8,
                                                   eval_fn=focused_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)

## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.



def get_for(board,player):
    cell_vals = [[3, 4, 5, 7, 5, 4, 3],[4, 6, 8, 10, 8, 6, 4], [5, 8, 11, 13, 11, 8, 5],[5, 8, 11, 13, 11, 8, 5], [4, 6, 8, 10, 8, 6, 4], [3, 4, 5, 7, 5, 4, 3]];
    ret = 0;
    vis = set();
    for chain in board.chain_cells(player):
        for cell in chain:
            if cell not in vis:
                x,y = cell;
                vis.add(cell);
                ret += cell_vals[x][y];
    return ret;

def chain_score(chain,board):
    if len(chain) == 1:return 0
    chain = list(chain);
    chain.sort();
    x,y = chain[0];
    dx = chain[1][0] - x;
    dy = chain[1][1] - y;
    H = min(max(lambda cell: cell[1],chain));
    L = len(chain);
    need = 4 - L;
    if dy == 0:
        h = board.get_height_of_column(y);
        if h == -1: return 0;
        have = h+1;
        if have < need: return 0;
        if h + 1 != H: return 0;
        return (L - 1)*100;

    nxtrow = x + (L + 1)*dx;
    nxtcol = y + (L + 1)*dy;
    prvrow = x - dx;
    prvcol = y - dy;
    ret = 0;
    if prvcol:
        h = board.get_height_of_column(prvcol);
        if h >= prvrow:
            ret += (L - 1)*100;
    if nxtcol < 7:
        h = board.get_height_of_column(nxtcol);
        if h >= nxtcol:
            ret += (L - 1) * 100;
    return ret;

def get_merge_cost(board):
    player1 = board.get_current_player_id();
    player2 = board.get_other_player_id();
    grid = [[0 for j in xrange(7)] for i in xrange(6)];
    for chain in board.chain_cells(player1):
        for x,y in chain:
            grid[x][y] = player1;
    for chain in board.chain_cells(player2):
        for x, y in chain:
            grid[x][y] = player2;
    board_tuples = tuple(max(lambda x:tuple(x),grid));
    other_board = ConnectFourBoard(board_array = board_tuples,
                                    current_player = player2);

    L1 = board.longest_chain(player1);
    L2 = board.longest_chain(player2);

    ret = 0;
    for move,new_board in get_all_next_moves(board):
        if new_board.is_win() == player1: return INFINITY;

    return ret;



def better_evaluate(board):
    if board.is_win() == board.get_current_player_id(): return INFINITY;
    if board.is_win() == board.get_other_player_id(): return NEG_INFINITY;
    if board.is_game_over(): return NEG_INFINITY;

    player1 = board.get_current_player_id();
    player2 = board.get_other_player_id();
    score1 = get_for(board,player1);
    score2 = get_for(board,player2);
    if get_merge_cost(board) != 0: return INFINITY;
    ret = score1 - score2 ;
    ret = max(ret,NEG_INFINITY);
    ret = min(ret,INFINITY);
    return ret;
# Comment this line after you've fully implemented better_evaluate
#better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
#better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,1,0,1,2,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))
    #print eval_chain(((4,3),(3,2),(2,1)),2,test_board_2);

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = True

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "3"
WHAT_I_FOUND_INTERESTING = "alpha beta and the eval functions"
WHAT_I_FOUND_BORING = "none"
NAME = "Noureldin"
EMAIL = "noureldinyosri@gmail.com"

