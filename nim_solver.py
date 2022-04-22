import shelve
from pprint import pprint


WIN = True
LOSE = False

with shelve.open("memory") as memory:
    if 'normal' not in memory:
        memory['normal'] = {}
        memory['misere'] = {}

    normal_memory = memory["normal"]
    normal_memory[()] = LOSE
    misere_memory = memory["misere"]
    misere_memory[()] = WIN


def sorted_tuple(raw_state):
    new_state = list(filter(lambda left: True if left != 0 else False, raw_state))
    return tuple(sorted(new_state))


# Find all possible states reachable from a given state
def find_options(state):
    state = list(state)
    reachable = set()
    for i, left in enumerate(state):
        new_state = state.copy()
        for new_left in range(left - 1, -1, -1):
            new_state[i] = new_left
            reachable.add(sorted_tuple(new_state))
    return reachable


# Determines whether a game state is WIN or LOSE
def min_max(state, memory_table):
    if state in memory_table:
        return memory_table[state]

    options_set = set()
    for option in find_options(state):
        options_set.add(min_max(option, memory_table))

    if LOSE not in options_set:
        memory_table[state] = LOSE
        return LOSE
    else:
        memory_table[state] = WIN
        return WIN


# print(min_max(tuple(7 for i in range(5)), normal_memory))

with shelve.open("memory") as memory:
    memory["normal"] = normal_memory
    memory["misere"] = misere_memory
