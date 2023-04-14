from flask import Flask, request
from src.building import UVT_BUILDING
from src.conversions import *

app = Flask(__name__)


@app.route('/path', methods=['GET'])
def get_path():
    def parse_location_arg(arg):
        return tuple(map(float, arg.split(',')))

    start = request.args['start']
    end = request.args['end']

    if start is None or end is None:
        return 'You should provide both start and end parameters.', 400

    start = LatLng(*parse_location_arg(start))
    end = LatLng(*parse_location_arg(end))

    # start, end = LatLng(45.747099, 21.229815, 0), LatLng(45.746722, 21.231551, 0)

    path = UVT_BUILDING.compute_path(start, end)
    # plot_path_on_map(path)
    return json.dumps(list(map(lambda p: p.to_tuple(), path)))


@app.route('/poi', methods=['GET'])
def get_poi():
    return json.dumps(UVT_BUILDING.rooms, default=vars)


if __name__ == '__main__':
    app.run()
