#!/usr/bin/env python3
import smbus
import time

registers = {'SERVO_1': 0x00,
             'ELEVATOR_THRUSTER': 0x10,
             'LEFT_THRUSTER': 0x11,
             'RIGHT_THRUSTER': 0x12}


class Arduino():
    def __init__(self, address=0x2f, bus_num=1):
        self.bus = smbus.SMBus(bus_num)  # 1 if Pi Zero or 3, 0 if Pi 2 or 1
        self.address = address

    def send(self, message, register=0x00, verify=False):
        '''Send message to Arduino.'''
        self.bus.write_i2c_block_data(self.address, register,
                                      [ord(char) for char in message])
        if verify:
            return_message = self.recv()
            print(('Register: {:#04x}\nMessage: {}\nResponse: {}'
                   ).format(register, message, return_message))
            return return_message
        time.sleep(0.01)

    def recv(self):
        message_bytes = self.bus.read_i2c_block_data(self.address, 0x00)
        message_parts = [chr(byte) for byte in message_bytes]
        return ''.join(message_parts).strip()


if __name__ == '__main__':
    ard = Arduino()
    while True:
        print('Which register would you like to talk to?')
        pad_size = len(max(registers, key=len)) + 5
        for key, val in registers.items():
            print('\t{:<{padding}}{:#04x}'.format(key, val, padding=pad_size))
        register = int(input('Enter a register: '), 16)
        message = input('Enter a message to send: ')
        ard.send(message, register=register, verify=True)
        print()
