from src.building import UVT_BUILDING

if __name__ == '__main__':
    print(*UVT_BUILDING.rooms, sep='\n')
    # print(json.dumps(UVT_BUILDING.rooms, default=vars))
    # start, end = LatLng(45.747099, 21.229815, 0), LatLng(45.746722, 21.231551, 0)
    # path = UVT_BUILDING.compute_path(start, end)
    # Building.plot_path_on_map(path)
