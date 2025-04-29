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

Objective:
Find one possible configurations where N queens can be safely placed on the board
according to the rules.
"""

from simpleai.search import (
    SearchProblem,
    hill_climbing_random_restarts
)
from random import (
    randint
)

BOARD_SIZE = 16


def queens_attacks(queen_pos, state):
    queen_col, queen_row = queen_pos
    attacks = 0
    
    for current_col in range(queen_col + 1, BOARD_SIZE):
        current_row = state[current_col]
        if(current_row == queen_row): 
            attacks += 2

        if( abs(current_row - queen_row) == abs(current_col - queen_col) ):
            attacks += 2

    return attacks


class QueensProblem(SearchProblem):

    def generate_random_state(self):
        state = [randint(0, BOARD_SIZE - 1) for row in range(BOARD_SIZE)]
        return tuple(state)
    

    def value(self, state):
        total_attacks = 0

        for queen_col, queen_row in enumerate(state):
            total_attacks += queens_attacks( (queen_col, queen_row), state)

        return -total_attacks
    

    def actions(self, state):
        available_actions = []

        for _, queen_col in enumerate(state):
            for queen_row in range(BOARD_SIZE):
                if (queen_row != state[queen_col]):
                    available_actions.append( (queen_col, queen_row) )

        return available_actions
    

    def result(self, state, action):
        state = list(state)
        state[action[0]] = action[1]
        state = tuple(state)
        return state
    

problem = QueensProblem(None)

result = hill_climbing_random_restarts(problem, restarts_limit=32)

print(result.value)
print(result)