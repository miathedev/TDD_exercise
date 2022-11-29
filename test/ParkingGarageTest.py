import unittest
from unittest.mock import patch

from ParkingGarage import ParkingGarage
from ParkingGarageError import ParkingGarageError

import mock.GPIO as GPIO
from mock.RTC import RTC


class ParkingGarageTest(unittest.TestCase):
    def setUp(self):
        self.parking_garage = ParkingGarage()
    @patch("mock.GPIO.input")
    def test_parking_garage_check_occupancy_true(self, mock_input):
        mock_input.return_value = 1023 #Any non zero value means, a car is detected
        for num in range(11, 14): #11,12,13
            occupancy = self.parking_garage.check_occupancy(num)
            self.assertTrue(occupancy)

    @patch("mock.GPIO.input")
    def test_parking_garage_check_occupancy_false(self, mock_input):
        mock_input.return_value = 0 #Zero value: nothing is detected in front of the sensor
        for num in range(11, 14):  # 11,12,13
            occupancy = self.parking_garage.check_occupancy(num)
            self.assertFalse(occupancy)

    @patch("mock.GPIO.input")
    def test_parking_garage_get_occupied_slots_2(self, mock_input):
        mock_input.side_effect = [255,255,0]
        spots = self.parking_garage.get_occupied_spots()
        self.assertEqual(2, spots)

    @patch("mock.GPIO.input")
    def test_parking_garage_get_occupied_slots_empty(self, mock_input):
        mock_input.side_effect = [0, 0, 0]
        spots = self.parking_garage.get_occupied_spots()
        self.assertEqual(0, spots)



