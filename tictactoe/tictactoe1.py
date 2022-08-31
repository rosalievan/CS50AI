"""
Tic Tac Toe Player
"""

import math
import numpy as np
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = []
    for list in board:
        for item in list:
            flat_board.append(item)

    print(flat_board)

    xcount = flat_board.count('X')
    ocount = flat_board.count('O')

    if xcount <= ocount:
        return 'X'
    else:
        return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionset = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            tuple = (i, j)
            if board[i][j] == EMPTY:
                actionset.add(tuple)
    return actionset


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not action in actions(board):
        raise Exception('sorry, that action is not available')
    newboard = copy.deepcopy(board)
    newboard[action[0]][action[1]] = player(board)

    return newboard


                
def checkRows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return None

def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result

    return checkDiagonals(board)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if len(actions(board)) == 0:
        return True
    return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    playerturn = player(board)
    if playerturn == 'X':
        value = -math.inf
        finalaction = None

        for action in actions(board):
            min_val = min_action(result(board, action))

            if min_val > value:
                value = min_val
                finalaction = action

        return finalaction

    if playerturn == 'O':
        value = math.inf
        finalaction = None

        for action in actions(board):
            max_val = max_action(result(board, action))

            if max_val < value:
                value = max_val
                finalaction = action
        return finalaction



def min_action(board):

    if terminal(board):
        return utility(board)

    max_value = math.inf
    for action in actions(board):
        max_value = min(max_value, max_action(result(board, action)))
    return max_value

def max_action(board):
    if terminal(board):
        return utility(board)

    min_value = -math.inf
    for action in actions(board):
        min_value = max(min_value, min_action(result(board, action)))
    return min_value