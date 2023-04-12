import recastdetour as rd

if __name__ == '__main__':
    navmesh = rd.Navmesh()
    navmesh.load_navmesh("../Data/navmesh-test2.bin")
    start = [-3.3, 0, -10.23]
    end = [-3.4, 4.5, 18.31]
    path = navmesh.pathfind_straight(start, end)
    print(path)
