import math
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any

class Pillar(object):
    """ x and y coordinates for each pillar object has its  (for its placement on the graph). """

    def __init__(self, x, y):  
        self.x = x
        self.y = y
        self.start = False
        self.dict = {}

    def set_reachable_node(self, p, possible_disks): 
        """ this function can be used to add a reachable pillar object p to the dictionary of nodes accesible to the main pillar object, 
        and the distance associated to reach it. """
        self.dict[p] = possible_disks

    def set_starting_disk(self, disk):
        self.starting_disk = disk

class Path(object):
    
    def __init__(self, starting_pillar):
        self.starting_pillar = starting_pillar
        self.cost = starting_pillar.starting_disk[1]
        self.pillars = [starting_pillar]

    def add_pillar(self, pillar, cost):
        self.pillars.append(pillar)
        self.cost += cost

def distance(p1,p2): 
    """ given two points, this function returns the (Pythogorean) distance between the two Pillar objects."""
    return math.sqrt(pow((p1.x - p2.x),2) + pow((p1.y - p2.y),2))

def possible_disks(dist, disks_pairs): 
    """ this function includes all the possible disc sizes that could be used to reach the distance required to the other pillar, 
    and in the end return the size of the cheapest disc."""

    possible_disks = []
    for disk in disks_pairs:
        if disk[2] >= dist: #compares if the combines distances of the discs at two pillars if sufficient (thus equal to or even greater as overlap is tolerated)
            possible_disks.append(disk)
    return sorted(possible_disks, key=lambda x: x[3]) #returns the possible discs in ascending order of costs
    
def reachable_pillars(p, pillars, threshold, disks_pairs): 
    """ given a starting pillar, it compares with every other pillar, and if the distance between them is less than 
    the biggest sized disc available(threshold), then its added as a reachable node to both """
    for p0 in pillars:
        dist = distance(p0, p)
        if dist <= threshold: #instead of using threshold can be directly using dist? I dont think so because we are using distance to see if they are reachable with the bigger disk
            p_p0_pairs = possible_disks(dist, disks_pairs)
            p0.set_reachable_node(p, p_p0_pairs)
            p.set_reachable_node(p0, p_p0_pairs)
    #return res #self note: instead of appending to res and returning, what if we dont append to it and return that

def cheaper_disk(disks, pillar):
    res = []
    for disk in disks:
        if disk[0] >= pillar.y:
            res.append(disk)
    return min(res, key = lambda t: t[1])

def create_adjacency_matrix(W, pillars, disks_pairs, max_r, disks): 
    """ this function creates the adjacency list by using dictionaries with each pillar object as key and its 
    values including a nested dictionary of the nodes accessible to it and the cost to access it. """
    start_index = 0
    starting_pillars = []
    for p in pillars:
        if p.y <= max_r:
            p.start = True
            p.set_starting_disk(cheaper_disk(disks, p))
            starting_pillars.append(p)

        start_index += 1   
        reachable_pillars(p, pillars[start_index:], 2*max_r, disks_pairs) #instead of using max_r can we not use dist bbetween the points as threshold directly
    return starting_pillars

def disks_combinations(disks):
    combinations = []
    for d in disks:
        for d1 in disks:
            combinations.append((d[0],d1[0],d[0]+d1[0],d[1]+d1[1])) #disc pairs = size of one disc, size of other disk, total size, total cost
    return combinations

def create_graph(W, pillars, disks): 
    """this function is used to create the graph of the canyo, in order to do that, for every pillar it will compute 
    the distance with the others pillars and for the reachable ones it will add the possible pairs of pillars to use 
    to reach that pillar with the reolated cost.
    It will also determine for each pillar if its a starting pillar or not.
    Args:
        W (Int): max y value on the canyon.
        pillars ([pillar]): pillars of the canyon
        disks ([(Int,Int)]): list of available disks, the tuple contains the radius and the cost respectively
    """
    
    disks = sorted(disks)
    max_r = disks[-1][0]
    disks_pairs = sorted(disks_combinations(disks), key=lambda x: x[2], reverse=True) #here x[2] is the total size of both discs
    starting_pillars = create_adjacency_matrix(W, pillars, disks_pairs, max_r, disks)#note: this functions returns two lists, not one, but i believe the second one is being ignored here
    for p in pillars:
        print(p.x,p.y)
        items = p.dict.items()
        print("nodes reachable from here: \n")
        for i in items:
            print(i[0].x,i[0].y,i[1]) 
            print("\n")
        print("\n")
    return starting_pillars

def read_input(): 
    """read the standard input and store pillars using pillar class, and then group them in a list, 
        save also the possible disks with their properties (radius, cost) in a list and store W value of the canyon.
    Returns:
        [type]: [description]
    """
    number_of_pillars,m_kind_of_disks,y_goal = list(map(int, input().split()))
    pillars = []
    disks = []
    for i in range(0, number_of_pillars):
        (x_i,y_i) = list(map(int, input().split()))
        pillars.append(Pillar(int(x_i),int(y_i)))

    for i in range(0, m_kind_of_disks):
        (r_i, c_i) = list(map(int, input().split()))
        disks.append((int(r_i),int(c_i)))

    return (y_goal, pillars, disks)

def search (starting_pillars, disks, pillars):

    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: Any=field(compare=False)

    paths_queue = PriorityQueue()
    for p in starting_pillars:
        path = Path(p)
        paths_queue.put(PrioritizedItem(path.cost, path))
    #now run dijkstra modified such that every time it checks if previous disk can be changed, if so checks 
    #for previous of that as well and so on.
    #from the path you add all the path with the cheapest connection we have from that disk to the others, and
    #for each new disk add new path in the queue with cost, once a solution is found, record results and cut out
    #branch that already have a lower cost.

def search_path(W, starting_pillars, disks, pillars):
    """search the least expensive path in the graph

    Args:
        W (Int): canyon goal
    """
    search(starting_pillars, disks, pillars)


def main():
    """main function of the project, read the input, prepare the canyon graph and search the graph
    """
    (W, pillars, disks) = read_input()
    starting_pillars = create_graph(W, pillars, disks)
    search_path(W, starting_pillars, disks, pillars)

if __name__ == "__main__":
    main()
