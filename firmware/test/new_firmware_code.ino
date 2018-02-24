// Runs the three stepper motors, and the servo
// License is available in LICENSE
// @author Harsimranjeet 


/////////////////////////////////////////////////////////////////////////////////////////////////////
// This code implements the inbuilt accelstepper function library functions for movements, 
// a lot of code has been trimmed and it is simpler to understand as a results.
// This code assumes that we have vertical steppers connected to one pin on arduino (possible thing to do)
/////////////////////////////////////////////////////////////////////////////////////////////////////

struct Coordinate{
    int x = -1; //will have value of 0 at corner (limit switch) and max at other end, units are in per step defined, initialized with garbage value of -1, must call resetMotors()!
    int y = -1; //will have value of 0 at corner (limit switch) and max at other end, units are in per step defined, ,initialized with garbage value of -1, must call resetMotors()!
}
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
#define 
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
void hForwardStep() {
    horizontal_stepper->onestep(FORWARD, DOUBLE);
    return;
}
void hBackwardStep() {
    horizontal_stepper->onestep(BACKWARD, DOUBLE);
    return;
}

// Wrappers for the left_vertical_stepper
void vForwardStep() {
    vertical_stepper->onestep(FORWARD, DOUBLE);
    return;
}
void vBackwardStep() {
    vertical_stepper->onestep(BACKWARD, DOUBLE);
    return;
}

// Wrap in AccelStepper object
AccelStepper hStepper(hForwardStep, hBackwardStep);
AccelStepper vStepper(lv_forwardstep, lv_backwardstep);

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
void goUp() {
    step = STEP;
    vStepper.setMaxSpeed(MAX_SPEED);
    vStepper.setAcceleration(Y_ACCEL);
    vStepper.moveTo(vStepper.currentPosition() - step);
    
    #if VERBOSE == 1
    Serial.println("Going up ... ");
    #endif

    vStepper.runToPosition();

    Coordinate.y -= 1;

    return;
}

void goDown() {
    step = -1*STEP;
    vStepper.setMaxSpeed(MAX_SPEED);
    vStepper.setAcceleration(Y_ACCEL);
    vStepper.moveTo(vStepper.currentPosition() - step);

    #if VERBOSE == 1
    Serial.println("Going down ... ");
    #endif

    vStepper.runToPosition();

    Coordinate.y += 1;

    return;
}

void goLeft() {
    step = STEP;
    hStepper.setMaxSpeed(MAX_SPEED);
    hStepper.setAcceleration(X_ACCEL);
    hStepper.moveTo(hStepper.currentPosition() - step);

    #if VERBOSE == 1
    Serial.println("Going left ... ");
    #endif

    hStepper.runToPosition();

    Coordinate.x -= 1;
    return;
}

void goRight() {
    step = -1*STEP;
    hStepper.setMaxSpeed(MAX_SPEED);
    hStepper.setAcceleration(Y_ACCEL);
    hStepper.moveTo(hStepper.currentPosition() - step);

    #if VERBOSE == 1
    Serial.println("Going right ... ");
    #endif

    hStepper.runToPosition();

    Coordinate.x += 1;

    return;
}

void resetSteppers() {

    #if VERBOSE == 1
    Serial.println("Going to limit switches ... ");
    #endif

    for(int i = 0; i < 10000; i++)
        goUp();
    for(int i = 0; i < 2000; i++)
        goLeft();
    
    Coordinate.x = 0;
    Coordinate.y = 0;
    //step = STEP;
    //vStepper.setMaxSpeed(MAX_SPEED);
    //vStepper.setAcceleration(Y_ACCEL);
    //vStepper.moveTo(vStepper.currentPosition() - 10000000*step);

    //hStepper.setMaxSpeed(MAX_SPEED);
    //hStepper.setAcceleration(Y_ACCEL);
    //hStepper.moveTo(vStepper.currentPosition() + 10000000*step);

    //vStepper.runToPosition();
    //hStepper.runToPosition();

    return;
}

void findCorner() {

    #if VERBOSE == 1
    Serial.println("Finding corner of the page ... ");
    #endif

    for(int i = 0; i < 7500; i++)
        goDown();
    for(int i = 0; i < 500; i++)
        goRight();

    //step = STEP;
    //vStepper.setMaxSpeed(MAX_SPEED);
    //vStepper.setAcceleration(Y_ACCEL);
    //vStepper.moveTo(vStepper.currentPosition() + 7500*step);

    //hStepper.setMaxSpeed(MAX_SPEED);
    //hStepper.setAcceleration(Y_ACCEL);
    //hStepper.moveTo(vStepper.currentPosition() - 500*step);

    //vStepper.runToPosition();
    //hStepper.runToPosition();

    return;
}

/*void findEdgeAndStepDown() {

    #if VERBOSE == 1
    Serial.println("Going to the beginnig of the margin ... ");
    #endif
    
    goDown();

    for(int i = 0; i < 1000; i++)
        goLeft();
    
    //step = STEP;

    //vStepper.setMaxSpeed(MAX_SPEED);
    //vStepper.setAcceleration(Y_ACCEL);
    //vStepper.moveTo(vStepper.currentPosition() + step);

    //hStepper.setMaxSpeed(MAX_SPEED);
    //hStepper.setAcceleration(Y_ACCEL);
    //hStepper.moveTo(vStepper.currentPosition() + 50000*step);

    //hStepper.runToPosition();

    return;
}*/

void moveToCoordinate(int X, int Y){ //absolute not relative 
    if(Coordinate.x < X)
        while(Coordinate.x != X)
            goRight();
    else 
        while(Coordinate.x != X)
            goLeft();
    if(Coordinate.y < Y)
        while(Coordinate.y != Y)
            goDown();
    else 
        while(Coordinate.y != Y)
            goUp();
}




