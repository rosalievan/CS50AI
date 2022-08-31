"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

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
    flat_board = [item for sublist in board for item in sublist]

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
    actions = set()
    for i in range(3):
        for j in range(3):
            action = (i,j)
            if  board[i][j] == EMPTY:
                actions.add(action)
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception ('not a valid action')
    boardcopy = copy.deepcopy(board)
    boardcopy[action[0]][action[1]] = player(board)
    return boardcopy


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

# def winner(board):
#     """
#     Returns the winner of the game, if there is one.
#     """
#     for i in range(3):
#         if len(set(board[i])) == 1:
#             return board[i][0]
#         transposed_board = np.transpose(board)
#         print(transposed_board)
#         if len(set(transposed_board[i])) == 1:
#             return board[i][0]
    
#     if len(set([r[i] for i, r in enumerate(board)])) == 1:
#         return board[1][1]
    
#     if len(set([r[-i-1] for i, r in enumerate(board)])) == 1:
#         return board [1][1]
    
#     return None    
    


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
    if winner(board) == 'O':
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == 'X':
        final_action = None
        value = -math.inf
        for action in actions(board):
            result_value = min_value(result(board, action))
            if result_value > value:
                final_action = action
                value = result_value

        return final_action

    if player(board) == 'O':
        final_action = None
        value = math.inf
        for action in actions(board):
            result_value = max_value(result(board, action))
            if result_value < value:
                final_action = action
                value = result_value
        return final_action



def max_value(board):
    value = -math.inf
    if terminal(board):
        return utility(board)

    if actions(board):
        for action in actions(board):
            value = max(value, min_value(result(board, action)))
    
    return value

def min_value(board):
    value = math.inf
    if terminal(board):
        return utility(board)

    if actions(board):
        for action in actions(board):
            value = min(value, max_value(result(board, action)))

    return value
    
