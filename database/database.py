import psycopg2
import datetime
import time

class BDEngine(object):
    def __init__(self, dbname, usr, psw, host):
        self.connection = psycopg2.connect(database=dbname, user=usr, host=host, password=psw)
        self.cursor = self.connection.cursor()

    def __get_id_from_station(self,station):
        if station.lower().find("москва") != -1:
            station = "Москва Курская"

        request = """select id from stations where station_name ilike '%s'""" % station
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if len(result) == 0:
            return None
        id = result[0][0]
        return id

    def __get_trains_between_stations_id(self,id_from, id_to):
        request = """select AA.train_id,BB.operating_day,AA.stations,AA.time from schedule_stations as AA join 
                        train_schedules as BB on AA.train_id = BB.train_id 
                        where (array_position(AA.stations,%d) < array_position(AA.stations,%d))""" % (id_from , id_to)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        return result

    def __get_row_count_of_users(self):
        request = """select id from users"""
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        return len(result)


    def get_station_from_id(self, id):
        return self.__get_station_from_id(id)

    def __get_station_from_id(self,id):
        request = """select station_name from stations where id = %d""" % id
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if len(result) == 0:
            return None
        name = result[0][0]
        return name

    def __get_train_number_from_train_id(self,train_id):
        request = """select train_number from trains where id = %d""" % train_id
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        name = result[0][0]
        return name

    def __get_train_id_from_train_number(self,train_number, train_start):
        station_id = self.__get_id_from_station(train_start)
        request = """select id from trains where (train_number = %s and departure_station = %d)""" % (train_number, station_id)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        name = result[0][0]
        return name

    def __operating_day_id(self,train_id):
        request = """select operating_day from train_schedules where train_id = %d""" % train_id
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        name = result[0][0]
        return name


    def get_info_from_train_number(self,train_number):
        request = """select BB.train_number, AA.stations, AA.time from schedule_stations as AA join trains as BB on AA.train_id = BB.id
                        where BB.train_number = %s""" % train_number
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if len(result) == 0:
            return None
        elif len(result) > 1:
            result = result[0]
        return result


    def get_info_from_train_number2(self,train_number, train_start):
        train_start = self.__get_id_from_station(train_start)
        request = """select BB.train_number, AA.stations, AA.time from schedule_stations as AA join trains as BB on AA.train_id = BB.id
                        where BB.train_number = %s and BB.departure_station = %s""" % (train_number, train_start)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if len(result) == 0:
            return None
        return result[0]


    def __replace_ids(self,trains):
        if trains is None:
            return None

        for i in range(len(trains)):
            trains[i] = list(trains[i])

        for train in trains:
            train[0] = self.__get_train_number_from_train_id(train[0])

            stations = train[2] #stations list
            for i in range(len(stations)):
                stations[i] = self.__get_station_from_id(stations[i])
        return trains

    def __time_choosing(self,time,station,trains,delta = 15):
        def is_in_list(time1,time2):
            result = False
            today = datetime.date.today()
            dateTimeA = datetime.datetime.combine(today, time1)
            dateTimeB = datetime.datetime.combine(today, time2)
            diff = (dateTimeA - dateTimeB).total_seconds() / 60 #minutes
            if abs(diff) < delta:
                result = True
            return result

        N = len(trains)
        for i in range(N-1,-1,-1):
            stations = trains[i][2]
            times = trains[i][3]
            station_index = stations.index(station)
            if not is_in_list(time,times[station_index]):
                del trains[i]
        return trains

    def get_scheduler(self,station_from, station_to, time = None):
        id_from = self.__get_id_from_station(station_from)
        id_to = self.__get_id_from_station(station_to)
        if id_from is None or id_to is None:
            return None
        trains = self.__get_trains_between_stations_id(id_from,id_to) 
        if time is not None:
            trains = self.__time_choosing(time,id_from,trains)
        trains = self.__replace_ids(trains)

        return trains

    def save_user(self,chat_id,train_number,station_from,station_to,train_start, name = "NULL"):
        err = False
        id_from = self.__get_id_from_station(station_from)
        id_to = self.__get_id_from_station(station_to)
        train_id = self.__get_train_id_from_train_number(train_number,train_start)
        if self.__consist_train_for_trainid(train_id,chat_id):
            err = True
            return err

        id = self.__get_row_count_of_users()+1
        name = '\''+name+'\''
        request = """insert into users (id,chat_id, first_name, train_id, station_id_from, station_id_to) 
                    values (%d,%s,%s,%d,%d,%d)""" % (id,chat_id,name,train_id,id_from,id_to)
        self.cursor.execute(request)
        self.connection.commit()
        return err

    def __consist_train_for_trainid(self, trainid, chat_id):
        request = """select id from users where train_id = %s and chat_id = %s""" % (trainid,chat_id)
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False

    def get_time_station(self,station_start ,station_name ,train_number):
        res = self.get_info_from_train_number(train_number)
        result = None
        for r in res:
            ff = self.__get_station_from_id(r[1][0])
            if ff == station_start:
                result = r

        times = result[2]
        stations = result[1]
        for i in range(len(stations)):
            stations[i] = self.__get_station_from_id(stations[i])


        N = len(times)
        for i in range(N):
            if stations[i] == station_name:
                return times[i]
        return None

    def get_user(self, login):
        request = """select * from users where login= '%s'""" % login
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        return result



