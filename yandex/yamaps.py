import requests
from lxml import etree



class YandexMapShot(object):
    def __init__(self, lat, lon, result):
        self.lat = lat
        self.lon = lon
        self.result = result
        self.https = """https://static-maps.yandex.ru/1.x/?l=map&"""

    def create_request(self):
        self.https += "ll=%s,%s&size=650,450&z=12&pt=" % (self.lon, self.lat)

        markset = ("pm2gnl1","pm2bll2","pm2ywl3","pm2rdl4","pm2vvl5")
        N = len(self.result)
        for i in range(N):
            mark = "%s,%s,%s~" % (self.result[i][3],self.result[i][2],markset[i % len(markset)])
            self.https += mark
        ya = "%s,%s,ya_ru" % (str(self.lon), str(self.lat))
        self.https += ya

    def send_request(self):
        answer = requests.get(self.https)
        img = answer.content
        return img

    def run(self):
        self.create_request()
        img = self.send_request()
        return img

