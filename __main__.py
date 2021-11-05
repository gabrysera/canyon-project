import math

"""
class Canyon_area(object):
    def __init__(self, x, y, pillars_subset):
        self.number_x = x
        self.number_y = y
        self.pillars = pillars_subset

#def create_adjacency_matrix():
    
def find_pillars(y_bound, x_bound, max_r, pillars):
    
    return 
"""
class Pillar(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dict = {}

    def set_reachable_node(self, p, dist):
        self.dict[p] = dist

def distance(p1,p2):
    return math.sqrt(pow((p1.x - p2.x),2) + pow((p1.y - p2.y),2))

def min_cost(dist, disks):
    res = []
    for d in disks:
        if d[0]*2 >= dist:
            res.append(d)
    res.sort(key=lambda x:x[1])
    return res[0][1]

def reachable_pillars(p, pillars, threshold, disks):
    res = []
    for p0 in pillars:
        dist = distance(p0, p)
        if dist <= threshold:
            res.append((p0,min_cost(dist, disks)))
            cost = res[-1][1]
            p0.set_reachable_node(p, cost)
            p.set_reachable_node(p0, cost)
    return res

def create_adjacency_matrix(W, pillars, disks, max_r):
    start_index = 0
    for p in pillars:
        start_index += 1
        reachable = reachable_pillars(p, pillars[start_index:], 2*max_r, disks)
        print(p.dict)

def create_graph(W, pillars, disks):
    #store pillars optimal distances/costs
    #after a path is found, optimizie it (checks if you can reduce cost)
    disks = sorted(disks)
    max_r = disks[-1][0]
    create_adjacency_matrix(W, pillars, disks, max_r)
    return 

def read_input():
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
