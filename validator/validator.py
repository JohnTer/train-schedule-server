class Validator(object):
    def __init__(self):
        russian_alphabet = [chr(i) for i in range(ord('А'),ord('я')+1)] + ['ё', 'Ё',' ']
        digits = set("0123456789")
        spec_symbols = ['-']
        self.dictionary = set(russian_alphabet + spec_symbols)
        self.dictionary = self.dictionary.union(digits)

        self.select_type = set("01234")


        russian_alphabet = [chr(i) for i in range(ord('A'),ord('z')+1)] 
        self.login_dictionary = set(russian_alphabet)
        self.login_dictionary = self.login_dictionary.union(digits)

    def validate_word_by_white_list(self, parameter):
        if len(parameter) == 0:
            return False

        is_valid = True
        for ch in parameter:
            if ch not in self.dictionary:
                is_valid = False
                break
        return is_valid

    def is_number(self, n):
        try:
            int(n)   # Type-casting the string to `float`.
        except ValueError:
            return False
        return True

    def validate_time(self, parameter):
        if parameter is None:
            return True
        if parameter.find(":") == -1:
            return False


        hour_min = parameter.split(":")
        if len(hour_min) != 2:
            return False
        # hour check
        if len(hour_min[0]) > 2 or not self.is_number(hour_min[0]):
            return False
        if int(hour_min[0]) >= 24 or int(hour_min[0]) < 0:
            return False
        # min check
        if len(hour_min[1]) > 2 or not self.is_number(hour_min[1]):
            return False
        if int(hour_min[1]) > 59 or int(hour_min[1]) < 0:
            return False

        return True

    def validate_select(self, select):

        return select in self.select_type

    def validate_data_from_search(self, from_station, to_station, time, select):
        is_valid = True
        is_valid &= self.validate_word_by_white_list(from_station)
        if not is_valid:
            return False

        is_valid &= self.validate_word_by_white_list(to_station)
        if not is_valid:
            return False

        is_valid &= self.validate_time(time)
        if not is_valid:
            return False

        is_valid &= self.validate_select(select)
        if not is_valid:
            return False
        
        return is_valid

    def validate_param_from_traininfo(self, number, station):
        is_valid = True
        is_valid &= self.validate_word_by_white_list(station)
        if not is_valid:
            return False
        is_valid &= self.is_number(number)
        return is_valid

    def validate_param_from_location(self, lat, lon):
        try:
            lat = float(lat)
            lon = float(lon)
        except:
            return False
        
        if not (-90 < lat < 90):
            return False
        if not (-180 < lon < 180):
            return False
        return True

    def validate_login_pass(self, login):
        if len(login) == 0:
            return False

        is_valid = True
        for ch in login:
            if ch not in self.login_dictionary:
                is_valid = False
                break
        return is_valid


