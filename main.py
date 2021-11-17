import math
from queue import PriorityQueue


import time 

class Pillar(object):
    """ x and y coordinates for each pillar object has its  (for its placement on the graph). """

    def __init__(self, x, y, disk):  
        self.x = x
        self.y = y
        self.start = False
        self.visited = False
        self.disk = disk 
        self.path_cost = disk[1]

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def set_disk(self, disk):#CHANGE NAME TO SET_DISK
        self.disk[0] = disk
        self.cost = self.disk[0][1]
        self.visited = True

    def set_path_cost(self, cost):
        self.path_cost = cost


def read_input(): 
    """read the standard input and store pillars using pillar class, and then group them in a list, 
        save also the possible disks with their properties (radius, cost) in a list and store W value of the canyon.
    Returns:
        [type]: [description]
    """
    number_of_pillars,m_kind_of_disks,y_goal = list(map(int, input().split()))
    pillars_positions = []
    disks = []
    for i in range(0, number_of_pillars):
        (x_i,y_i) = list(map(int, input().split()))
        pillars_positions.append(((int(x_i),int(y_i))))

    for i in range(0, m_kind_of_disks):
        valid = True
        (r_i, c_i) = list(map(int, input().split()))
        #if new r_i is smaller than already existing r_j then c_i has to be smaller otherwise this disk is not appended
        for d in disks:
            if int(r_i) < d[0]:
                if int(c_i) >= d[1]:
                    valid = False
            if int(r_i) > d[0]:
                if int(c_i) <= d[1]:
                    disks.remove(d)
        #also checks for later disks
        if valid:
            disks.append((int(r_i),int(c_i)))
        #disks.append((int(r_i),int(c_i)))

    return (y_goal, pillars_positions, disks)

def create_adjacency_matrix(W, pillars_positions, max_r, disks): 
    """ this function creates the adjacency list by using dictionaries with each pillar object as key and its 
    values including a nested dictionary of the nodes accessible to it and the cost to access it. """
    starting_pillars = []
    for p in pillars_positions:
        if p[1] <= max_r:
            #take all the disks that p[1] can use to reach 0 and create a pillar for each disk.
            for d in disks:
                if p[1] <= d[0]:
                    starting_pillars.append(Pillar(p[0],p[1],d))
                else:
                    break
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
    max_r = disks[0][0]
    for pill in pillars_positions:
        if pill[0] >= pillar.x - max_r*2:
            if pill[0] <= pillar.x + max_r*2:
                for d in disks:
                    #check if also other pillars reach the new neighbour with this disk, if so , add only if path_cost is cheaper
                    #to check for the other pillars we need another for loop for the disks, and then if disk in in dict, then check 
                    #if distance holds, if so, if the other pillar path_cost is cheaper then do not add the current one to new neighbours.
                    
                    dist = distance(pillar.x, pillar.y, pill[0], pill[1])
                    
                    if dist <= pillar.disk[0] + d[0] and dist != 0.0:
                        if (pill[0], pill[1], d[0]) not in dict:
                            new_pillar = Pillar(pill[0], pill[1], (d[0], pillar.path_cost + d[1]))
                            neighbour.append(new_pillar)
                            dict[(pill[0], pill[1], d[0])] = new_pillar
                            #dict[(pill[0], pill[1], d[0])].path_cost = pillar.path_cost + d[1]
                        elif dict[(pill[0], pill[1], d[0])].path_cost > pillar.path_cost + d[1]:
                            neighbour.append(Pillar(pill[0], pill[1], (d[0], pillar.path_cost + d[1])))
                            #dict[(pill[0], pill[1], d[0])].path_cost = pillar.path_cost + d[1]
                    else:
                        break
            else:
                break
    return neighbour


