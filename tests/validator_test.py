import unittest
from validator.validator import Validator
from unittest.mock import patch

class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()

    def test_validate_time_validate_inset(self):
        time = "23:00"
        self.assertTrue(self.validator.validate_time(time))

    def test_validate_time_validate_outset_hour(self):
        time = "24:00"
        self.assertFalse(self.validator.validate_time(time))

    def test_validate_time_validate_outset_min(self):
        time = "22:60"
        self.assertFalse(self.validator.validate_time(time))

    def test_validate_time_validate_invalid_min(self):
        time = "21:1M"
        self.assertFalse(self.validator.validate_time(time))


    def test_validate_time_validate_invalid_hour(self):
        time = "2M:11"
        self.assertFalse(self.validator.validate_time(time))

    def test_validate_time_validate_invalid(self):
        time = "21:21:A"
        self.assertFalse(self.validator.validate_time(time))

if __name__ == "__main__":
    unittest.main(exit=False)
