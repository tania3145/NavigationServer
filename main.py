import recastdetour as rd
import json
import plotly.express as px
import pandas as pd
from flask import Flask

from src.conversions import *

app = Flask(__name__)


def compute_path(start, end):
    """
    :param start: LatLng
    :param end: LatLng
    :return: path as [LatLng]
    """
    start = start.to_blender_point().to_recast_nav_mesh_point().to_tuple()
    end = end.to_blender_point().to_recast_nav_mesh_point().to_tuple()
    navmesh = rd.Navmesh()
    navmesh.load_navmesh("Data/uvt-raw.bin")
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


@app.route('/')
def get_path():
    start = LatLng(45.74709967206854, 21.229815840540294)
    end = LatLng(45.7467227634899, 21.2315518683754)

    path = compute_path(start, end)
    plot_path_on_map(path)
    json_response = json.dumps(path)
    print(json_response)
    return json_response


if __name__ == '__main__':
    get_path()
    app.run()
