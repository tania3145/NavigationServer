import csv
import recastdetour as rd
import pandas as pd
import plotly.express as px
from src.conversions import *

NAVMESH_BIN_FILE = 'Data/uvt-raw.bin'
ROOM_POI_FILE = 'Data/RoomsMetadata.csv'


class Room:
    def __init__(self, index, name, coordinates):
        self.index = index
        self.name = name
        self.coordinates = coordinates

    def __str__(self):
        return f'Room(Index: {self.index}, Name: {self.name}, Coordinates({len(self.coordinates)}): {self.coordinates})'

    def __repr__(self):
        return self.__str__()


class Building:
    def __init__(self, navmesh, rooms):
        self.navmesh = navmesh
        self.rooms = rooms

    @staticmethod
    def from_files(navmesh_path, room_poi_path):
        def parse_csv_tuple(t):
            return tuple(map(float, t[1:-1].split(', ')))

        navmesh = rd.Navmesh()
        navmesh.load_navmesh(navmesh_path)

        rooms = []
        with open(room_poi_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                row_data = []
                for coo in row[1:]:
                    coo_data = parse_csv_tuple(coo)
                    # TODO: blender does something really strange so we have to convert to RecastNavMeshPoint
                    coo_data = RecastNavMeshPoint(coo_data).to_blender_point().to_lat_lng().to_tuple()
                    row_data.append(coo_data)
                # TODO: blender order is triangle draw so we have to swap the last 2 rows
                row_data[2], row_data[3] = row_data[3], row_data[2]
                rooms.append(Room(str(row[0]), str(row[0]), row_data))
        return Building(navmesh, rooms)

    def compute_path(self, start, end):
        """
        :param start: LatLng
        :param end: LatLng
        :return: path as [LatLng]
        """
        start = start.to_blender_point().to_recast_nav_mesh_point().to_tuple()
        end = end.to_blender_point().to_recast_nav_mesh_point().to_tuple()
        path = self.navmesh.pathfind_straight(start=start, end=end)

        return list(map(lambda p: RecastNavMeshPoint(p).to_blender_point().to_lat_lng(), path))

    @staticmethod
    def plot_path_on_map(path):
        if len(path) <= 0:
            return

        path = list(map(lambda p: p.to_tuple(), path))
        color_scale = [(0, 'orange'), (1, 'red')]
        data = list(zip(*path))
        df = pd.DataFrame({
            'Lat': data[0],
            'Lng': data[1],
            'Level': data[2],
            'Idx': range(0, len(path)),
            'Size': 1
        })
        fig = px.scatter_mapbox(df,
                                lat='Lat',
                                lon='Lng',
                                hover_name='Idx',
                                hover_data=['Lat', 'Lng'],
                                color='Level',
                                color_continuous_scale=color_scale,
                                size='Size',
                                zoom=18,
                                height=800,
                                width=800)

        fig.update_layout(mapbox_style='open-street-map')
        fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        fig.show()


UVT_BUILDING = Building.from_files(NAVMESH_BIN_FILE, ROOM_POI_FILE)
