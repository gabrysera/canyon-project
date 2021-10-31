
def read_input():

    number_of_pillars,m_kind_of_disks,y_goal = list(map(int, input().split()))
    pillars = disks = []

    for i in range(0, number_of_pillars):
        (x_i,y_i) = list(map(int, input().split()))
        pillars.append((int(x_i),int(y_i)))

    for i in range(0, m_kind_of_disks):
        (r_i, c_i) = list(map(int, input().split()))
        disks.append((int(r_i),int(c_i)))

def main():
    read_input()

if __name__ == "__main__":
    main()
