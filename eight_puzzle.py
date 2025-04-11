"""
Problem: Eight Puzzle (8-Puzzle)

Goal:
Rearrange the tiles in a 3x3 board to reach a specific goal configuration by sliding tiles
into the empty space (represented as 0).

Board Structure:
The board consists of 8 numbered tiles and one empty space.
Each move shifts a tile adjacent to the empty space into that space.

Initial State:
A given random configuration of the 3x3 grid with tiles 1-8 and one empty space.

Goal State (usually):
0 1 2
3 4 5
6 7 8  <- where 0 represents the blank space

Constraints:
- Only tiles adjacent (horizontally or vertically) to the blank space can be moved.
- Only one tile can be moved at a time.

Objective:
Find the shortest sequence of moves that transforms the initial configuration
into the goal configuration.
"""

from simpleai.search import (
    SearchProblem,
    astar
)


INITIAL_STATE = (
    (5,1,2),
    (3,4,0),
    (6,7,8)
)

GOAL = (
    (0,1,2),
    (3,4,5),
    (6,7,8)
)


def find_piece(state, piece) :
    for row_index, row in enumerate(state):
        for column_index, column in enumerate(row):
            if( state[row_index][column_index] == piece ): return (row_index, column_index)


class EightPuzzleProblem(SearchProblem):

    def cost(self, state, action, state2):
        return 1
    

    def is_goal(self, state):
        return state == GOAL
    

    def actions(self, state):
        zero_row, zero_col = find_piece(state, 0)
        available_actions = []
        possible_actions = (
            (zero_row + 1, zero_col),  # Up
            (zero_row - 1, zero_col),  # Down
            (zero_row, zero_col + 1),  # Right
            (zero_row, zero_col - 1)   # Left
        )

        for action in possible_actions:
            row, col = action[0], action[1]
            if (0 <= row <= 2) and (0 <= col <= 2):
                available_actions.append(state[row][col])

        return available_actions
    

    def result(self, state, action):
        zero_row, zero_col = find_piece(state, 0)
        piece_row, piece_col = find_piece(state, action)

        state = list(list(row) for row in state)

        state[zero_row][zero_col] = action
        state[piece_row][piece_col] = 0

        state = tuple(tuple(row) for row in state)

        return state
    

    def heuristic(self, state):
        total_distance = 0
        for piece in range(1, 9):
            row, col = find_piece(state, piece)
            goal_row, goal_col = find_piece(GOAL, piece)

            distance = abs(row - goal_row) + abs(col - goal_col)
            total_distance += distance

        return total_distance
    



result = astar(EightPuzzleProblem(INITIAL_STATE))

print(result.path())
print(result.cost)