// Runs the three stepper motors, and the servo
// License is available in LICENSE
// @author eeshiken
// @since 22-DEC-2017
// @version 2.0.0

// Imports
#include <AccelStepper.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Wire.h>
#include <Servo.h>


// Constants
// Program defines
#define VERBOSE 0 // false
#define VERSION_MAJOR 2
#define VERSION_MINOR 0
#define VERSION_PATCH 0
#define FINE_SPEED 1000
#define MAX_SPEED 1000
// Hardware defines
#define BAUD_RATE 115200
#define ARM_PIN 5
#define CLAW_PIN 9
#define INTERRUPT_PIN1 1
#define INTERRUPT_PIN2 2
#define INTERRUPT_PIN3 3


// Variables
// Objects
Servo arm_servo;
Servo claw_servo;

// Flags
byte CONNECTED = 0; //false
byte ARM_IS_RAISED = 0; // false;
byte CLAW_IS_OPEN = 0; // false;

// Program variables
double X_ACCEL = 100.0;
double Y_ACCEL = 100.0;
int pos = 0;
char cmd;

// Adafruit MotorShield AFMS bottom - 0 and AFSM top - 1
Adafruit_MotorShield AFMS0(0x60); // Default address, no jumpers
Adafruit_MotorShield AFMS1(0x61); // Rightmost jumper closed

// Program methods
void setup() {
    Serial.begin(BAUD_RATE);

    Serial.print("Rembot Uno v");
    Serial.print(VERSION_MAJOR);
    Serial.print(".");
    Serial.print(VERSION_MINOR);
    Serial.print(".");
    Serial.println(VERSION_PATCH);

    // Start boards
    AFMS0.begin();
    AFMS1.begin();

    // Attach pins
    arm_servo.attach(ARM_PIN);
    claw_servo.attach(CLAW_PIN);
}

void loop() {
}
