"""
sys: Exiting the application when error
json: to parse the response from MVG API
pandas: to parse departureTime which is in ms
requests: To make requests to the MVG API
datetime: To calculate the timedelta
"""
import sys
import json
import pandas
import requests as req
from datetime import datetime, timedelta


class Departure:
    """
    This class provides the departure times of a station
    of the MVG.
    """

    def __init__(self, station_name):
        stations_json = self.get_stations(station_name)
        parsed_stations = self.parse_stations(stations_json)
        departures = self.get_departures(parsed_stations[0][1])
        parsed_departures = self.parse_departures(departures)
        print(self.toString(parsed_departures))

    def get_stations(self, user_input):
        """
        Get request to MVG API for list of stations
        witch matches the parameter

        :param user_input: stations to search
        :return: all available stations matching the input
        """

        url = 'https://www.mvg.de/api/fahrinfo/location/queryWeb?q={}'.format(user_input)
        request = req.get(url)

        if request.status_code == 200:
            return json.loads(request.text)['locations']
        else:
            print('Error while fetching data')
            sys.exit(1)

    def parse_stations(self, stations_json):
        """
        Parsing stations to get id and name

        :param stations_json: json formatted string with all
            stations to be parsed
        :return: array format: (name, id)
        """
        output = []

        for station in stations_json:
            output.append((station['name'], station['id']))

        return output

    def get_departures(self, station_id):
        """
        Returns list of departures of station

        :param station_id: Id of station
        :return: list of departures
        """

        url = 'https://www.mvg.de/api/fahrinfo/departure/{}?footway=0'.format(station_id)

        request = req.get(url)

        if request.status_code == 200:
            return json.loads(request.text)['departures']
        else:
            print('Error while fetching data')
            sys.exit(1)

    def parse_departures(self, departures_json):
        """
        Filters only needed information of departures

        :param departures_json: json file of departures
        :return: filtered output. format: (product, destination, line_number)
        """
        output = []

        for departure in departures_json:
            product = departure['product']
            departure_time = self.calc_dep_time(departure['departureTime'])
            destination = departure['destination']
            label = departure['label']

            output.append((product, departure_time, destination, label))

        return output

    def calc_dep_time(self, departure_time):
        """
        Calculates the timedelta between now and the departure time

        "BUG": When the computer has a delay of a few minutes the return
        value will be (23,59) or something like that.
        Workaround: Replace it with now while parsing

        :param departure_time: the departure time in ms
        :return: array. format: (hours, minutes)
        """
        time_object = pandas.to_datetime(departure_time, unit='ms') + timedelta(hours=1)
        time_object = time_object.strftime('%Y-%m-%d %H:%M')
        time_object = datetime.strptime(time_object, '%Y-%m-%d %H:%M')
        date_obj_now = datetime.now()

        t_delta = time_object - date_obj_now

        return t_delta.seconds // 3600, int(t_delta.seconds % 3600 / 60.0)

    def to_string(self, departures):
        """
        Returns the departure times of a station as a string.
        Format:
        '{}: {: <8} - {}\n'.format(departure_time, label, destination)

        :param departures: departures as array like delivered from
                self.parse_stations(self, stations_json)
        :return: formatted string
        """

        output = ""
        for departure in departures:
            product = departure[0]
            hours, minutes = departure[1]
            destination = departure[2]
            label = departure[3]

            if minutes == 0 or hours == 23 and minutes == 59 \
                    or hours == 23 and minutes == 57:
                departure_time = '{: <9}'.format('now')
            else:
                if hours:
                    departure_time = \
                            'In {: <2} h:{: <2} min'.format(hours, minutes)
                else:
                    departure_time = 'In {: <2} min'.format(minutes)

            if product == 'BUS':
                label = 'Bus {}'.format(label)
            elif product == 'TRAM':
                label = 'Tram {}'.format(label)

            output += '{}: {: <8} - {}\n'  \
                .format(departure_time, label, destination)

        return output
