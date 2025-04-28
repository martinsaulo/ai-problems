"""
Problem: Backpack Problem

Goal:
Select a subset of items to transport in a backpack in order to maximize the total monetary value without exceeding the backpack's weight capacity.

Context:
You are given a backpack with a limited weight capacity (expressed in kilograms) and a list of items.
Each item has an associated weight and monetary value.

Constraints:
- The total weight of the selected items must not exceed the backpack's capacity.
- Each item can be included only once.

Objective:
Determine which combination of items can be transported to maximize the total value while respecting the weight limit.
"""

from simpleai.search import (
    SearchProblem,
    hill_climbing_random_restarts
)
from random import (
    randint
)

OBJECTS = {     # Object = [Name, Weight, Value]
    "Pencil" : (1, 15),
    "Laptop" : (5, 1500),
    "Headphones" : (1, 200),
    "Notebook" : (2, 300),
    "Water Bottle" :(1, 25),
    "Camera" : (2, 800),
    "Jacket" : (3, 400),
    "Smartphone" : (2, 1000),
    "Tablet" : (2, 600),
    "Book" : (2, 100),
    "Sneakers" : (2, 250),
    "Watch" : (2, 500),
    "Sunglasses" : (1, 150),
}
MAX_WEIGHT = 10
NAME = 0
WEIGHT = 1
VALUE = 2


def cast(objects_list):
    return [[key, value[0], value[1]] for key, value in objects_list.items()]


def available_objects(state):
    objects = OBJECTS.copy()
    for object in state:
        objects.pop(object[NAME])
    
    return cast(objects)


class BackpackProblem(SearchProblem):

    def value(self, state):
        object_values = [object[VALUE] for object in state]
        return sum(object_values)
    

    def generate_random_state(self):
        state = []
        objects = cast(OBJECTS)
        total_weight = 0
        while (len(objects) > 0):
            rand_item_index = randint(0, len(objects) - 1)
            rand_item = objects[rand_item_index]

            if( total_weight + rand_item[WEIGHT] <= MAX_WEIGHT):
                state.append(rand_item)
                total_weight += rand_item[WEIGHT]

            objects.pop(rand_item_index)

        return tuple(state)
    

    def actions(self, state):
        objects = available_objects(state)
        total_weight = sum( [object[WEIGHT] for object in state] )
        available_actions = [("Add", object) for object in objects if object[WEIGHT] + total_weight <= MAX_WEIGHT]
        available_actions += [("Remove", object) for object in state]

        return available_actions


    def result(self, state, action):
        state = list(state)

        if(action[0] == "Add"):
            state.append(action[1])
        elif(action[0] == "Remove"):
            state.remove(action[1])

        state = tuple(state)
        return state
    


problem = BackpackProblem(None)

result = hill_climbing_random_restarts(problem, restarts_limit=999)

print(result.value)
print(result)
