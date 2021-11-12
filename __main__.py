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
        self.reach_end = False
        self.dict = {}
        self.visited = False
        self.disk = [(0,0)]

    def set_reachable_node(self, p, possible_disks): 
        """ this function can be used to add a reachable pillar object p to the dictionary of nodes accesible to the main pillar object, 
        and the distance associated to reach it. """
        self.dict[p] = (possible_disks)

    def set_starting_disk(self, disk):#CHANGE NAME TO SET_DISK
        self.disk[0] = disk
        self.cost = self.disk[0][1]
        self.visited = True

    def set_path_cost(self, cost):
        self.cost_path = cost

    def set_end_disk(self, end_disk):
        self.end_disk = end_disk
        self.reach_end = True

    def get_disks(self, pillar):
        return self.dict.get(pillar)

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

def disk_to_the_end(disks, y, W):
    for d in disks:
        if d[0] + y >= W:
            return d

def create_adjacency_matrix(W, pillars, disks_pairs, max_r, disks): 
    """ this function creates the adjacency list by using dictionaries with each pillar object as key and its 
    values including a nested dictionary of the nodes accessible to it and the cost to access it. """
    start_index = 0
    starting_pillars = []
    finish = False
    for p in pillars:
        if p.y <= max_r:
            p.set_starting_disk(cheaper_disk(disks, p))
            p.set_path_cost(p.disk[0][1])
            starting_pillars.append(p)
        if p.y + max_r >= W:
            p.set_end_disk(disk_to_the_end(disks, p.y, W))
            finish = True
        start_index += 1   
        reachable_pillars(p, pillars[start_index:], 2*max_r, disks_pairs) #instead of using max_r can we not use dist bbetween the points as threshold directly
    if not finish:
        print('impossible')
        return []
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
    disks = sorted(disks, key = lambda x: x[1])
    disks_pairs = sorted(disks_combinations(disks), key=lambda x: x[3]) #here x[2] is the total size of both discs
    starting_pillars = create_adjacency_matrix(W, pillars, disks_pairs, max_r, disks)#note: this functions returns two lists, not one, but i believe the second one is being ignored here
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

def take_cheapest_disks(disks_pairs, disk_size):
    for i in  range(0, len(disks_pairs)):
        if disks_pairs[i][1] >= disk_size:
            if disks_pairs[i][0] == disk_size and disks_pairs[i][1] != disk_size:
                if i < len(disks_pairs)-1:
                    return disks_pairs[i+1]
            else:
                return disks_pairs[i]
    return disks_pairs[0]

def search (starting_pillars, W):

    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: Any=field(compare=False)
    
    paths_queue = PriorityQueue()
    for p in starting_pillars:
        paths_queue.put(PrioritizedItem(p.cost, p))
    final_value = 100000000000000000000
    while(not paths_queue.empty()):
        now_pillar = paths_queue.get().item
        if now_pillar.reach_end:
            value = now_pillar.cost_path - now_pillar.cost + now_pillar.end_disk[1]
            if value < final_value:
                final_value = value
        for adjacent_pillar in now_pillar.dict.items():
            #print("pillars: ")
            #print(now_pillar.x, now_pillar.y)
            #print(adjacent_pillar[0].x, adjacent_pillar[0].y)
            #print("costs: ")
            new_disks = take_cheapest_disks(adjacent_pillar[0].dict[now_pillar], now_pillar.disk[0][0])
            new_cost = now_pillar.cost_path + new_disks[3] - now_pillar.cost #+ (now_pillar.dict[adjacent_pillar[0]][0][4] - now_pillar.disk[0][1]) #wrong, first check for our disk size. maybe we can use dictionary to access cheaper disk given the size
            #print("now pillar path cost: ",now_pillar.cost_path,"new cost: " ,new_cost, "new disk cost: ",new_disks[3], "now pillar cost: ",now_pillar.cost)
            #print("new disk: ",new_disks, "\n", now_pillar.disk)
            #print("\n")
            if new_cost < final_value:
                if adjacent_pillar[0].visited:
                    if new_cost < adjacent_pillar[0].cost_path:
                        adjacent_pillar[0].set_starting_disk((new_disks[0], new_disks[4]))#something wrong here
                        adjacent_pillar[0].set_path_cost(new_cost)
                        paths_queue.put(PrioritizedItem(new_cost, adjacent_pillar[0]))
                else:
                    adjacent_pillar[0].set_starting_disk((new_disks[0], new_disks[4]))
                    adjacent_pillar[0].set_path_cost(new_cost)
                    paths_queue.put(PrioritizedItem(new_cost, adjacent_pillar[0]))
    print(final_value)

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
