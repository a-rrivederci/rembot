// Runs the three stepper motors, and the servo
// License is available in LICENSE
// @author eeshiken
// @since 27-JAN-2018
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
#define ARM_TURN_TIME 80
#define CLAW_TURN_TIME 140
#define STEP 50
// Hardware defines
#define BAUD_RATE 9600
#define ARM_PIN 10
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
char cmd;
int step;

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
    claw_servo.write(90); // No motion
}

void loop() {
}

void serialEvent() {
    switch(Serial.read()) {
        case 'U': // go up
            go_up();
            break;
        case 'J': // go down
            go_down();
            break;
        case 'H': // go left
            go_left();
            break;
        case 'K': // go right
            go_right();
            break;
        case 'W': // raise arm
            arm_raise();
            break;
        case 'S': // lower arm
            arm_lower();
            break;
        case 'A': // open claw
            claw_open();
            break;
        case 'D': // close claw
            claw_close();
            break;
        default:
            Serial.println("Not Recognized");
    }
    return;
}

// Custom methods
// Motor
void go_up() {
    step = STEP;
    lv_stepper.setMaxSpeed(MAX_SPEED);
    lv_stepper.setAcceleration(Y_ACCEL);
    lv_stepper.moveTo(lv_stepper.currentPosition() - step);

    rv_stepper.setMaxSpeed(MAX_SPEED);
    rv_stepper.setAcceleration(Y_ACCEL);
    rv_stepper.moveTo(lv_stepper.currentPosition() - step);

    #if VERBOSE == 1
    Serial.println("Going up ... ");
    #endif

    run_motors();

    return;
}

void go_down() {
    step = -1*STEP;
    lv_stepper.setMaxSpeed(MAX_SPEED);
    lv_stepper.setAcceleration(Y_ACCEL);
    lv_stepper.moveTo(lv_stepper.currentPosition() - step);

    rv_stepper.setMaxSpeed(MAX_SPEED);
    rv_stepper.setAcceleration(Y_ACCEL);
    rv_stepper.moveTo(lv_stepper.currentPosition() - step);

    #if VERBOSE == 1
    Serial.println("Going down ... ");
    #endif

    run_motors();

    return;
}

void go_left() {
    step = STEP;
    h_stepper.setMaxSpeed(MAX_SPEED);
    h_stepper.setAcceleration(X_ACCEL);
    h_stepper.moveTo(h_stepper.currentPosition() - step);

    #if VERBOSE == 1
    Serial.println("Going left ... ");
    #endif

    run_motors();

    return;
}

void go_right() {
    step = -1*STEP;
    h_stepper.setMaxSpeed(MAX_SPEED);
    h_stepper.setAcceleration(Y_ACCEL);
    h_stepper.moveTo(h_stepper.currentPosition() - step);

    #if VERBOSE == 1
    Serial.println("Going right ... ");
    #endif

    run_motors();

    return;
}

void run_motors() {
    bool flag = true;
    while(flag == true) {
        flag = false;
        if (h_stepper.distanceToGo() != 0) {
            #if VERBOSE == 1
            Serial.println("Running horizontal_stepper ... ");
            #endif
            h_stepper.run();
            flag = true;
        }
        if (lv_stepper.distanceToGo() != 0) {
            #if VERBOSE == 1
            Serial.println("Running left_vertical_stepper ... ");
            #endif
            lv_stepper.run();
            flag = true;
        }
        if (rv_stepper.distanceToGo() != 0) {
            #if VERBOSE == 1
            Serial.println("Running right_vertical_stepper ... ");
            #endif
            rv_stepper.run();
            flag = true;
        }

    }

    #if VERBOSE == 1
    Serial.println("End motor run\n");
    #endif

    return;
}

// Effector
void arm_raise() {
    // Check if arm is raised
    if (ARM_IS_RAISED != false) {
        #if VERBOSE == 1
        Serial.println("Arm is already raised\n");
        #endif

        return;
    }

    // Raise arm
    //Start turning anti-clockwise
    arm_servo.write(180);
    // Go on turning for the right duration
    delay(ARM_TURN_TIME);
    // Stop turning
    arm_servo.write(90);

    ARM_IS_RAISED = true;

    #if VERBOSE == 1
    Serial.println("Arm is raised\n");
    #endif

    return;
}

void arm_lower() {
    // Check if arm is already lowered
    if (ARM_IS_RAISED != true) {
        #if VERBOSE == 1
        Serial.println("Arm is already lowered\n");
        #endif

        return;
    }

    // Lower arm
    //Start turning clockwise
    arm_servo.write(0);
    // Go on turning for the right duration
    delay(ARM_TURN_TIME);
    // Stop turning
    arm_servo.write(90);

    ARM_IS_RAISED = false;

    #if VERBOSE == 1
    Serial.println("Arm is lowered\n");
    #endif

    return;
}

void claw_open() {
    // Check if claw is already open
    if (CLAW_IS_OPEN != false){
        #if VERBOSE == 1
        Serial.println("Claw is already open\n");
        #endif

        return;
    }

    // Open claw
    //Start turning anti-clockwise
    claw_servo.attach(CLAW_PIN);
    claw_servo.write(180);
    // Go on turning for the right duration
    delay(CLAW_TURN_TIME);
    // Stop turning
    //claw_servo.write(90);
    claw_servo.detach();

    CLAW_IS_OPEN = true;

    #if VERBOSE == 1
    Serial.println("Claw is open\n");
    #endif

    return;
}

void claw_close() {
    // Check if claw is aready closed
    if (CLAW_IS_OPEN != true) {
        #if VERBOSE == 1
        Serial.println("Claw is already closed\n");
        #endif

        return;
    }

    // Close claw
    // Start turning clockwise
    claw_servo.attach(CLAW_PIN);
    claw_servo.write(0);
    // Go on turning for the right duration
    delay(CLAW_TURN_TIME);
    // Stop turning
    //claw_servo.write(90);
    claw_servo.detach();

    CLAW_IS_OPEN = false;

    #if VERBOSE == 1
    Serial.println("Claw is closed\n");
    #endif

    return;
}
