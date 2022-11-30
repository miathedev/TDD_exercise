import time
from datetime import datetime

import mock.GPIO as GPIO
from mock.RTC import RTC
from ParkingGarageError import ParkingGarageError


class ParkingGarage:
    # Pin number declarations
    INFRARED_PIN1 = 11
    INFRARED_PIN2 = 12
    INFRARED_PIN3 = 13
    RTC_PIN = 15
    SERVO_PIN = 16
    LED_PIN = 18

    GARAGE_DOOR_DEGREE_OPEN_DUTY_CYLE = (180 / 18) + 2
    GARAGE_DOOR_DEGREE_CLOSED_DUTY_CYLE = (0 / 18) + 2

    def __init__(self):
        """
        Constructor
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.INFRARED_PIN1, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN2, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN3, GPIO.IN)
        GPIO.setup(self.RTC_PIN, GPIO.IN)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        self.rtc = RTC(self.RTC_PIN)
        self.pwm = GPIO.PWM(self.SERVO_PIN, 50)
        self.pwm.start(0)

        #Mias additions
        self.garage_open = False #Keeps track if garage door open

    def check_occupancy(self, pin: int) -> bool:
        """
        Checks whether one of the infrared distance sensor detects something in front of it.
        :param pin: The data pin of the sensor that is being checked (e.g., INFRARED_PIN1).
        :return: True if the infrared sensor detects something, False otherwise.
        """
        return GPIO.input(pin) > 0

    def get_occupied_spots(self) -> int:
        """
        Calculates the number of occupied parking spots in the garage.
        :return: The number of occupied spots.
        """
        occupied = 0
        if GPIO.input(self.INFRARED_PIN1):
            occupied += 1
        if GPIO.input(self.INFRARED_PIN2):
            occupied += 1
        if GPIO.input(self.INFRARED_PIN3):
            occupied += 1

        return occupied

    def calculate_parking_fee(self, entry_time: str) -> float:
        """
        Uses the RTC to calculate the amount of money to be paid by the customer of the garage
        For each hour spent in the garage, there is a flat cost of 2.50 €;
        additionally, during the weekend (Saturday and Sunday)
        an additional 25% fee is applied to the total of the parking ticket.
        Even when customers do not exceed a full hour, they will still be charged 2.50 €.
        :param entry_time: A string in the format "hh:mm:ss" containing the entry time of a
        vehicle in the garage
        :return: The total amount to be paid by the customer
        """
        entry_time = time.strptime(entry_time, '%H:%M:%S')
        exit_time = time.strptime(RTC.get_current_time_string(), '%H:%M:%S')
        weekday = RTC.get_current_day()

        time_parked_hours = exit_time.tm_hour - entry_time.tm_hour
        time_parked_minutes = exit_time.tm_min - entry_time.tm_min

        if time_parked_minutes > 0:
            time_parked_hours += 1

        cost = time_parked_hours * 2.5
        if weekday not in ["SATURDAY", "SUNDAY"]:
            return cost
        else:
            return cost + cost * 0.25

    def open_garage_door(self) -> None:
        """
        Opens the garage door using the servo motor
        A motor angle of 180 degrees corresponds to a fully open door
        """
        if not self.garage_open:
            self.garage_open = True
            self.change_servo_angle(self.GARAGE_DOOR_DEGREE_OPEN_DUTY_CYLE)


    def close_garage_door(self) -> None:
        """
        Closes the garage door using the servo motor
        A motor angle of 0 degrees corresponds to a fully closed door
        """
        if self.garage_open:
            self.garage_open = False
            self.change_servo_angle(self.GARAGE_DOOR_DEGREE_CLOSED_DUTY_CYLE)

    def is_garage_door_open(self) -> bool:
        return self.garage_open
    def turn_light_on(self) -> None:
        """
        Turns on the smart lightbulb
        """
        pass

    def turn_light_off(self) -> None:
        """
        Turns off the smart lightbulb
        """
        pass

    def change_servo_angle(self, duty_cycle):
        """
        Changes the servo motor's angle by passing him the corresponding PWM duty cycle signal
        :param duty_cycle: the length of the duty cycle
        """
        GPIO.output(self.SERVO_PIN, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        GPIO.output(self.SERVO_PIN, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)
