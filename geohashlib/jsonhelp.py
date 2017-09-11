# -*- coding: utf-8 -*-
"""Utility functions to convert json strings to shapely shapes

The below four functions were found in the unit test that Jerry Xu provided
in his geohash shape package.
"""
import json
from shapely.geometry import box, Point, mapping, shape
from shapely.geometry.base import BaseGeometry


class ShapelyEncoder(json.JSONEncoder):
    """For the purpose of exporting shapes into JSON format."""

    def default(self, obj):
        if isinstance(obj, BaseGeometry):
            return mapping(obj)
        return json.JSONEncoder.default(self, obj)


class ShapelyDecoder(json.JSONDecoder):
    """Aims to decode json string into shapely shape."""

    def decode(self, json_string):
        def shapely_object_hook(obj):
            if 'coordinates' in obj and 'type' in obj:
                return shape(obj)
            return obj

        return json.loads(json_string, object_hook=shapely_object_hook)


def export_to_json(data):
    """For the purpose of exporting shapes into JSON format.
    :param data shapely geometry object
    :return str"""
    return json.dumps(data, indent=4, sort_keys=True, cls=ShapelyEncoder)


def load_from_json(json_string):
    """Takes input that's in JSON file formatting and converts it into a shape from shapely.

    :return BaseGeometry
    """
    return json.loads(json_string, cls=ShapelyDecoder)
