import recastdetour as rd
import json
from flask import Flask

app = Flask(__name__)


def convert_point(point):
    point = list(map(lambda p: p / 1000 / 111, point))
    return [point[0] + 45.74648651703219, 0, point[2] + 21.22946578527367]


@app.route('/')
def get_path():
    navmesh = rd.Navmesh()
    navmesh.load_navmesh("Data/navmesh-test2.bin")
    start = (-3.3, 0, -10.23)
    end = (-3.4, 4.5, 18.31)
    path = navmesh.pathfind_straight(start, end)
    path = list(map(lambda p: convert_point(p), path))
    json_response = json.dumps(path)
    print(json_response)
    return json_response


if __name__ == '__main__':
    app.run()
