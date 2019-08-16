import datetime
import projsettings
import threading
import time
from database.database import BDEngine
from yandex.yamaps import YandexMapShot
from yandex.yalocation import YandexNearestLocations
from dataformatter.dataformatter import Formatter
from validator.validator import Validator

class Model(object):
    def __init__(self):
        self.bd = BDEngine(projsettings.DBNAME, projsettings.DB_USER, projsettings.DB_PASSWORD, projsettings.DB_HOST)
        self.formatter = Formatter()
        self.validator = Validator()

    def get_scheduler_between(self, station_from, station_to):
         shed = self.bd.get_scheduler(station_from, station_to)
         return shed

    def get_search_result(self, station_from, station_to, time = None, select = None):
        station_from = station_from.replace(" ", "")
        station_to = station_to.replace(" ", "")
        time = time.replace(" ", "")
        if time == "None":
            time = None


        is_valid = self.validator.validate_data_from_search(station_from, station_to, time, select)
        if not is_valid:
            return None, None

        if time is not None:
            time = time.split(":")
            time = datetime.time(int(time[0]), int(time[1]))

        results = self.bd.get_scheduler(station_from, station_to, time)
        if results is None:
            return [], None
        results = self.formatter.trainlist_time_intervals(results, select)
        result = self.formatter.get_data_for_trainlist_template(results)
        select = self.formatter.get_data_for_trainlist_template_select(select)
        return result, select

    def get_train_info(self, number, departure_station):
        is_valid = self.validator.validate_param_from_traininfo(number, departure_station)
        if not is_valid:
            return None, None

        result = self.bd.get_info_from_train_number2(str(number), departure_station)
        if result is None:
            return None, None

        station_list = result[1]
        for i in range(len(station_list)):
            station_list[i] = self.bd.get_station_from_id(station_list[i])
        
        train_list, title = self.formatter.get_data_for_train_template(result)
        return train_list, title


    def get_nearest_station(self, geo, R = 5):
        is_valid = self.validator.validate_param_from_location(geo[0], geo[1])
        if not is_valid:
            return None, None

        YandexStation = YandexNearestLocations(geo[0], geo[1], projsettings.YA_API_KEY, R)
        list_stations = YandexStation.run()
        response = None
        img = None
        if len(list_stations) > 0:
            response = list_stations
            map = YandexMapShot(geo[0], geo[1], list_stations)
            img = map.run()
            
        return response, img

    def write_map_img(self, img):
        fname = str(hash(img)) + ".png"
        path = "static/img/%s" % fname
        with open(path ,"wb") as f:
            f.write(img)
        return path

    def get_map_info(self, lat, lon):
        geo = (float(lat), float(lon))
        stationlist, img = self.get_nearest_station(geo)

        img_path = self.write_map_img(img)
        stationlist = self.formatter.get_data_for_table_map(stationlist)
        return stationlist, img_path

    def auth_user(self, login, password):
        print(threading.get_ident())
        is_valid = self.validator.validate_login_pass(login)
        if not is_valid:
            return None
        usr_psw = self.bd.get_user(login)

        if len(usr_psw) != 1:
            return False, None
        usr_psw = usr_psw[0]
        if password == usr_psw[2]:
            return True, usr_psw[0]
        else:
            return False, None



    def get_times(self, line, start_station, stop_station, index_st = 0, step = 1):
        n = len(line)
        for train_i in range(index_st, n, step):
            train = line[train_i]
            m = len(train[2])
            time_start = train[3][0]
            for station_i in range(m):
                if train[2][station_i] == start_station:
                    time_start = train[3][station_i]
                    line[train_i].append(time_start)
                elif train[2][station_i] == stop_station:
                    train1 = self.__diff_times_in_seconds(time_start,train[3][station_i], True)
                    line[train_i].append(train1)
                    line[train_i].append(train[3][station_i])
                    break
        return None

    def start_thr(self, line, start_station, stop_station, count, rr = None):
        pool = []

        if rr is None:
            rr = [0] * count
        for i in range(count):
            thr = threading.Thread(target = self.get_times, args = (line,start_station,stop_station,i,count))
            time.sleep(rr[i])
            thr.start()
            pool.append(thr)

        for i in range(count):
            pool[i].join()


    def __diff_times_in_seconds(self, t1, t2, mod = False):
        h1, m1, s1 = t1.hour, t1.minute, t1.second
        h2, m2, s2 = t2.hour, t2.minute, t2.second
        t1_secs = s1 + 60 * (m1 + 60*h1)
        t2_secs = s2 + 60 * (m2 + 60*h2)

        res = ( t2_secs - t1_secs)
        if mod and res < 0:
            res += 86400
        return res

    def route_time(self, station1, station2, count, node = None):
        first_line = self.bd.get_scheduler(station1, node)
        second_line = self.bd.get_scheduler(node, station2)

        min_time = 86400
        result = None
        for train1 in first_line:
            for train2 in second_line:
                wait_time = self.__diff_times_in_seconds(train1[-1], train2[-3])
                if wait_time < 480:
                    continue
                time = train1[-2] + train2[-2] + wait_time
                if min_time > time:
                    min_time = time
                    result = (train1, train2)

        result = list(result)
        result.append(min_time)
        return result
