import numpy as np
import math


def detect_cross_antimeridian(start, end):
    """
    Detects if the path between two points crosses the antimeridian.
    Adjusts coordinates if necessary.
    """
    start_lat, start_lon = np.radians(start)
    end_lat, end_lon = np.radians(end)

    crosses_antimeridian = abs(end_lon - start_lon) > np.pi
    if crosses_antimeridian:
        end_lon = end_lon - 2 * np.pi if end_lon > start_lon else end_lon

    return (np.degrees(start_lat), np.degrees(start_lon)), (
        np.degrees(end_lat), np.degrees(end_lon)), crosses_antimeridian


def get_arced_coordinates(start, end, crosses_antimeridian, num_points=100):
    """
    Returns coordinates of the curved line between start and end points.
    """
    start_lat, start_lon = np.radians(start)
    end_lat, end_lon = np.radians(end)

    great_circle_distance = np.arccos(
        np.sin(start_lat) * np.sin(end_lat) + np.cos(start_lat) * np.cos(end_lat) * np.cos(end_lon - start_lon))
    fractions = np.linspace(0, 1, num_points)

    intermediates = []
    for fraction in fractions:
        a = np.sin((1 - fraction) * great_circle_distance) / np.sin(great_circle_distance)
        b = np.sin(fraction * great_circle_distance) / np.sin(great_circle_distance)
        x = a * np.cos(start_lat) * np.cos(start_lon) + b * np.cos(end_lat) * np.cos(end_lon)
        y = a * np.cos(start_lat) * np.sin(start_lon) + b * np.cos(end_lat) * np.sin(end_lon)
        z = a * np.sin(start_lat) + b * np.sin(end_lat)
        intermediate_lat = np.arctan2(z, np.sqrt(x ** 2 + y ** 2))
        intermediate_lon = np.degrees(np.arctan2(y, x))
        if intermediate_lon > 0 and crosses_antimeridian:
            intermediate_lon -= 360
        intermediates.append([np.degrees(intermediate_lat), intermediate_lon])
    return intermediates


def haversine(coord1, coord2):
    R = 6371.0  # Earth radius in kilometers

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance
