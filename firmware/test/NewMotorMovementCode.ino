// Runs the three stepper motors, and the servo
// License is available in LICENSE
// @author Harsimranjeet 


/////////////////////////////////////////////////////////////////////////////////////////////////////
// This code implements the inbuilt accelstepper function library functions for movements, 
// a lot of code has been trimmed and it is simpler to understand as a results.
// This code assumes that we have vertical steppers connected to one pin on arduino (possible thing to do)
/////////////////////////////////////////////////////////////////////////////////////////////////////


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
#define STEP 50
// Hardware defines
#define BAUD_RATE 9600
#define HORIZONTAL_INTERRUPT_PIN 2
#define RIGHT_INTERRUPT_PIN 3 // Can only use 2 and 3 for Uno ISR

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
Adafruit_StepperMotor *vertical_stepper = AFMS1.getStepper(200, 1); 

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
void v_forwardstep() {
    vertical_stepper->onestep(FORWARD, DOUBLE);
    return;
}
void v_backwardstep() {
    vertical_stepper->onestep(BACKWARD, DOUBLE);
    return;
}

// Wrap in AccelStepper object
AccelStepper h_stepper(h_forwardstep, h_backwardstep);
AccelStepper v_stepper(lv_forwardstep, lv_backwardstep);

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

    // Interrupt
    // pinMode(RIGHT_INTERRUPT_PIN, INPUT_PULLUP);
    // pinMode(HORIZONTAL_INTERRUPT_PIN, INPUT_PULLUP);
    // attachInterrupt(digitalPinToInterrupt(RIGHT_INTERRUPT_PIN), stopVerticalMotors, RISING);
    // attachInterrupt(digitalPinToInterrupt(HORIZONTAL_INTERRUPT_PIN), stopHorizontalMotor, RISING);
}
// Custom methods
// Motor
void go_up() {
    step = STEP;
    v_stepper.setMaxSpeed(MAX_SPEED);
    v_stepper.setAcceleration(Y_ACCEL);
    v_stepper.moveTo(v_stepper.currentPosition() - step);
    
    #if VERBOSE == 1
    Serial.println("Going up ... ");
    #endif

    v_stepper.runToPosition();

    return;
}

void go_down() {
    step = -1*STEP;
    v_stepper.setMaxSpeed(MAX_SPEED);
    v_stepper.setAcceleration(Y_ACCEL);
    v_stepper.moveTo(v_stepper.currentPosition() - step);

    #if VERBOSE == 1
    Serial.println("Going down ... ");
    #endif

    v_stepper.runToPosition();

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

    h_stepper.runToPosition();

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

    h_stepper.runToPosition();

    return;
}





