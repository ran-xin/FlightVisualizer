import gui
import flightdata
import mapgenerator

if __name__ == '__main__':
    location_list = flightdata.read_journey('airport_pairs.csv')
    mapgenerator.map_generation(location_list)
    gui.display()