def search_path(W, starting_pillars, pillars_positions, disks):

    dict ={}
    paths_queue = PriorityQueue()
    for p in starting_pillars:
        paths_queue.put((p.disk[1], p))
        dict[(p.x,p.y,p.disk[0])] = p 
    already_found = False
    final_value = 0
    while(not paths_queue.empty()):
        now_pillar = paths_queue.get()
        
        if now_pillar[1].y + now_pillar[1].disk[0] >= W:
            if already_found:
                if now_pillar[1].path_cost < final_value:
                    if now_pillar[1].path_cost < final_value:
                        final_value = now_pillar[1].path_cost
            else:
                final_value = now_pillar[1].path_cost
                already_found = True
        #if now_pillar[0] == now_pillar[1].path_cost:
        adjacency_pillars = find_neighbour_pillars(now_pillar[1], pillars_positions, disks ,dict)
        for new_pillar in adjacency_pillars:
            if already_found:
                if new_pillar.path_cost < final_value:
                    paths_queue.put((new_pillar.path_cost, new_pillar))
            else:
                paths_queue.put((new_pillar.path_cost , new_pillar))
    if already_found:
        print(final_value)
    else:
        print("impossible")

def find_neighbour_pillars_inline(pillar, pillars_positions, disks ,dict):
    neighbour = []
    max_r = disks[0][0]
    for pill in pillars_positions:
        if pill[0] == pillar.x:
            if pill[1] > pillar.y:
                for d in disks:
                    dist = distance(pillar.x, pillar.y, pill[0], pill[1])
                    if dist <= pillar.disk[0] + d[0]: # and dist != 0.0: - this is redundant now
                        if (pill[0], pill[1], d[0]) not in dict:
                            new_pillar = Pillar(pill[0], pill[1], (d[0], pillar.path_cost + d[1]))
                            neighbour.append(new_pillar)
                            dict[(pill[0], pill[1], d[0])] = new_pillar
                            #dict[(pill[0], pill[1], d[0])].path_cost = pillar.path_cost + d[1]
                        elif dict[(pill[0], pill[1], d[0])].path_cost > pillar.path_cost + d[1]:
                            neighbour.append(Pillar(pill[0], pill[1], (d[0], pillar.path_cost + d[1])))
                            #dict[(pill[0], pill[1], d[0])].path_cost = pillar.path_cost + d[1]
                    else:
                        break
            # else:
            #     break
    return neighbour

def search_path_in_line(W, starting_pillars, pillars_positions, disks):
    dict ={}
    paths_queue = PriorityQueue()
    for p in starting_pillars:
        paths_queue.put((p.disk[1], p))
        dict[(p.x,p.y,p.disk[0])] = p 
    already_found = False
    final_value = 0
    while(not paths_queue.empty()):
        now_pillar = paths_queue.get()
        
        if now_pillar[1].y + now_pillar[1].disk[0] >= W:
            if already_found:
                if now_pillar[1].path_cost < final_value:
                    if now_pillar[1].path_cost < final_value:
                        final_value = now_pillar[1].path_cost
            else:
                final_value = now_pillar[1].path_cost
                already_found = True
        #if now_pillar[0] == now_pillar[1].path_cost:
        adjacency_pillars = find_neighbour_pillars_inline(now_pillar[1], pillars_positions, disks ,dict)

        for new_pillar in adjacency_pillars:
            if already_found:
                if new_pillar.path_cost < final_value:
                    paths_queue.put((new_pillar.path_cost + (W - new_pillar.y), new_pillar))
            else:
                paths_queue.put((new_pillar.path_cost + (W - new_pillar.y) , new_pillar))
    if already_found:
        print(final_value)
    else:
        print("impossible")


def main():
    """main function of the project, read the input, prepare the canyon graph and search the graph
    """
    t = time.time()
    (W, pillars_positions, disks) = read_input()
    disks = sorted(disks, reverse = True)
    pillars_positions = sorted(pillars_positions)
    # pillars_positions = sorted(pillars_positions, key = lambda x: x[1])
    
    starting_pillars = create_graph(W, pillars_positions, disks)
    inline = False
    if inline:
        search_path_in_line(W, starting_pillars, pillars_positions, disks)
    else:
        search_path(W, starting_pillars, pillars_positions, disks)
    print(time.time() - t)

if __name__ == "__main__":
    main()
