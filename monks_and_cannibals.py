from simpleai.search import (
    SearchProblem,
    breadth_first,
    limited_depth_first,
)

# Estado => ( orilla_izq , orilla_der , post_bote)
INITIAL_STATE = ((0,0),(3,3),1) 
LEFT_SHORE = 0
RIGHT_SHORE = 1

# Orilla => (monjes, canibales)
MONK = 0
CANNIBAL = 1
BOAT = 2


def more_monks(shore):
    return shore[MONK] == 0 or shore[MONK] >= shore[CANNIBAL]


def readable_path(full_path):
    steps = []
    for _, step in full_path: # _, step ignora el primer elemento de la lista

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
            [1, 0, state[BOAT]], # 1 monje
            [2, 0, state[BOAT]], # 2 monjes
            [1, 1, state[BOAT]], # 1 monje y 1 canibal
            [0, 1, state[BOAT]], # 1 canibal
            [0, 2, state[BOAT]]  # 2 canibales
        ]
        available_moves = []
        
        for move in possible_moves:
            new_state = self.result(state, move)
            if(self.is_valid(new_state)):
                available_moves.append(move)
        
        return available_moves
    
    
    def is_valid(self, state):
        
        if( any(val < 0 for val in state[LEFT_SHORE]) ): # Comprueba si algun valor en la lista es negativo
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