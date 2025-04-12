"""
Problem: N-Queens

Goal:
Place N queens on an N×N chessboard in such a way that no two queens threaten each other.

Rules:
- A queen can attack any piece in the same row, column, or diagonal.

Constraints:
- No two queens can share the same row, column, or diagonal.
- Exactly one queen must be placed in each row.
- The final arrangement must have all N queens placed with no conflicts.

Input:
An integer N representing the size of the board and the number of queens.

Objective:
Find one possible configurations where N queens can be safely placed on the board
according to the rules.
"""

from simpleai.search import (
    SearchProblem,
    limited_depth_first
)

BOARD_SIZE = 8
INITIAL_STATE = ()

def share_diagonals(queen_row, state):
    for col, row in enumerate(state):
        new_queen = (len(state), queen_row)
        current_queen = (col,row)
        if(abs(new_queen[0] - current_queen[0]) == abs(new_queen[1] - current_queen[1])): return True
                
    return False


class QueensProblem(SearchProblem):

    def cost(self, state, action, state2):
        return 1
    

    def result(self, state, action):
        state = list(state)
        state.append(action)
        state = tuple(state)
        return state
    

    def is_goal(self, state):
        return len(state) == BOARD_SIZE


    def actions(self, state):
        return [row for row in range(0,BOARD_SIZE) if row not in state and not share_diagonals(row, state)]



problem = QueensProblem(INITIAL_STATE)
result = limited_depth_first(problem, depth_limit=BOARD_SIZE)

print(result)
