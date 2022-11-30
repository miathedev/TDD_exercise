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
        mock_input.return_value = 1023  # Any non zero value means, a car is detected
        for num in range(11, 14):  # 11,12,13
            occupancy = self.parking_garage.check_occupancy(num)
            self.assertTrue(occupancy)

    @patch("mock.GPIO.input")
    def test_parking_garage_check_occupancy_false(self, mock_input):
        mock_input.return_value = 0  # Zero value: nothing is detected in front of the sensor
        for num in range(11, 14):  # 11,12,13
            occupancy = self.parking_garage.check_occupancy(num)
            self.assertFalse(occupancy)

    @patch("mock.GPIO.input")
    def test_parking_garage_get_occupied_slots_2(self, mock_input):
        mock_input.side_effect = [255, 255, 0]
        spots = self.parking_garage.get_occupied_spots()
        self.assertEqual(2, spots)

    @patch("mock.GPIO.input")
    def test_parking_garage_get_occupied_slots_empty(self, mock_input):
        mock_input.side_effect = [0, 0, 0]
        spots = self.parking_garage.get_occupied_spots()
        self.assertEqual(0, spots)

    @patch.object(RTC, "get_current_time_string")
    @patch.object(RTC, "get_current_day")
    def test_parking_garage_get_parking_fee_example_1(self, mock_rtc_day, mock_rtc_time):
        mock_rtc_time.return_value = "15:24:54"  # exit_time
        mock_rtc_day.return_value = "MONDAY"
        entry_time = "12:30:15"

        fee = self.parking_garage.calculate_parking_fee(entry_time)
        self.assertEqual(7.5, fee)

    @patch.object(RTC, "get_current_time_string")
    @patch.object(RTC, "get_current_day")
    def test_parking_garage_get_parking_fee_example_2(self, mock_rtc_day, mock_rtc_time):
        mock_rtc_time.return_value = "18:12:28"  # exit_time
        mock_rtc_day.return_value = "SATURDAY"
        entry_time = "10:15:08"

        fee = self.parking_garage.calculate_parking_fee(entry_time)
        self.assertEqual(25.0, fee)

    def test_parking_garage_close_open_door(self):
        # NOTE: I wanted to actually mock the call of pwm.ChangeDutyCycle to run another function,
        # so that im able to check if the correct DUTY Cycle has been set. But i dont know how :/

        # Default closed, closing again - should be still closed
        self.assertFalse(self.parking_garage.is_garage_door_open())
        self.parking_garage.close_garage_door()
        self.assertFalse(self.parking_garage.is_garage_door_open())

        # Open garage
        self.parking_garage.open_garage_door()
        self.assertTrue(self.parking_garage.is_garage_door_open())

        # Open garage again, should still be open
        self.parking_garage.open_garage_door()
        self.assertTrue(self.parking_garage.is_garage_door_open())

        # Close garage
        self.parking_garage.close_garage_door()
        self.assertFalse(self.parking_garage.is_garage_door_open())

    def test_parking_garage_light(self):
        # Light is default off
        self.assertFalse(self.parking_garage.is_light_on())

        # Even after putting the light off, if its off, it should be still off
        self.parking_garage.turn_light_off()
        self.assertFalse(self.parking_garage.is_light_on())

        # Turn light on
        self.parking_garage.turn_light_on()
        self.assertTrue(self.parking_garage.is_light_on())

        # Even after turning the light on, it was on, it should be still on
        self.parking_garage.turn_light_on()
        self.assertTrue(self.parking_garage.is_light_on())

        # Turn light off
        self.parking_garage.turn_light_off()
        self.assertFalse(self.parking_garage.is_light_on())
