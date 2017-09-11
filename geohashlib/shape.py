# -*- coding: utf-8 -*-
"""Functions to translate geohashes to shapes and back

The functions "neighbor" and "shape2geohash" were the two original functions
in the geohash_shape package by Jonathan Xu. shape2geohash was originally called
geohash_shape.

neighbors() was added for convenience and we added geohash2poly
"""
import geohash # from python-geohash
from geojson import Polygon, Point
from shapely.geometry import box


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


def neighbors(geo_hash):
    directions = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]
    surrounding_geohashes = [neighbor(geo_hash, direc) for direc in directions]
    return surrounding_geohashes


def shape2geohash(shape, precision, mode='intersect', threshold=None):
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

    for lat in range(0, lat_step + 1):
        for lon in range(0, lon_step + 1):
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


def _coordinates(geohashes):
    geohashes = [geohash.decode(h) for h in geohashes]
    return geohashes


def _corners(geohashes):
    vertices = []
    for geo in geohashes:
        if (neighbor(geo, [1, 0]) in geohashes) and (neighbor(geo, [-1, 0]) in geohashes):
            pass
        elif (neighbor(geo, [0, -1]) in geohashes) and (neighbor(geo, [0, 1]) in geohashes):
            pass
        else:
            vertices.append(geo)
    return vertices


def _shape(vert):
    points = _coordinates(vert)
    return Polygon(points)


def geohash2shape(geohashes):
    """hash2poly that takes a set of geohashes and returns a shape.
    :param geohashes
    :type geohashes: list
    :return BaseGeometry
    """
    corners_ = _corners(geohashes)
    shape_ = _shape(corners_)
    return shape_
