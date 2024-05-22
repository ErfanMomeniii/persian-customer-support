import os
import requests
import configparser
import json
from crawl.models.flight import flight
from crawl.models.hotel import hotel

alibaba_flight_url = "https://ws.alibaba.ir/api/v1/flights"
alibaba_hotel_url = "https://ws.alibaba.ir/api/v1/hotel"


def save_to_file(data, file_path=''):
    with open(file_path, 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


class AlibabaScraper:
    def __init__(self, scrap=None):
        if scrap is None:
            scrap = []
        if 'flight' in scrap:
            self.flight_scraper()

        if 'hotel' in scrap:
            self.hotel_scraper()

    @staticmethod
    def flight_scraper():
        config = configparser.ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config.ini')
        config.read(config_path)

        inner_cities = config['cities']['flight_inner_list'].split(',')
        dates = config['dates']['list'].split(',')
        flights = []
        for s in inner_cities:
            for d in inner_cities:
                for adult in range(1, 10):
                    for st in range(0, len(dates)):
                        for fi in range(st + 1, len(dates)):
                            if s != d:
                                try:
                                    data = {
                                        "origin": s,
                                        "destination": d,
                                        "departureDate": dates[st],
                                        "returndate": dates[fi],
                                        "adult": adult,
                                        "child": 0,
                                        "infant": 0,
                                    }

                                    headers = {
                                        'Content-Type': 'application/json',
                                    }

                                    response = requests.request(method="post",
                                                                url=alibaba_flight_url + "/domestic/available",
                                                                headers=headers,
                                                                json=data).json()
                                    response = requests.request(method='get',
                                                                url=alibaba_flight_url + "/domestic/available/" +
                                                                    response['result']['requestId']
                                                                ).json()
                                    departing_flights = response['result']['departing']
                                    returning_flights = response['result']['returning']
                                    for df in departing_flights:
                                        f = flight(df['originName'], df['destinationName'], df['leaveDateTime'],
                                                          df['arrivalDateTime'],
                                                          df['priceAdult'], df['airlineName'])
                                        flights.append(f)

                                    for rf in returning_flights:
                                        f = flight(rf['originName'], rf['destinationName'], rf['leaveDateTime'],
                                                          rf['arrivalDateTime'],
                                                          rf['priceAdult'], rf['airlineName'])
                                        flights.append(f)
                                except:
                                    continue

        data = [f.to_dict() for f in flights]
        save_to_file(data=data, file_path=os.path.join(script_dir, 'flights.json'))
        return

    @staticmethod
    def hotel_scraper():
        config = configparser.ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config.ini')
        config.read(config_path, encoding='utf-8')

        dates = config['dates']['list'].split(',')
        hotel_cities = config['cities']['hotel_list'].split(',')
        hotels = []
        for c in hotel_cities:
            for st in range(0, len(dates)):
                for fi in range(st + 1, len(dates)):
                    for adult in range(0, 10):
                        for child in range(0, 10):
                            try:
                                cl = c.split('_')
                                data = {
                                    "checkIn": dates[st],
                                    "checkOut": dates[fi],
                                    "destination": {
                                        "type": "City",
                                        "id": cl[1]
                                    },
                                    "rooms": [
                                        {
                                            "adults": [30 for i in range(0, adult)],
                                            "children": [7 for i in range(0, child)],
                                        }
                                    ]

                                }

                                headers = {
                                    'Content-Type': 'application/json',
                                }
                                countryCode = "IR"
                                if cl[2] in ["وان", "استانبول", "آنتالیا"]:
                                    countryCode = "TR"
                                elif cl[2] in ["دبی"]:
                                    countryCode = "AE"
                                response = requests.request(method="post",
                                                            url=alibaba_hotel_url + "/search?cityId=" + cl[
                                                                1] + "&countryCode=" + countryCode,
                                                            headers=headers,
                                                            json=data).json()

                                data = {
                                    "sessionId": response["result"]["sessionId"],
                                    "filter": [],
                                    "sort": {
                                        "order": -1,
                                        "field": "score"
                                    },
                                    "skip": 0,
                                    "limit": -1
                                }
                                response = requests.request(method="post",
                                                            url=alibaba_hotel_url + "/result?cityId=" + cl[
                                                                1] + "&countryCode=" + countryCode,
                                                            headers=headers,
                                                            json=data).json()
                                hs = response["result"]["result"]
                                for h in hs:
                                    ht = hotel(
                                        h['name']['fa'],
                                        h['country']['name']['fa'],
                                        h['city']['name']['fa'],
                                        h['pricePerNight'],
                                        adult,
                                        child
                                    )
                                    hotels.append(ht)
                            except:
                                continue

        data = [h.to_dict() for h in hotels]
        save_to_file(data=data, file_path=os.path.join(script_dir, 'hotels.json'))
