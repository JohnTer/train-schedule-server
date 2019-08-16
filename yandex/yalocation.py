import requests
from lxml import etree




class YandexNearestLocations(object):
    def __init__(self, lat, lon, ya_key, radius = 5, limit = 5):
        self.apikey = ya_key
        self.http = "https://api.rasp.yandex.net/v3.0/nearest_stations/?apikey=%s" % self.apikey
        self.lat = lat
        self.lon = lon
        
        self.radius = radius
        self.transport_types = "suburban,train"
        self.limit = limit

    def create_string_request(self):
        self.http += "&format=xml&lat=%f&lng=%f&distance=%d&transport_types=%s&limit=%d&lang=ru_RU" \
        % (self.lat,self.lon,self.radius,self.transport_types, self.limit)

    def send_request(self):
        answer = requests.get(self.http)
        text = answer.text
        return text

    def get_stations(self,xml):
        stations = []
        xml = xml[xml.index('\n')+1:]
        root = etree.fromstring(xml)
        childs = root.getchildren()
        for i in range(1,len(childs)):
            elem = childs[i]
            station_name = elem.find('title').text
            station_distance = elem.find('distance').text
            lat = elem.find('lat').text
            lon = elem.find('lng').text
            stations.append((station_name,station_distance,lat,lon))
        return stations


    def run(self):
        self.create_string_request()
        xml = self.send_request()
        result = self.get_stations(xml)
        return result
