import math
from queue import PriorityQueue

class Pillar(object):
    """ x and y coordinates for each pillar object has its  (for its placement on the graph). """

    def __init__(self, x, y, *args):  
        self.x = x
        self.y = y
        self.disk = args[0] 
        self.path_cost = self.disk[1]
        if len(args) == 2:
            self.path_cost = args[1]
        self.adjacency_pillars = {}
        

    def __lt__(self, other):
        return self.path_cost < other.path_cost





def read_input(): 
    """read the standard input and store pillars using pillar class, and then group them in a list, 
        save also the possible disks with their properties (radius, cost) in a list and store W value of the canyon.
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
        for d in disks:
            if int(r_i) < d[0]:
                if int(c_i) >= d[1]:
                    valid = False
            if int(r_i) > d[0]:
                if int(c_i) <= d[1]:
                    disks.remove(d)
        if valid:
            disks.append((int(r_i),int(c_i)))
    return (y_goal, pillars_positions, disks)

def take_starting_pillars(W, pillars_positions, max_r, disks): 
    starting_pillars = []
    for p in pillars_positions:
        if p[1] <= max_r:
            for d in disks:
                if p[1] <= d[0]:
                    starting_pillars.append(Pillar(p[0],p[1],d))
                else:
                    break
    return starting_pillars

def create_graph(W, pillars_positions, disks): 
    max_r = disks[0][0]
    starting_pillars = take_starting_pillars(W, pillars_positions ,max_r, disks)
    return starting_pillars

def distance(x1, y1, x2, y2): 
    return math.sqrt(pow((x1 - x2),2) + pow((y1 - y2),2))

def find_neighbour_pillars(pillar, pillars_positions, disks ,dict, final_value, already_found):
    new_dict={}
    max_r = disks[0][0]
    for pill in pillars_positions:
        if pill[0] >= pillar.x - max_r*2:
            if pill[0] <= pillar.x + max_r*2:
                dist = distance(pillar.x, pillar.y, pill[0], pill[1])
                for d in disks:
                    if already_found:
                        if pillar.path_cost + d[1] >= final_value:
                            break
                    if dist <= pillar.disk[0] + d[0] and dist != 0.0:
                        if (pill[0], pill[1], d[0]) not in dict:
                            new_pillar = Pillar(pill[0], pill[1], d, pillar.path_cost + d[1])
                            # neighbour.append(new_pillar)
                            dict[(pill[0], pill[1], d[0])] = new_pillar
                            new_dict[(pill[0], pill[1], d[0])] = new_pillar      
                    else:
                        break
            else:
                break
    return new_dict


def search_path(W, starting_pillars, pillars_positions, disks, impossible_check):
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
                if impossible_check:
                    return 0
                final_value = now_pillar[1].path_cost
                already_found = True
        adjacency_pillars = find_neighbour_pillars(now_pillar[1], pillars_positions, disks ,dict ,final_value, already_found)
        for new_pillar_key in adjacency_pillars:
            obj = adjacency_pillars[new_pillar_key]
            paths_queue.put((obj.path_cost , obj))
    if already_found:
        return final_value
    else:
        return "impossible"

def main():
    
    (W, pillars_positions, disks) = read_input()
    disks = sorted(disks, reverse = True)
    pillars_positions = sorted(pillars_positions)
    starting_pillars_impossible = create_graph(W, pillars_positions, [disks[0]])
    if search_path(W, starting_pillars_impossible, pillars_positions, [disks[0]], True) != "impossible":
        starting_pillars = create_graph(W, pillars_positions, disks)
        print(search_path(W, starting_pillars, pillars_positions, disks, False))
    else:
        print("impossible")
    


if __name__ == "__main__":
    main()
