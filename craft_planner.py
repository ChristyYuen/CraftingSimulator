import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    """
    if ('Consumes' in rule.keys()):
    	for temp in rule['Consumes']:
            consumes = [(temp, rule['Consumes'][temp])] # puts all the temps in list

    if ('Requires' in rule.keys()):
        for item in rule['Requires'].items():
            requires = [item]  # puts all the items in list
            """
    if 'Consumes' not in rule.keys():
        consumes = {}
    else:
        consumes = rule['Consumes']
    if 'Requires' not in rule.keys():
        requires = {}
    else:
        requires = rule['Requires']

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        for item, amt in consumes.items():
            if amt > state[item]:
                return False

        for item, amt in requires.items():
            if state[item] < 1:
                return False

        return True #otherwise true

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    if 'Consumes' not in rule.keys():
        consumes = {}
    else:
        consumes = rule['Consumes']
    if 'Produces' not in rule.keys():
        produces = {}
    else:
        produces = rule['Produces']

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        for con, amt in consumes.items():
            next_state[con] -= amt
        for pro, amt in produces.items():
            next_state[pro] += amt
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    requirements = goal

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for goal, amt in requirements.items():
            if state[goal] < amt:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state):
    # Implement your heuristic here!
    heuristic_value = 0
    # if current amount goal item < require 
    #     smth times diff

    # if 'Goal' < 'Required':
    #     heuristic_value = 

    if 'rail' in 'Goal' and state['rail'] < 21:
        return -1
    
    if (state['wood'] > 1 
    or state['bench'] > 1 
    or state['cart'] > 1
    or state['coal'] > 1   
    or state['cobble'] > 8 
    or state['furnace'] > 1
    or state['ingot'] > 6
    or state['iron_axe'] > 0
    or state['iron_pickaxe'] > 1
    or state['ore'] > 1
    or state['plank'] > 7 
    or state['rail'] > 16
    or state['stick'] > 5 
    or state['stone_axe'] > 0
    or state['stone_pickaxe'] > 1
    or state['wooden_axe'] > 0 
    or state['wooden_pickaxe'] > 1):
    	return 1000

    made_items = ["bench", "cart", "furnace", "iron_axe", "iron_pickaxe", "plank", "rail", "stone_axe", "stone_pickaxe", "wooden_axe", "wooden_pickaxe"]
    raw_materials = ["coal", "cobble", "ingot", "ore", "stick", "wood"]
    #lower number the better

    for things in made_items:
        if(state[things] > 1):
            return 1000
        if things in 'Requires':
            return 0
    
    for things in raw_materials:
        if things in 'Requires':
            return 10
        elif (state['wood'] > 1 
            or state['coal'] > 1   
            or state['cobble'] > 8 
            or state['ingot'] > 6
            or state['ore'] > 1
            or state['plank'] > 7 
            or state['stick'] > 5):
    	    return 1000

    for things in raw_materials:
        if things in 'Consumes':
            return 0
        elif (state['wood'] > 1 
            or state['coal'] > 1   
            or state['cobble'] > 8 
            or state['ingot'] > 6
            or state['ore'] > 1
            or state['plank'] > 7 
            or state['stick'] > 5):
    	    return 1000


    return heuristic_value

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state

    path = []
    heap = []
    first_node = (0, state)
    heap.append(first_node) #initial state
    came_from = dict()
    came_from[state] = None
    cost = dict()
    cost[state] = 0
    action = dict()
    action[state] = 'start'

    while time() - start_time < limit:
        heap.sort()
        curr = heap.pop(0)
        curr_state = curr[1]
        for node in graph(curr_state): #node[0]=name, node[1]=state, node[2]=action
            new_cost = node[2] + cost[curr_state]
            if node[1] not in came_from.keys():
                priority = new_cost + heuristic(node[1])
                heap.append((priority, node[1]))
                cost[node[1]] = new_cost
                came_from[node[1]] = curr[1]
                action[node[1]] = node[0]
                if is_goal(node[1]):
                    curr = node[1]
                    print("Plan: Goal Found")
                    print("Cost: " + str(cost[curr]))
                    #print("Remaining Time: " + str(limit- time()))
                    print("Computing Time: " + str(time()))#The amount of compute time the search process took
                    break
        else:
            continue
        break

    if type(curr) is not tuple:
        if is_goal(curr):
            length = 0
            while curr is not None:
                length+=1
                path.append((curr, action[curr]))
                curr = came_from[curr]
            #print(length-1)
            path.reverse()
            return path

    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t', state)
            print(action)
