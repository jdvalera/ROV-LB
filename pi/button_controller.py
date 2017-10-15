#!/usr/bin/env python3
from i2c_master import Arduino, registers
import RPi.GPIO as GPIO
import time

SPEED_PIN = 17
ROTATE_LEFT_PIN = 27
ROTATE_RIGHT_PIN = 22
FORWARD_PIN = 5
REVERSE_PIN = 6
ASCEND_PIN = 23
DESCEND_PIN = 24


def rotate_left(channel):
    while GPIO.input(channel) is False:
        if GPIO.input(SPEED_PIN) is False:
            ard.send('255', register=registers['RIGHT_THRUSTER'])
            ard.send('-255', register=registers['LEFT_THRUSTER'])
        else:
            ard.send('10', register=registers['RIGHT_THRUSTER'])
            ard.send('-10', register=registers['LEFT_THURSTER'])
        time.sleep(0.1)
    ard.send('0', register=registers['RIGHT_THRUSTER'])
    ard.send('0', register=registers['LEFT_THRUSTER'])


def rotate_right(channel):
    while GPIO.input(channel) is False:
        if GPIO.input(SPEED_PIN) is False:
            ard.send('-255', register=registers['RIGHT_THRUSTER'])
            ard.send('255', register=registers['LEFT_THRUSTER'])
        else:
            ard.send('-10', register=registers['RIGHT_THRUSTER'])
            ard.send('10', register=registers['LEFT_THRUSTER'])
        time.sleep(0.1)
    ard.send('0', register=registers['RIGHT_THRUSTER'])
    ard.send('0', register=registers['LEFT_THRUSTER'])


def move_forward(channel):
    while GPIO.input(channel) is False:
        if GPIO.input(SPEED_PIN) is False:
            ard.send('255', register=registers['RIGHT_THRUSTER'])
            ard.send('255', register=registers['LEFT_THRUSTER'])
        else:
            ard.send('10', register=registers['RIGHT_THRUSTER'])
            ard.send('10', register=registers['LEFT_THRUSTER'])
        time.sleep(0.1)
    ard.send('0', register=registers['RIGHT_THRUSTER'])
    ard.send('0', register=registers['LEFT_THRUSTER'])


def move_reverse(channel):
    while GPIO.input(channel) is False:
        if GPIO.input(SPEED_PIN) is False:
            ard.send('-255', register=registers['RIGHT_THRUSTER'])
            ard.send('-255', register=registers['LEFT_THRUSTER'])
        else:
            ard.send('-10', register=registers['RIGHT_THRUSTER'])
            ard.send('-10', register=registers['LEFT_THRUSTER'])
        time.sleep(0.1)
    ard.send('0', register=registers['RIGHT_THRUSTER'])
    ard.send('0', register=registers['LEFT_THRUSTER'])


def descend(channel):
    while GPIO.input(channel) is False:
        if GPIO.input(SPEED_PIN) is False:
            ard.send('-255', register=registers['ELEVATOR_THRUSTER'])
        else:
            ard.send('-10', register=registers['ELEVATOR_THRUSTER'])
        time.sleep(0.1)
    ard.send('0', register=registers['ELEVATOR_THRUSTER'])


def ascend(channel):
    while GPIO.input(channel) is False:
        if GPIO.input(SPEED_PIN) is False:
            ard.send('255', register=registers['ELEVATOR_THRUSTER'])
        else:
            ard.send('10', register=registers['ELEVATOR_THRUSTER'])
        time.sleep(0.1)
    ard.send('0', register=registers['ELEVATOR_THRUSTER'])


if __name__ == '__main__':
    ard = Arduino()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SPEED_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ROTATE_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ROTATE_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(FORWARD_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(REVERSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ASCEND_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DESCEND_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(ROTATE_LEFT_PIN, GPIO.FALLING,
                          callback=rotate_left, bouncetime=200)
    GPIO.add_event_detect(ROTATE_RIGHT_PIN, GPIO.FALLING,
                          callback=rotate_right, bouncetime=200)
    GPIO.add_event_detect(FORWARD_PIN, GPIO.FALLING,
                          callback=move_forward, bouncetime=200)
    GPIO.add_event_detect(REVERSE_PIN, GPIO.FALLING,
                          callback=move_reverse, bouncetime=200)
    GPIO.add_event_detect(ASCEND_PIN, GPIO.FALLING,
                          callback=ascend, bouncetime=200)
    GPIO.add_event_detect(DESCEND_PIN, GPIO.FALLING,
                          callback=descend, bouncetime=200)
    while True:
        time.sleep(1)
