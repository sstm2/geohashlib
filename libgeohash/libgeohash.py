
#==============================================================================

import geohash, json
from geojson import Polygon
from shapely.geometry import box, Point,mapping, shape
from shapely.geometry.base import BaseGeometry

#==============================================================================


# The below four functions were found in the unit test that Jerry Xu provided 
# in his geohash shape package.


class ShapelyEncoder(json.JSONEncoder):
    """
    For the purpose of exporting shapes into JSON format.
    """
    def default(self, obj):
        if isinstance(obj, BaseGeometry):
            return mapping(obj)
        return json.JSONEncoder.default(self, obj)


class ShapelyDecoder(json.JSONDecoder):
    """
    Aims to decode json string into shapely shape.
    """
    def decode(self, json_string):

        def shapely_object_hook(obj):
            if 'coordinates' in obj and 'type' in obj:
                return shape(obj)
            return obj

        return json.loads(json_string, object_hook=shapely_object_hook)


def export_to_JSON(data):
    """
    For the purpose of exporting shapes into JSON format.
    """
    return json.dumps(data, indent=4, sort_keys=True, cls=ShapelyEncoder)


def load_from_JSON(json_string):
    """
    Takes input that's in JSON file formatting and converts it into a shape from shapely.
    """
    return json.loads(json_string, cls=ShapelyDecoder)

#==============================================================================

# The functions "neighbor" and "geohash_shape" were the two original functions
# in the geohash_shape package.

def neighbor(geo_hash, direction):
    """
    Find neighbor of a geohash string in certain direction.
    :param geo_hash: geohash string
    :type geo_hash: str
    :param direction: Direction is a two-element array, i.e. [1,0] means north, [1,1] means northeast
    :type direction: list
    :return: geohash string
    :rtype: str
    """
    decode_result = geohash.decode_exactly(geo_hash)
    neighbor_lat = decode_result[0] + direction[0] * decode_result[2] * 2
    neighbor_lon = decode_result[1] + direction[1] * decode_result[3] * 2
    return geohash.encode(neighbor_lat, neighbor_lon, len(geo_hash))


def geohash_shape(shape, precision, mode='intersect', threshold=None):
    """
    Find list of geohashes to cover the shape
    :param shape: shape to cover
    :type shape: BaseGeometry
    :param precision: geohash precision
    :type precision: int
    :param mode: 'intersect' - all geohashes intersect the shape
                               use 'threashold' option to specify a percentage of least coverage
                 'inside' - all geohashes inside the shape
                 'center' - all geohashes whose center is inside the shape
    :type mode: str
    :param threshold: percentage of least coverage
    :type threshold: float
    :return: list of geohashes
    :rtype: list
    """
    (min_lon, min_lat, max_lon, max_lat) = shape.bounds

    hash_south_west = geohash.encode(min_lat, min_lon, precision)
    hash_north_east = geohash.encode(max_lat, max_lon, precision)

    box_south_west = geohash.decode_exactly(hash_south_west)
    box_north_east = geohash.decode_exactly(hash_north_east)

    per_lat = box_south_west[2] * 2
    per_lon = box_south_west[3] * 2

    lat_step = int(round((box_north_east[0] - box_south_west[0]) / per_lat))
    lon_step = int(round((box_north_east[1] - box_south_west[1]) / per_lon))

    hash_list = []

    for lat in xrange(0, lat_step + 1):
        for lon in xrange(0, lon_step + 1):
            next_hash = neighbor(hash_south_west, [lat, lon])
            if mode == 'center':
                (lat_center, lon_center) = geohash.decode(next_hash)
                if shape.contains(Point(lon_center, lat_center)):
                    hash_list.append(next_hash)
            else:
                next_bbox = geohash.bbox(next_hash)
                next_bbox_geom = box(next_bbox['w'], next_bbox['s'], next_bbox['e'], next_bbox['n'])

                if mode == 'inside':
                    if shape.contains(next_bbox_geom):
                        hash_list.append(next_hash)
                elif mode == 'intersect':
                    if shape.intersects(next_bbox_geom):
                        if threshold is None:
                            hash_list.append(next_hash)
                        else:
                            intersected_area = shape.intersection(next_bbox_geom).area
                            if (intersected_area / next_bbox_geom.area) >= threshold:
                                hash_list.append(next_hash)

    return hash_list


    
#==============================================================================
    
# Request #1: Create a function that returns the eight surrounding geohashes.

def neighbors(geo_hash):
    directions = [[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
    surrounding_geohashes = [neighbor(geo_hash,direc) for direc in directions]
    return surrounding_geohashes
    
    
#==============================================================================   


# Request #2: Create a function called hash2poly that takes a set of geohashes 
#             and returns a shape.

def _coordinates(geohashes):
    geohashes = [geohash.decode(h) for h in geohashes]
    return geohashes
    
def _corners(geohashes):
    vertices = []
    for geo in geohashes:
        if (neighbor(geo,[1,0]) in geohashes) and (neighbor(geo,[-1,0]) in geohashes):
            pass
        elif (neighbor(geo,[0,-1]) in geohashes) and (neighbor(geo,[0,1]) in geohashes):
            pass
        else:
            vertices.append(geo)
    return vertices
    
def _shape(vert):
    points = _coordinates(vert)
    return Polygon(points)
    
def hash2poly(geohashes):
    corners_ = _corners(geohashes)
    shape_ = _shape(corners_)
    return shape_
    
#==============================================================================
