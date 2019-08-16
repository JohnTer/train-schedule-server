import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class WebTest():
    def __init__(self):
        self.driver = webdriver.Firefox()

    def test_auth(self, login, password):
        self.driver.get("http://localhost:5000/")
        lg = self.driver.find_element_by_name("login")
        psw = self.driver.find_element_by_name("password")

        lg.send_keys(login)
        psw.send_keys(password)
        psw.send_keys(Keys.RETURN)

        time.sleep(2)
        return self.driver.page_source

    def get_trainlist(self, from_station_text, to_station_text, time_station_text = ""):
        self.test_auth("test", "test")
        from_station = self.driver.find_element_by_id("from_station")
        to_station = self.driver.find_element_by_id("to_station")
        time_station = self.driver.find_element_by_id("time_station")

        from_station.send_keys(from_station_text)
        to_station.send_keys(to_station_text)
        time_station.send_keys(time_station_text)

        time_station.send_keys(Keys.RETURN)

        self.driver.find_element_by_tag_name("button").click()

        time.sleep(2)
        return self.driver.page_source

    def get_trainlist_select(self, from_station_text, to_station_text, time_station_text = "", select = 0):
        self.get_trainlist(from_station_text, to_station_text, time_station_text)

        idtag = "key%d" % select
        self.driver.find_element_by_id(idtag).click()

        time.sleep(2)
        return self.driver.page_source

    def __del__(self):
        self.driver.close()



class BLTest(unittest.TestCase):
    def setUp(self):
        self.webtest = WebTest()


    def test_auth_denied(self):
        html = self.webtest.test_auth("some", "thing")
        result = "Время" in html
        self.assertFalse(result)

    def test_auth_success(self):
        html = self.webtest.test_auth("test", "test")
        result = "Поиск" in html
        self.assertTrue(result) 
    
    def test_search_success_no_time(self):
        html = self.webtest.get_trainlist("Горенки", "Москва")
        count = html.count("""<h5 class="color--asphalt">""")
        self.assertEqual(count, 15)

    def test_search_fail_no_time(self):
        html = self.webtest.get_trainlist("Горенки", "Москва", "4:00")
        result = "Четыреста четыре" in html
        self.assertTrue(result)


    def test_search_success_with_time(self):
        html = self.webtest.get_trainlist("Горенки", "Москва", "7:40")
        count = html.count("""<h5 class="color--asphalt">""")
        self.assertEqual(count, 1)

    def test_search_success_select(self):
        html = self.webtest.get_trainlist_select("Балашиха", "Москва", select = 1)
        count = html.count("""<h5 class="color--asphalt">""")
        self.assertEqual(count, 5)

    def tearDown(self):
        del self.webtest



if __name__ == "__main__":
    unittest.main(exit=False)