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
        self.visited = False

    def set_reachable_node(self, p, possible_disks): 
        """ this function can be used to add a reachable pillar object p to the dictionary of nodes accesible to the main pillar object, 
        and the distance associated to reach it. """
        self.dict[p] = possible_disks

    def set_starting_disk(self, disk):#CHANGE NAME TO SET_DISK
        self.disk = [disk]
        self.cost = self.disk[0][1]

    def set_path_cost(self, cost):
        self.cost_path = cost
"""
class Path(object):
    
    def __init__(self, pillars):
        #self.starting_pillar = starting_pillar
        self.cost = pillars[-1].cost
        self.pillars = pillars

    def get_pillars(self):
        return self.pillars
"""


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
            #CHANGE: FOR LOOP
            p0_p_pairs =  []
            for pair in p_p0_pairs:
                p0_p_pairs.append((pair[1], pair[0], pair[2], pair[3], pair[5], pair[4]))
            p0.set_reachable_node(p, p_p0_pairs)
            p.set_reachable_node(p0,  p0_p_pairs)
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
            p.set_path_cost(p.disk[0][1])
            p.visited = True
            starting_pillars.append(p)

        start_index += 1   
        reachable_pillars(p, pillars[start_index:], 2*max_r, disks_pairs) #instead of using max_r can we not use dist bbetween the points as threshold directly
    return starting_pillars

def disks_combinations(disks):
    combinations = []
    for d in disks:
        for d1 in disks:
            combinations.append((d[0],d1[0],d[0]+d1[0],d[1]+d1[1],d[1],d1[1])) #disc pairs = size of one disc, size of other disk, total size, total cost
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
    """ 
    for p in pillars:
        print(p.x,p.y)
        items = p.dict.items()
        print("nodes reachable from here: \n")
        for i in items:
            print(i[0].x,i[0].y,i[1]) 
            print("\n")
        print("\n")
    """
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

def take_cheapest_disk():
    return

def search (starting_pillars, W):

    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: Any=field(compare=False)
    
    paths_queue = PriorityQueue()
    for p in starting_pillars:
        paths_queue.put(PrioritizedItem(p.cost, p))

    final_value = 1000000000
    while(not paths_queue.empty()):
        now_pillar = paths_queue.get().item
        for adjacent_pillar in now_pillar.dict.items():
            #print("pillar: " ,now_pillar.x, now_pillar.y)
            #print("adjacent pillar: ", adjacent_pillar[0].x, adjacent_pillar[0].y)
            #print(now_pillar.dict[adjacent_pillar[0]][0][4])
            new_cost = now_pillar.cost_path + adjacent_pillar[0].dict[now_pillar][0][4] + (now_pillar.dict[adjacent_pillar[0]][0][4] - now_pillar.disk[0][1]) #wrong, first check for our disk size. maybe we can use dictionary to access cheaper disk given the size
            #print("new path cost: ", new_cost)
            if adjacent_pillar[0].visited:
                if new_cost < adjacent_pillar[0].cost_path:
                    print("pillar: " ,now_pillar.x, now_pillar.y)
                    print("adjacent pillar: ", adjacent_pillar[0].x, adjacent_pillar[0].y)
                    print("changing cost: ",new_cost, adjacent_pillar[0].cost_path)
                    adjacent_pillar[0].set_starting_disk((adjacent_pillar[0].dict[now_pillar][0][0] , adjacent_pillar[0].dict[now_pillar][0][4]))#something wrong here
                    adjacent_pillar[0].set_path_cost(new_cost)
                    paths_queue.put(PrioritizedItem(new_cost, adjacent_pillar[0]))
            else:
                adjacent_pillar[0].visited = True
                adjacent_pillar[0].set_starting_disk((adjacent_pillar[0].dict[now_pillar][0][0] , adjacent_pillar[0].dict[now_pillar][0][4]))
                adjacent_pillar[0].set_path_cost(new_cost)
                paths_queue.put(PrioritizedItem(new_cost, adjacent_pillar[0]))

        if adjacent_pillar[0].y + adjacent_pillar[0].disk[0][0] >= W:
            if adjacent_pillar[0].cost_path < final_value:
                final_value = adjacent_pillar[0].cost_path
    print(final_value)
    """
    path = paths_queue.get()
    dijkstra_pillars = path.item.pillars[-1].dict.items()
    for reachable_pillar in dijkstra_pillars:
        print(path.item.pillars)
        new_size = 0
        index = 0
        print("pillar: ",path.item.pillars[-1].x ,path.item.pillars[-1].y)
        print("pillar size: ",path.item.pillars[-1].disk[0][0])
        while (path.item.pillars[-1].disk[0][0] > new_size): #size
            
            new_size = reachable_pillar[1][index][1]
            #print("pillar size: ",path.item.pillars[-1].disk[0][0])
            print("new pillar: ",reachable_pillar[1][index])
            print("new pillar size: ",reachable_pillar[1][index][1])
            index += 1
        index -= 1
        
        print(reachable_pillar[0].x, reachable_pillar[0].y, reachable_pillar[0].visited, reachable_pillar[1][index][5], reachable_pillar[1][index][4])
        new_cost = path.item.cost + reachable_pillar[1][index][5] + (reachable_pillar[1][index][4] - path.item.pillars[-1].cost) #wrong, first check for our disk size. maybe we can use dictionary to access cheaper disk given the size
        if reachable_pillar[0].visited:
            if reachable_pillar[0].cost > new_cost:
                path.item.pillars.append(reachable_pillar[0])
                new_path = Path(path)
                reachable_pillar[0].set_starting_disk((reachable_pillar[1][0][2] ,reachable_pillar[1][0][5]))
                paths_queue.put(PrioritizedItem(new_cost, new_path))
        else:
            reachable_pillar[0].visited = True
            reachable_pillar[0].set_starting_disk((reachable_pillar[1][index][2] ,reachable_pillar[1][index][5]))
            path.item.pillars.append(reachable_pillar[0])
            print("path: ",path.item.pillars)
            new_path = Path(path)
            paths_queue.put(PrioritizedItem(new_cost, new_path))
    """
    

    #now run dijkstra modified such that every time it checks if previous disk can be changed, if so checks 
    #for previous of that as well and so on.
    #from the path you add all the path with the cheapest connection we have from that disk to the others, and
    #for each new disk add new path in the queue with cost, once a solution is found, record results and cut out
    #branch that already have a lower cost.
    #for every node keep track of max cost until now so that we can prune branches.

def search_path(W, starting_pillars):
    """search the least expensive path in the graph

    Args:
        W (Int): canyon goal
    """
    search(starting_pillars, W)


def main():
    """main function of the project, read the input, prepare the canyon graph and search the graph
    """
    (W, pillars, disks) = read_input()
    starting_pillars = create_graph(W, pillars, disks)
    search_path(W, starting_pillars)

if __name__ == "__main__":
    main()
