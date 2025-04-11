"""
Problem: Monks and Cannibals

Goal:
Safely transport 3 monks and 3 cannibals from the right shore of a river to the left shore
using a boat that can carry at most 2 people at a time.

Constraints:
- The boat cannot cross the river by itself; it needs at least one person to operate.
- At any moment (on either shore), if the number of cannibals exceeds the number of monks,
  the monks will be eaten. Thus, this configuration is invalid.
- Only two people can travel in the boat at the same time (either 1 or 2).
- The boat can travel back and forth between the shores.

Initial State:
All 3 monks and 3 cannibals are on the right shore, and the boat is also on the right shore.

Objective:
Find a sequence of valid moves that brings all monks and cannibals to the left shore
without violating any of the constraints.
"""

from simpleai.search import (
    SearchProblem,
    breadth_first,
    limited_depth_first,
)

# State => ( left_shote , right_pos , boat_pos)
INITIAL_STATE = ((0,0),(3,3),1) 
LEFT_SHORE = 0
RIGHT_SHORE = 1

# Shore => (monk, cannibal)
MONK = 0
CANNIBAL = 1
BOAT = 2


def more_monks(shore):
    return shore[MONK] == 0 or shore[MONK] >= shore[CANNIBAL]


def readable_path(full_path):
    steps = []
    for _, step in full_path:

        direction = "<--" if step[BOAT] == LEFT_SHORE else "-->"
        left_shore =  ( "M" * step[LEFT_SHORE][MONK] ) + ( "C" * step[LEFT_SHORE][CANNIBAL] )
        right_shote = ( "M" * step[RIGHT_SHORE][MONK] ) + ( "C" * step[RIGHT_SHORE][CANNIBAL] )
        
        steps.append([direction, left_shore, right_shote])
    
    return steps
    


class MonksAndCannibals(SearchProblem):
    def cost(self, state, action, state2):
        return 1
    
    
    def is_goal(self, state):
        return state[LEFT_SHORE] == (3,3)
    
    
    def actions(self, state):
        possible_moves = [
            [1, 0, state[BOAT]], # 1 monk
            [2, 0, state[BOAT]], # 2 monks
            [1, 1, state[BOAT]], # 1 monk y 1 cannibal
            [0, 1, state[BOAT]], # 1 cannibal
            [0, 2, state[BOAT]]  # 2 cannibals
        ]
        available_moves = []
        
        for move in possible_moves:
            new_state = self.result(state, move)
            if(self.is_valid(new_state)):
                available_moves.append(move)
        
        return available_moves
    
    
    def is_valid(self, state):
        
        if( any(val < 0 for val in state[LEFT_SHORE]) ):
            return False

        if( any(val < 0 for val in state[RIGHT_SHORE]) ):
            return False
        
        return (more_monks(state[LEFT_SHORE]) and more_monks(state[RIGHT_SHORE]))
    
    
    def result(seft, state, action):
        state = [list(state[LEFT_SHORE]), list(state[RIGHT_SHORE]), state[BOAT]]
        boat_pos = state[BOAT]
        other_side = 1 - state[BOAT]
        
        state[other_side][MONK] += action[MONK]
        state[other_side][CANNIBAL] += action[CANNIBAL]
        state[boat_pos][MONK] -= action[MONK]
        state[boat_pos][CANNIBAL] -= action[CANNIBAL]
        state[BOAT] = other_side
        
        state = (tuple(state[LEFT_SHORE]), tuple(state[RIGHT_SHORE]), state[BOAT])
        return state
    


problem = MonksAndCannibals(INITIAL_STATE)

result = breadth_first(problem, graph_search=True)
#result = limited_depth_first(problem, depth_limit=11)

full_path = result.path()
print(readable_path(full_path))
print(result.cost)