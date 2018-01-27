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
#define VERBOSE 1 // true
#define VERSION_MAJOR 2
#define VERSION_MINOR 0
#define VERSION_PATCH 0
#define FINE_SPEED 1000
#define MAX_SPEED 1000
#define TURN_TIME 90
// Hardware defines
#define BAUD_RATE 9600
#define ARM_PIN 5
#define CLAW_PIN 9
#define INTERRUPT_PIN1 1
#define INTERRUPT_PIN2 2
#define INTERRUPT_PIN3 3


// Variables
// Objects
Servo arm_servo; // servo1
Servo claw_servo; //servo2

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

// Connect two steppers with 200 steps per revolution (1.8 degree)
// Connect to the bottom shield
Adafruit_StepperMotor *horizontal_stepper = AFMS0.getStepper(200, 2);

// Connect to the top shield
Adafruit_StepperMotor *left_vertical_stepper = AFMS1.getStepper(200, 1);
Adafruit_StepperMotor *right_vertical_stepper = AFMS1.getStepper(200, 2);

// Wrappers for the horizontal_stepper
void h_forwardstep() {
    horizontal_stepper->onestep(FORWARD, DOUBLE);
    return;
}
void h_backwardstep() {
    horizontal_stepper->onestep(BACKWARD, DOUBLE);
    return;
}

// Wrappers for the left_vertical_stepper
void lv_forwardstep() {
    left_vertical_stepper->onestep(FORWARD, DOUBLE);
    return;
}
void lv_backwardstep() {
    left_vertical_stepper->onestep(BACKWARD, DOUBLE);
    return;
}

// wrappers for the right_vertical_stepper
void rv_forwardstep() {
    right_vertical_stepper->onestep(FORWARD, DOUBLE);
    return;
}
void rv_backwardstep() {
    right_vertical_stepper->onestep(BACKWARD, DOUBLE);
    return;
}

// Wrap in AccelStepper object
AccelStepper h_stepper(h_forwardstep, h_backwardstep);
AccelStepper lv_stepper(lv_forwardstep, lv_backwardstep);
AccelStepper rv_stepper(rv_forwardstep, rv_backwardstep);

// Program methods
void setup() {
    Serial.begin(BAUD_RATE);

    Serial.print("Rembot Uno v");
    Serial.print(VERSION_MAJOR);
    Serial.print(".");
    Serial.print(VERSION_MINOR);
    Serial.print(".");
    Serial.println(VERSION_PATCH);

    // Start shileds
    AFMS0.begin();
    AFMS1.begin();

    // lv_stepper.setMaxSpeed(MAX_SPEED);
    // lv_stepper.setAcceleration(X_ACCEL);
    // lv_stepper.moveTo(100);
    
    // rv_stepper.setMaxSpeed(MAX_SPEED);
    // rv_stepper.setAcceleration(X_ACCEL);
    // rv_stepper.moveTo(100);
    // Attach Servos
    arm_servo.attach(ARM_PIN);
    claw_servo.attach(CLAW_PIN);

    arm_servo.write(90); // No motion
    //claw_servo.write(90); // No motion
}

void loop() {
    // // Change direction at the limits
    // if (lv_stepper.distanceToGo() == 0)
    //     lv_stepper.moveTo(-lv_stepper.currentPosition());
    // if (rv_stepper.distanceToGo() == 0)
    //     rv_stepper.moveTo(-rv_stepper.currentPosition());
    // lv_stepper.run();
    // rv_stepper.run();

    // Test raise_arm
    if (Serial.available()) {
        switch(Serial.read()) {
            case 'A': // open claw
                open_claw();
                break;
            case 'D': // close claw
                close_claw();
                break;
            default:
                Serial.println("Not Recognized");
        }
    }
}

// Input: degrees to raise the arm
void raise_arm(int deg) {
    // Check if arm is raised
    if (ARM_IS_RAISED != false) {
        return;
    }
    // Raise arm
    for (pos = 0; pos <= deg; pos += 1) { // goes from 0 degrees to 180 degrees in steps of 1 degree
        arm_servo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
    }
    ARM_IS_RAISED = true;

    return;
}

// Input: degrees to lower the arm
void lower_arm(int deg) {
    // Check if arm is already lowered
    if (ARM_IS_RAISED != true) {
        return;
    }
    // Lower arm
    for (pos = deg; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
        arm_servo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
    }
    ARM_IS_RAISED = false;

    return;
}

// Input: degrees to open claw
void close_claw() {
    // Check if claw is aready closed
    if (CLAW_IS_OPEN != true) {
        #if VERBOSE == 1
        Serial.println("Claw is already closed");
        #endif
        return;
        
    }
    // Close claw
    // Start turning clockwise
    claw_servo.write(0);
    // Go on turning for the right duration
    delay(TURN_TIME);
    // Stop turning
    claw_servo.write(90);

    CLAW_IS_OPEN = false;
    #if VERBOSE == 1
    Serial.println("Claw is closed");
    #endif

    return;
}

// Input: degrees to open claw
void open_claw() {
    // Check if claw is already open
    if (CLAW_IS_OPEN != false){
        #if VERBOSE == 1
        Serial.println("Claw is already open");
        #endif
        return;
    }
    // Open claw
    //Start turning anti-clockwise
    claw_servo.write(180);
    // Go on turning for the right duration
    delay(TURN_TIME);
    // Stop turning
    claw_servo.write(90);

    CLAW_IS_OPEN = true;
    #if VERBOSE == 1
    Serial.println("Claw is open");
    #endif

    return;
}