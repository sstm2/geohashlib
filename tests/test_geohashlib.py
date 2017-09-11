import json
import geohashlib as g

test_shape = {"type": "Polygon",
              "coordinates": [[[-73.9741, 40.7626], [-73.9736, 40.7626], [-73.9737, 40.7622], [-73.9740, 40.7622]]]}
test_geojson = json.dumps(test_shape)

def test_shape2geohash():
    expected_geohashes = ['dr5rus']
    shape = g.load_from_json(test_geojson)
    assert (expected_geohashes == g.shape2geohash(shape, 6))

def test_geohash2shape():
    shape = g.load_from_json(test_geojson)
    test_geohashes = g.shape2geohash(shape, 9)
    expected_shape = {"coordinates": [[40.76225996017456, -73.9739727973938], [40.76225996017456, -73.97371530532837],
                                   [40.762388706207275, -73.97401571273804], [40.762431621551514, -73.97367238998413],
                                   [40.76256036758423, -73.97405862808228], [40.76256036758423, -73.97367238998413]],
                   "type": "Polygon"}
    shape = g.geohash2shape(test_geohashes)
    assert (True)