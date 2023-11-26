import csv


def read_journey(file_path):
    """
    Reads journey data from a CSV file and returns a list of locations.
    """
    locations = []
    try:
        with open(file_path, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row

            for row in csv_reader:
                locations.append(row)
    except IOError:
        print(f"Error reading file {file_path}")
    return locations


def search_airport(input_iata_code):
    airports = {}
    with open('airports.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            iata_code = row['iata_code']
            if iata_code == input_iata_code:
                return input_iata_code, row['latitude_deg'], row['longitude_deg']


def add_journey(dep, arr, file_path='airport_pairs.csv'):
    dep_airport = search_airport(dep)
    arr_airport = search_airport(arr)
    new_entry = [dep_airport[0], arr_airport[0]]

    # Read all data from the CSV file
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    # Check if the new entry exists and modify data
    found = False
    for i in range(0, len(rows)):
        if rows[i] == new_entry:
            found = True
            # TODO: Temporary testing
            rows.append(new_entry)
            break

    # Add the new entry if not found
    if not found:
        rows.append(new_entry)

    # Write the modified data back to the CSV file
    with open(file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows)
    return 0
