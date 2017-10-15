#include <Wire.h>
#include <Servo.h>
#include "Thruster.h"

// The i2c address of the Arduino
#define SLAVE_ADDRESS 0x2f

// Servo Pin
const int servoPin = 2;

// Pins used for Elevator Thruster
const int pwmElevatorThruster = 3;
const int dirElevatorThruster = 7;

// Pins used for Left Thrusters
const int pwmLeftThruster = 5;
const int dirLeftThruster = 4;

// Pins used for Right Thrusters
const int pwmRightThruster = 6;
const int dirRightThruster = 8;

// Create register and objects for servo1 (This is here as an example for moving servos)
#define SERVO_1 0x00
Servo servo1;
int servo1loc = 90;  // This is the starting position for the servo

// Create register and object for elevatorThruster
#define ELEVATOR_THRUSTER 0x10
Thruster elevatorThruster = Thruster(pwmElevatorThruster, dirElevatorThruster);

// Create register and object for leftThruster
#define LEFT_THRUSTER 0x11
Thruster leftThruster = Thruster(pwmLeftThruster, dirLeftThruster);

// Create register and object for rightThruster
#define RIGHT_THRUSTER 0x12
Thruster rightThruster = Thruster(pwmRightThruster, dirRightThruster);

// These variables keep track of which messages were sent and to whom
byte recentMessageRegister;
String recentMessage;

void setup() {
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(recvMessage);
  Wire.onRequest(sendMessage);
  Serial.begin(9600);
  servo1.attach(servoPin);
}

void loop() {
  servo1.write(servo1loc);
  delay(100);
}

void recvMessage(int byteLength) {
  // Single byte messages contain no message
  if (byteLength <= 1) return;
  
  byte messageRegister = Wire.read();  // First byte sent is a register
  recentMessageRegister = messageRegister;
  String message;
  while (Wire.available())  // The remaining bytes are the message
    message += (char)Wire.read();
  recentMessage = message;

  switch (messageRegister) {
    case SERVO_1:
      servo1loc = message.toInt();
      if (servo1loc > 180) {
        servo1loc = 180;
      } else if (servo1loc < 0) {
        servo1loc = 0;
      }
      break;
    case ELEVATOR_THRUSTER:
      elevatorThruster.setFromMessage(message);
      break;
    case LEFT_THRUSTER:
      leftThruster.setFromMessage(message);
      break;
    case RIGHT_THRUSTER:
      rightThruster.setFromMessage(message);
      break;
    default:
      break;
  }
  
  Serial.print("Value: ");
  Serial.println(message);
  Serial.print("Message register: ");
  Serial.println(messageRegister, HEX);
  Serial.println();
}

void sendMessage() {
  // We can only send 32 bytes at a time
  int padStart = 0;
  String message;
  switch (recentMessageRegister) {
    case SERVO_1:
      message += "Servo 1 Position is: ";
      message += servo1loc;
      padStart = message.length();
      Wire.write(message.c_str());
      break;
    case ELEVATOR_THRUSTER:
      message = "Elevator speed=";
      message += elevatorThruster.getSpeed();
      message += ", dir=";
      message += elevatorThruster.getDirection();
      padStart = message.length();
      Wire.write(message.c_str());
      break;
    case LEFT_THRUSTER:
      message = "Left Thruster speed=";
      message += leftThruster.getSpeed();
      message += ", dir=";
      message += leftThruster.getDirection();
      padStart = message.length();
      Wire.write(message.c_str());
      break;
    case RIGHT_THRUSTER:
      message = "Right Thruster speed=";
      message += rightThruster.getSpeed();
      message += ", dir=";
      message += rightThruster.getDirection();
      padStart = message.length();
      Wire.write(message.c_str());
      break;
    default:
      break;
  }

  // Fill the remaining bytes with spaces
  for (int i = padStart; i < 32; i++)
    Wire.write(' ');
}
