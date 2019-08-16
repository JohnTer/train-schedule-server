import unittest
from dataformatter.dataformatter import Formatter
from unittest.mock import patch

class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = Formatter()

    def test_get_days_of_week_invalid(self):
        day = "32"
        self.assertRaises(TypeError, self.formatter.get_days_of_week(day))

    def test_get_days_of_week_inset(self):
        day = 3
        result = 'Пн Вт ' 
        self.assertEqual(self.formatter.get_days_of_week(day), result)
        
    
    def test_get_days_of_week_outset(self):
        day = -5
        result = ''
        self.assertEqual(self.formatter.get_days_of_week(day), result)


    def test_get_days_of_week_border(self):
        day = 0
        result = ''
        self.assertEqual(self.formatter.get_days_of_week(day), result)

        day = 128
        result = ''
        self.assertEqual(self.formatter.get_days_of_week(day), result)

    def test_gtshed_inset(self):
        shed = 'Пн Вт'
        result = 3
        self.assertEqual(self.formatter.gtshed(shed), result)
    
        shed = 'Вт Ср Чт Пт Сб Вс'
        result = 126
        self.assertEqual(self.formatter.gtshed(shed), result)


    def test_gtshed_outset(self):
        shed = 'Пн1'
        result = 0
        self.assertEqual(self.formatter.gtshed(shed), result)
    

    def test_gtshed_border(self):    
        shed = 'Пн'
        result = 1
        self.assertEqual(self.formatter.gtshed(shed), result)
    
        shed = 'Пн Вт Ср Чт Пт Сб Вс'
        result = 127
        self.assertEqual(self.formatter.gtshed(shed), result)

if __name__ == "__main__":
    unittest.main(exit=False)
