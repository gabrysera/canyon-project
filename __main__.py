import math

class Pillar(object):
    """ x and y coordinates for each pillar object has its  (for its placement on the graph). """
    def __init__(self, x, y):  
        self.x = x
        self.y = y
        self.dict = {}

    def set_reachable_node(self, p, possible_disks): 
        """ this function can be used to add a reachable pillar object p to the dictionary of nodes accesible to the main pillar object, and the distance associated to reach it. """
        self.dict[p] = possible_disks

def distance(p1,p2): 
    """ given two points, this function returns the (Pythogorean) distance between the two Pillar objects."""
    return math.sqrt(pow((p1.x - p2.x),2) + pow((p1.y - p2.y),2))

def possible_disks(dist, disks_pairs): 
    "this function includes all the possible disc sizes that could be used to reach the distance required to the other pillar, and in the end return the size of the cheapest disc. """
    possible_disks = []
    for disk in disks_pairs:
        if disk[2] >= dist:
            possible_disks.append(disk)
    return sorted(possible_disks, key=lambda x: x[3])
    
def reachable_pillars(p, pillars, threshold, disks_pairs): 
    """ given a starting pillar, it compares with every other pillar, and if the distance between them is less than the biggest sized disc available(threshold), then its added as a reachable node to both """
    for p0 in pillars:
        dist = distance(p0, p)
        if dist <= threshold:
            p_p0_pairs = possible_disks(dist, disks_pairs)
            p0.set_reachable_node(p, p_p0_pairs)
            p.set_reachable_node(p0, p_p0_pairs)
    #return res #self note: instead of appending to res and returning, what if we dont append to it and return that

def create_adjacency_matrix(W, pillars, disks_pairs, max_r): 
    """ this function creates the adjacency list by using dictionaries with each pillar object as key and its values including a nested dictionary of the nodes accessible to it and the cost to access it. """
    start_index = 0
    for p in pillars:
        start_index += 1
        #reachable = 
        reachable_pillars(p, pillars[start_index:], 2*max_r, disks_pairs)

def disks_combinations(disks):
    combinations = []
    for d in disks:
        for d1 in disks:
            combinations.append((d[0],d1[0],d[0]+d1[0],d[1]+d1[1]))
    return combinations

def create_graph(W, pillars, disks): 
    """ this function sorts the disks with increasing size and chooses the biggest disc size available as the maximum size to pass as the threshold to the function for creating the adjacency matrix. """
    #store pillars optimal distances
    #only store distances, and then while you run the search you add cost depending on the actual disk
    #after a path is found, optimizie it (checks if you can reduce cost) 
    disks = sorted(disks)
    max_r = disks[-1][0]
    disks_pairs = sorted(disks_combinations(disks), key=lambda x: x[2], reverse=True)
    create_adjacency_matrix(W, pillars, disks_pairs, max_r)
    for p in pillars:
        print(p.x,p.y)
        items = p.dict.items()
        print("nodes reachable from here: \n")
        for i in items:
            print(i[0].x,i[0].y,i[1])
            print("\n")
        print("\n")
    return 

def read_input(): 
    """ this function reads the input and stores them into variables and appends others as tuples to lists to be later used in creating a graph representation and running the Dijstra's algorithm on it. """
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

def main():
    (W, pillars, disks) = read_input()
    create_graph(W, pillars, disks)

if __name__ == "__main__":
    main()
