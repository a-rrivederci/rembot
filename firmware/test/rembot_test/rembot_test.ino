// Runs the three stepper motors, and the servo
// License is available in LICENSE
// @author eeshiken
// @since 22-DEC-2017
// @version 2.0.0

// Imports
// For motor shield V2
#include <AccelStepper.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Wire.h>
// For servos
#include <Servo.h>

// Constants
#define VERBOSE 0 // false
#define VERSION_MAJOR 2
#define VERSION_MINOR 0
#define VERSION_PATCH 0
#define BAUD_RATE 9600

// Variables
// Flags
byte CONNECTED = 0; //false
// Program variables
char cmd;


void setup() {
    Serial.begin(BAUD_RATE);
    Serial.print("Rembot Uno v");
    Serial.print(VERSION_MAJOR);
    Serial.print(".");
    Serial.print(VERSION_MINOR);
    Serial.print(".");
    Serial.println(VERSION_PATCH);
}

void loop() {
  switch (CONNECTED) {
    case 0:
        if (Serial.available()) {
            cmd = Serial.read();
            switch(cmd) {
                case 'c': 
                    CONNECTED = 1;
                    Serial.println('C');
                    break;
            }
        }
        break;
    case 1:
        if (Serial.available()) {
            cmd = Serial.read();
            switch(cmd) {
                case 'k':
                    count_down();
                    break;
                case 'd':
                    CONNECTED = 0;
                    Serial.println('D');
                    break;
            }
        }
        break;
  } 
}
