import recastdetour as rd
import json
import utm
import plotly.express as px
import pandas as pd
from flask import Flask

app = Flask(__name__)


class UVTConvertor:
    def __init__(self):
        (self.easting, self.northing, self.zone_number, self.zone_letter) = utm.from_latlon(45.74666101971023, 21.230468210382533)

    def three_d_space_to_lat_lng(self, point):
        (lat, lng) = utm.to_latlon(self.easting + point[0], self.northing - point[2], self.zone_number, self.zone_letter)
        return lat, lng, point[1]

    def lat_lng_to_three_d_space(self, lat, lng, level=0):
        easting2, northing2, zone_number2, zone_letter2 = utm.from_latlon(lat, lng)
        return easting2 - self.easting, level, -(northing2 - self.northing)


def compute_path(start, end):
    convertor = UVTConvertor()
    start = convertor.lat_lng_to_three_d_space(*start)
    end = convertor.lat_lng_to_three_d_space(*end)
    navmesh = rd.Navmesh()
    navmesh.load_navmesh("Data/uvt-raw.bin")
    path = navmesh.pathfind_straight(start, end)
    return list(map(lambda p: convertor.three_d_space_to_lat_lng(p), path))


def plot_path_on_map(path):
    if len(path) <= 0:
        return

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
    start = (-50, 0, -50)
    end = (85, 0, -5)
    convertor = UVTConvertor()
    path = compute_path(convertor.three_d_space_to_lat_lng(start), convertor.three_d_space_to_lat_lng(end))
    plot_path_on_map(path)
    json_response = json.dumps(path)
    print(json_response)
    return json_response


if __name__ == '__main__':
    get_path()
    app.run()
