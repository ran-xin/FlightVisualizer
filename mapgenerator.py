import folium

import flightdata
import calculation

def map_generation(route):
    """
    Plots curved lines on a map for each pair of locations with tooltips.
    """
    map_center = [-50, 40]  # A central point for initializing the map
    m = folium.Map(location=map_center, zoom_start=2, min_zoom=2, max_zoom=10)
    m.fit_bounds([[-70, -270], [90, 180]])

    flights = {}

    # Process routes and assign colors
    for rte in route:
        flight_direction = (rte[0], rte[1])
        if flight_direction not in flights and (rte[1], rte[0]) not in flights:
            flights[flight_direction] = ["blue", 1]
        elif flight_direction in flights:
            flights[flight_direction][1] += 1
        else:
            flights[flight_direction] = ["red", 1]

    # Collect keys to be removed after iteration
    keys_to_remove = set()

    for key in flights:
        if key in keys_to_remove:
            continue

        reverse_key = (key[1], key[0])
        start_coordinate = [float(i) for i in flightdata.search_airport(key[0])[1:]]
        end_coordinate = [float(i) for i in flightdata.search_airport(key[1])[1:]]
        adjusted_start, adjusted_end, crosses_antimeridian = calculation.detect_cross_antimeridian(start_coordinate, end_coordinate)
        arced_coordinates = calculation.get_arced_coordinates(adjusted_start, adjusted_end, crosses_antimeridian)

        count = flights[key][1]
        count_reverse = flights[reverse_key][1] if reverse_key in flights else 0

        for i in range(-count, count_reverse):
            processed_coordinates = []
            processed_coordinates.append(arced_coordinates[0])
            for j in range(1, len(arced_coordinates)-1):
                offset = j if j <= 0.5 * len(arced_coordinates) else len(arced_coordinates) - j
                new_longitude = arced_coordinates[j][1] + (i * calculation.haversine(adjusted_start, adjusted_end)*0.00001 * offset)
                processed_coordinates.append([arced_coordinates[j][0], new_longitude])
            processed_coordinates[-1] = arced_coordinates[-1]

            color = flights[key][0] if i < 0 else flights[reverse_key][0]
            folium.PolyLine(processed_coordinates, color=color, weight=1.5, opacity=1).add_to(m)
            folium.CircleMarker(adjusted_start, radius=2.5, color='red', fill=True, fill_color='orange', fill_opacity=1,
                                    tooltip=key[0]).add_to(m)
            folium.CircleMarker(adjusted_end, radius=2.5, color='red', fill=True, fill_color='orange', fill_opacity=1,
                                    tooltip=key[1]).add_to(m)
        print("1")
        keys_to_remove.add(key)
        keys_to_remove.add(reverse_key)

    # Remove processed keys
    for key in keys_to_remove:
        flights.pop(key, None)

    m.save("world_map.html")






