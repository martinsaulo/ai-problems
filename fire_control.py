"""
Problem: Fire Control

Goal:
Extinguish the fire in all rooms of the house.

Rules:
- Moving from one room to another takes 5 seconds.
- Each room on fire has flames of varying intensity levels, affecting how long it takes to extinguish:
  - Level 1 flames require 10 seconds of water spray.
  - Level 2 flames require 30 seconds of water spray.
  - Level 3 flames require 600 seconds of water spray.

Constraints:
- There is only one firefighter and he always starts at the entrance hall.
- The firefighter can move from one room to another if they are directly connected.

Objective:
Find the optimal sequence of movements and spraying actions to extinguish all fires as quickly as possible.
"""

from simpleai.search import (
    SearchProblem,
    astar
)

HALL = -1
LIVING = 0
BATHROOM = 1
BEDROOM = 2
KITCHEN = 3
ACTUAL_POS = 4
ADJACENT_ROOMS = {
    LIVING : [KITCHEN, BEDROOM],
    BATHROOM : [BEDROOM, KITCHEN],
    BEDROOM : [LIVING, BATHROOM],
    KITCHEN : [LIVING, BATHROOM],
}

INITIAL_STATE = (10, 30, 600, 600, HALL)

class FireControl(SearchProblem):
    
    def is_goal(self, state):
        return sum(state[:-1]) == 0 # Add all values except ACTUAL_POS

    
    def cost(self, state, action, state2):
        if(action[0] == "Move"):
            return 5
        
        return state[state[ACTUAL_POS]]
    

    def actions(self, state):
        if(state[ACTUAL_POS] == HALL):
            return [("Move", LIVING)]
        
        available_moves = []
        actual_pos = state[ACTUAL_POS]

        if(state[actual_pos] != 0):
            available_moves.append(("Spray", actual_pos))

        available_moves += [("Move", room) for room in ADJACENT_ROOMS.get(actual_pos)]

        return available_moves
    

    def result(self, state, action):
        state = list(state)

        if(action[0] == "Move"):
            state[ACTUAL_POS] = action[1]
        else:
            state[action[1]] = 0

        state = tuple(state)
        return state
    

    def heuristic(self, state):
        return sum(state)



problem = FireControl(INITIAL_STATE)

result = astar(problem)

print(result.path())
print(result.cost)