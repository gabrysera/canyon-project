import math
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any, final

import time 
#documentation
#testing
class Pillar(object):
    """ x and y coordinates for each pillar object has its  (for its placement on the graph). """


    def __init__(self, x, y, disk):  
        self.x = x #x coordinate
        self.y = y #y coordinate
        self.start = False #is it the start node?
        self.reach_end = False 
        self.dict = {} #with pillars that can be reached as keys and the values being the distance to them
        self.visited = False 
        self.disk = disk 
        self.previous_pillar = None
        self.path_cost = disk[1] #cost of the disk assigned to it

    def visit(self):
        self.visited = True

    def set_disk(self, disk):
        self.disk[0] = disk
        self.cost = self.disk[0][1]
        self.visited = True

    def set_path_cost(self, cost):
        self.path_cost = cost

    def set_end_disk(self, end_disk):
        self.end_disk = end_disk
        self.reach_end = True


def read_input(): 
    
    """read the standard input and store pillars using pillar class, and then group them in a list, 
        save also the possible disks with their properties (radius, cost) in a list and store W value of the canyon.
    Returns:
        [type]: [description]
    """
    number_of_pillars,m_kind_of_disks,y_goal = list(map(int, input().split())) #y_goal is the width
    pillars_positions = []
    disks = []
    for i in range(0, number_of_pillars):
        (x_i,y_i) = list(map(int, input().split()))
        pillars_positions.append(((int(x_i),int(y_i)))) #pillars_position is a list of tuples containing the coordinates of each tuple

    for i in range(0, m_kind_of_disks):
        valid = True
        (r_i, c_i) = list(map(int, input().split()))
        #if new r_i is smaller than already existing r_j then c_i has to be smaller otherwise this disk is not appended
        for d in disks:
            if int(r_i) < d[0]:
                if int(c_i) >= d[1]: #self note: do we need input validation here?
                    valid = False
            if int(r_i) > d[0]:
                if int(c_i) <= d[1]:
                    disks.remove(d)
        #also checks for later disks
        if valid:
            disks.append((int(r_i),int(c_i))) #disks is a list that contains the radius of the disk and its respective 
                                                    #cost in a tuple for each different type of disc

    return (y_goal, pillars_positions, disks) 

def create_adjacency_matrix(W, pillars_positions, max_r, disks): 
    """ this function creates the adjacency list by using dictionaries with each pillar object as key and its 
    values including a nested dictionary of the nodes accessible to it and the cost to access it. """
    starting_pillars = []
    for p in pillars_positions:
        if p[1] <= max_r: #a pillar is a possible starting point only if the y coordinate of the pillar is <= to the biggest 
                                                              
                                                                                            #radius disc available
            #take all the disks that p[1] can use to reach 0 and create a pillar for each disk.
            for d in disks:
                if p[1] <= d[0]:
                    starting_pillars.append(Pillar(p[0],p[1],d))
                else:
                    break #self note: no need to continue any further?(because the discs are only going to get bigger)
        #if p.y + max_r >= W:
            #take all the disks that p[1] can use to reach W and create a pillar for each disk.
        #    p.set_end_disk(disk_to_the_end(disks, p.y, W))
    return starting_pillars

def create_graph(W, pillars_positions, disks): 
    """this function is used to create the graph of the canyo, in order to do that, for every pillar it will compute 
    the distance with the others pillars and for the reachable ones it will add the possible pairs of pillars to use 
    to reach that pillar with the reolated cost.
    It will also determine for each pillar if its a starting pillar or not.
    Args:
        W (Int): max y value on the canyon.
        pillars ([pillar]): pillars of the canyon
        disks ([(Int,Int)]): list of available disks, the tuple contains the radius and the cost respectively
    """
    
    
    max_r = disks[0][0]
    starting_pillars = create_adjacency_matrix(W, pillars_positions ,max_r, disks)#note: this functions returns two lists, not one, but i believe the second one is being ignored here
    #disks = sorted(disks, key = lambda x: x[1])
    return starting_pillars

def distance(x1, y1, x2, y2): 
    """ given two points, this function returns the (Pythogorean) distance between the two Pillar objects."""
    return math.sqrt(pow((x1 - x2),2) + pow((y1 - y2),2))

def find_neighbour_pillars(pillar, pillars_positions, disks ,dict):
    neighbour = []
    for pill in pillars_positions:
        for d in disks:
            if distance(pillar.x, pillar.y, pill[0], pill[1]) <= pillar.disk[0] + d[0] and distance != 0.0: #self note: im not sure what distance is doing here
                if (pill[0], pill[1], d[0]) not in dict:
                    new_pillar = Pillar(pill[0], pill[1], d)
                    neighbour.append(new_pillar)
                    dict[(pill[0], pill[1], d[0])] = new_pillar #the dict stores the neighbour pillars for each given pillars and the disc size required to reach them as key, and the neighbour pillar object as value
                    dict[(pill[0], pill[1], d[0])].path_cost = pillar.path_cost + d[1] #self note: thus directly accessing members makes the set_path function obsolute i assume?
                elif dict[(pill[0], pill[1], d[0])].path_cost > pillar.path_cost + d[1]: #if the neighbouring pillar is already present, it checks if a smaller disc size is found that can also reach this neighbour, then update the cost of neighbour pillar to a new lower cost 
                    neighbour.append(Pillar(pill[0], pill[1], d))
                    dict[(pill[0], pill[1], d[0])].path_cost = pillar.path_cost + d[1] 
            else:
                break
    return neighbour


def search_path(W, starting_pillars, pillars_positions, disks):

    @dataclass(order=True)
    class PrioritizedItem:
        priority: int
        item: Any=field(compare=False)

    dict ={} #this dict will later contain the neighbouring pillars for a given pillar
    paths_queue = PriorityQueue()
    for p in starting_pillars:
        paths_queue.put(PrioritizedItem(p.disk[1], p)) #//puts the cost of 
        dict[(p.x,p.y,p.disk[0])] = p #adding the starting pillars coordinates and sice of disc to dict
    already_found = False
    final_value = 0
    while(not paths_queue.empty()):
        now_pillar = paths_queue.get()
        if now_pillar.item.y + now_pillar.item.disk[0] >= W: #if the y coordinate of pillar + the disc size reach the other side of canyon
            if already_found:
                if now_pillar.item.path_cost < final_value:
                    if now_pillar.item.path_cost < final_value: #self note: extra line?
                        final_value = now_pillar.item.path_cost
            else:
                final_value = now_pillar.item.path_cost
                already_found = True #self note: function of already_found?
        if now_pillar.priority == now_pillar.item.path_cost: #self note: would just else work here?
            adjacency_pillars = find_neighbour_pillars(now_pillar.item, pillars_positions, disks ,dict)
            for new_pillar in adjacency_pillars:
                if already_found:
                    if new_pillar.path_cost < final_value:
                        paths_queue.put(PrioritizedItem(new_pillar.path_cost, new_pillar)) 
                else:
                    paths_queue.put(PrioritizedItem(new_pillar.path_cost, new_pillar))

    if final_value==0:
        print("impossible")
    else:
        print(final_value)


def main():
    """main function of the project, read the input, prepare the canyon graph and search the graph
    """
    t = time.time()
    (W, pillars_positions, disks) = read_input()
    disks = sorted(disks, reverse = True)
    starting_pillars = create_graph(W, pillars_positions, disks)
    search_path(W, starting_pillars, pillars_positions, disks)
    # print(time.time() - t)

if __name__ == "__main__":
    main()
