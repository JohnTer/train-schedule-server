import datetime


class Formatter(object):
    def __init__(self):
        self.days = {1:'Пн',2:'Вт',4:'Ср',8:'Чт',16:'Пт',32:'Сб',64:'Вс'}
        self.sep = " "
        self.max_int_of_day = 64

    def get_days_of_week(self, day):
        try:
            day = int(day)
        except:
            raise TypeError("Invalid type of day!")
        if day < 0:
            return ""
        result = ""
        bit = 1
        while bit <= self.max_int_of_day:
            if bit & day:
                result += self.days[bit] + self.sep
            bit *= 2
        return result 

    def get_str_time_from_datetime(self, date):
        result = date.strftime("%H:%M")
        return result



    def gtshed(self, shed):
        days = {'пн': 1,'вт':2,'ср':4,'чт':8,'пт':16,'сб':32,'вс':64}
        result = 0
        shed = shed.lower().split()
        if 'пн' in shed:
            result |= days['пн']
        if 'вт' in shed:
            result |= days['вт']
        if 'ср' in shed:
            result |= days['ср']
        if 'чт' in shed:
            result |= days['чт']
        if 'пт' in shed:
            result |= days['пт']
        if 'сб' in shed:
            result |= days['сб']
        if 'вс' in shed:
            result |= days['вс']

        return result




    def get_data_for_trainlist_template(self, trainlist):
        result = []
        for train in trainlist:
            number = train[0]
            days = self.get_days_of_week(train[1])

            from_station = train[2][0]
            to_station = train[2][-1]

            from_time = train[3][0]
            to_time= train[3][-1]

            time = self.get_str_time_from_datetime(from_time) + " - " + self.get_str_time_from_datetime(to_time)
            title = "%d %s - %s" % (number, from_station, to_station)
            res = dict(title = title, time = time, days = days, id = number, station_from = from_station)
            result.append(res)
        return result

    def get_data_for_trainlist_template_select(self, select):
        result = [""] * 5
        result[int(select)] = "selected"
        return result


    def trainlist_time_intervals(self, trainlist, option):
        option = int(option)
        time1, time2 = None, None
        if option == 0:
            return trainlist
        elif option == 1:
            time1 = datetime.time(hour = 6)
            time2 = datetime.time(hour = 11, minute = 59)
        elif option == 2:
            time1 = datetime.time(hour = 12)
            time2 = datetime.time(hour = 17, minute = 59)
        elif option == 3:
            time1 = datetime.time(hour = 18)
            time2 = datetime.time(hour = 23, minute = 59)
        elif option == 4:
            time1 = datetime.time(hour = 0)
            time2 = datetime.time(hour = 5, minute = 59)

        n = len(trainlist)
        for i in range(n-1,-1,-1):
            if not (trainlist[i][3][0] >= time1 and trainlist[i][3][0] <= time2):
                del trainlist[i]
        return trainlist


    def get_data_for_train_template(self, train):
        station_list = []
        title = "%d %s - %s" % (train[0],train[1][0],train[1][-1])
        for i in range(len(train[1])):
            time = train[2][i]
            time = self.get_str_time_from_datetime(time)
            station = train[1][i]
            res = dict(time = time, station = station)
            station_list.append(res)
        return station_list, title

    def get_data_for_table_map(self, stationlist):
        result = []
        for i, station in enumerate(stationlist):
            res = dict(station = station[0], dist = station[1], id = i + 1)
            result.append(res)
        return result 

  
