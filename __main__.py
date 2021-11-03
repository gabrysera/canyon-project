import math


class Canyon_area(object):
    def __init__(self, x, y, pillars_subset):
        self.number_x = x
        self.number_y = y
        self.pillars = pillars_subset

#def create_adjacency_matrix():
    
def find_pillars(y_bound, x_bound, max_r, pillars):
    
    return 

def create_graph(W, pillars, disks):
    #pillar X_i, Y_i can only touch pillars at 

    #2) determine if the graph would be sparse or dense
    #3) build adjecency data structure
    #4) djikstra
    pillars = sorted(pillars)
    max_x = pillars[-1][0]#max(pillars, key=lambda x:x[0])[0]
    max_r = max(disks, key=lambda x:x[0])[0]
    areas = [[Canyon_area(y_area, x_area,find_pillars(y_area, x_area, max_r, pillars)) for x_area in range(int(math.ceil(max_x/(max_r*2))))] for y_area in range(int(math.ceil(W/(max_r*2))))]
    print(len(areas),len(areas[0]))
    return 

def read_input():
    number_of_pillars,m_kind_of_disks,y_goal = list(map(int, input().split()))
    pillars = []
    disks = []
    for i in range(0, number_of_pillars):
        (x_i,y_i) = list(map(int, input().split()))
        pillars.append((int(x_i),int(y_i)))

    for i in range(0, m_kind_of_disks):
        (r_i, c_i) = list(map(int, input().split()))
        disks.append((int(r_i),int(c_i)))

    return (y_goal, pillars, disks)

def main():
    (W, pillars, disks) = read_input()
    create_graph(W, pillars, disks)

if __name__ == "__main__":
    main()
