from flask import Flask, request
from src.building import UVT_BUILDING
from src.conversions import *

app = Flask(__name__)


# LatLng arguments
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

    path = UVT_BUILDING.compute_path(start, end)
    return json.dumps(list(map(lambda p: p.to_tuple(), path)))


@app.route('/poi', methods=['GET'])
def get_poi():
    return json.dumps(UVT_BUILDING.rooms, default=vars)


if __name__ == '__main__':
    app.run()
