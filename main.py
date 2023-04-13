import recastdetour as rd
import plotly.express as px
import pandas as pd
import csv
from flask import Flask, request
from src.conversions import *

app = Flask(__name__)

NAVMESH_BIN_FILE = "Data/uvt-raw.bin"
ROOM_POI_FILE = "Data/RoomsMetadata.csv"


def compute_path(start, end):
    """
    :param start: LatLng
    :param end: LatLng
    :return: path as [LatLng]
    """
    start = start.to_blender_point().to_recast_nav_mesh_point().to_tuple()
    end = end.to_blender_point().to_recast_nav_mesh_point().to_tuple()
    navmesh = rd.Navmesh()
    navmesh.load_navmesh(NAVMESH_BIN_FILE)
    path = navmesh.pathfind_straight(start, end)
    return list(map(lambda p: RecastNavMeshPoint(p).to_blender_point().to_lat_lng(), path))


def plot_path_on_map(path):
    if len(path) <= 0:
        return

    path = list(map(lambda p: p.to_tuple(), path))
    color_scale = [(0, 'orange'), (1, 'red')]
    data = list(zip(*path))
    df = pd.DataFrame({
        "Lat": data[0],
        "Lng": data[1],
        "Level": data[2],
        "Idx": range(0, len(path)),
        "Size": 1
    })
    fig = px.scatter_mapbox(df,
                            lat="Lat",
                            lon="Lng",
                            hover_name="Idx",
                            hover_data=["Lat", "Lng"],
                            color="Level",
                            color_continuous_scale=color_scale,
                            size="Size",
                            zoom=18,
                            height=800,
                            width=800)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


@app.route('/path', methods=['GET'])
def get_path():
    def parse_location_arg(arg):
        return tuple(map(float, arg.split(',')))

    start = request.args['start']
    end = request.args['end']

    if start is None or end is None:
        return "You should provide both start and end parameters.", 400

    start = LatLng(*parse_location_arg(start))
    end = LatLng(*parse_location_arg(end))

    # start, end = LatLng(45.747099, 21.229815, 0), LatLng(45.746722, 21.231551, 0)

    path = compute_path(start, end)
    # plot_path_on_map(path)
    return json.dumps(list(map(lambda p: p.to_tuple(), path)))


@app.route('/poi', methods=['GET'])
def get_poi():
    def parse_csv_tuple(t):
        return tuple(map(float, t[1:-1].split(', ')))

    room_data = {}
    with open(ROOM_POI_FILE, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            row_data = []
            for coo in row[1:]:
                coo_data = parse_csv_tuple(coo)
                # TODO: blender does something really strange
                coo_data = BlenderPoint((coo_data[0], -coo_data[2], coo_data[1])).to_lat_lng().to_tuple()
                row_data.append(coo_data)
            # TODO: blender does something really strange
            row_data[2], row_data[3] = row_data[3], row_data[2]
            room_data[str(row[0])] = row_data
    return json.dumps(room_data)


if __name__ == '__main__':
    app.run()
