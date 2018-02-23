/**
  Runs the three stepper motors, and the servo
  License is available in LICENSE
  @author catilin refayet eeshiken
  @since 22-DEC-2017
**/

#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Servo.h>

#define SERVO_PIN 5
#define CLAW_PIN 9
#define INTERRUPT_PIN1 1
#define INTERRUPT_PIN2 2
#define INTERRUPT_PIN3 3
#define BAUD_RATE 115200
#define FINE_SPEED 1000
#define MAX_SPEED 1000

Servo servo1;
Servo claw_servo;
bool ARM_IS_RAISED = false;
bool CLAW_IS_OPEN = false;
double X_ACCEL = 100.0;
double Y_ACCEL = 100.0;

int pos = 0;

Adafruit_MotorShield AFMStop(0x61); // Rightmost jumper closed
Adafruit_MotorShield AFMSbot(0x60); // Default address, no jumpers

// Connect two steppers with 200 steps per revolution (1.8 degree)
// to the top shield
Adafruit_StepperMotor *myStepper3 = AFMStop.getStepper(200, 2);

// Connect to the bottom shield
Adafruit_StepperMotor *myStepper2 = AFMSbot.getStepper(200, 2);
Adafruit_StepperMotor *myStepper1 = AFMSbot.getStepper(200, 1);

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// wrappers for the first motor!
void forwardstep1() {
    myStepper1->onestep(FORWARD, DOUBLE);
    return;
}
void backwardstep1() {
    myStepper1->onestep(BACKWARD, DOUBLE);
    return;
}

// wrappers for the second motor!
void forwardstep2() {
    myStepper2->onestep(FORWARD, DOUBLE);
    return;
}
void backwardstep2() {
    myStepper2->onestep(BACKWARD, DOUBLE);
    return;
}

// wrappers for the third motor!
void forwardstep3() {
    myStepper3->onestep(FORWARD, DOUBLE);
    return;
}
void backwardstep3() {
    myStepper3->onestep(BACKWARD, DOUBLE);
    return;
}

// Now we'll wrap the 3 steppers in an AccelStepper object
AccelStepper stepper1(forwardstep1, backwardstep1);
AccelStepper stepper2(forwardstep2, backwardstep2);
AccelStepper stepper3(forwardstep3, backwardstep3);

void setup() {
    Serial.begin(BAUD_RATE);

    AFMSbot.begin(); // Start the bottom shield
    AFMStop.begin(); // Start the top shield

    servo1.attach(SERVO_PIN);
    claw_servo.attach(CLAW_PIN);
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

void run_motors() {
    bool flag = true;
    while(flag == true) {
        flag = false;
        if (stepper1.distanceToGo() != 0) {
            stepper1.run();
            flag = true;
        }
        if (stepper2.distanceToGo() != 0) {
            stepper2.run();
            flag = true;
        }
        if (stepper3.distanceToGo() != 0) {
            stepper3.run();
            flag = true;
        }

    }
    return;
}

// Motor 3 should be the y direction
// Inputs: initial and final x coordinate, initial and final y coordinate // dir = 0 = CW //dir = 1 = ACW
void move_steppers(int pos_x1,int pos_x2,int pos_y1, int pos_y2,int dirX,int dirY, int custom_speed) {
    int mult = 1;
    int deg_x = mult*(pos_x2 - pos_x1);
    int deg_y = mult*(pos_y2 - pos_y1);

    if (dirX = 1) {
        stepper1.setMaxSpeed(custom_speed);
        stepper1.setAcceleration(X_ACCEL);
        stepper1.moveTo(-stepper1.currentPosition()-deg_x);

        stepper2.setMaxSpeed(custom_speed);
        stepper2.setAcceleration(X_ACCEL);
        stepper2.moveTo(-stepper2.currentPosition()-deg_x);
    }
    if (dirX = 0) {
        stepper1.setMaxSpeed(custom_speed);
        stepper1.setAcceleration(X_ACCEL);
        stepper1.moveTo(-stepper1.currentPosition()- deg_x);

        stepper2.setMaxSpeed(custom_speed);
        stepper2.setAcceleration(X_ACCEL);
        stepper2.moveTo(-stepper2.currentPosition()-deg_x);
    }
    if (dirY = 1) {
        stepper3.setMaxSpeed(custom_speed);
        stepper3.setAcceleration(Y_ACCEL);
        stepper3.moveTo(-stepper3.currentPosition()-deg_y);
    }
    if (dirY = 0) {
        stepper3.setMaxSpeed(custom_speed);
        stepper3.setAcceleration(Y_ACCEL);
        stepper3.moveTo(-stepper3.currentPosition()-deg_y);
    }

    return;
}

// Resets motors to initial position
void reset() {
    stepper1.setMaxSpeed(MAX_SPEED);
    stepper1.setAcceleration(X_ACCEL);
    stepper1.moveTo(-stepper1.currentPosition()-10);

    stepper2.setMaxSpeed(MAX_SPEED);
    stepper2.setAcceleration(X_ACCEL);
    stepper2.moveTo(-stepper2.currentPosition()-10);

    stepper3.setMaxSpeed(MAX_SPEED);
    stepper3.setAcceleration(Y_ACCEL);
    stepper3.moveTo(-stepper3.currentPosition()-10);

    bool flag = true;

    // Poll the switch
    while(flag == true) {
        flag = false;

        if ((stepper1.distanceToGo() != 0) and (digitalRead(INTERRUPT_PIN1)!=true)) {
            stepper1.run();
            flag = true;
        }
        if ((stepper2.distanceToGo() != 0) and (digitalRead(INTERRUPT_PIN2)!=true)) {
            stepper2.run();
            flag = true;
        }
        if ((stepper3.distanceToGo() != 0) and (digitalRead(INTERRUPT_PIN3)!=true)) {
            stepper3.run();
            flag = true;
        }
    }

    return;
}

void loop() {
    Serial.println("Starting Loop");

    // Move from initial coordinate of (0,0) to a coordinate of (360,360)
    move_steppers(0,100,0,300,1,1,MAX_SPEED);
    move_steppers(0,-500,0,300,1,0,MAX_SPEED);

    run_motors();
    Serial.println("Run Completed");

    delay(500);
    Serial.println("Running other way");

    // Serial.println("Raising Arm");
    // raise_arm(10);
    // Serial.println("Lowering Arm");
    // lower_arm(10);
    // Serial.println("Open Claw");
    // open_claw(10);
    // Serial.println("Close Claw");
    // close_claw(10);
    // reset();
}

// Input: degrees to raise the arm
void raise_arm(int deg) {
    if (ARM_IS_RAISED != false)
    return;
    for (pos = 0; pos <= deg; pos += 1) { // goes from 0 degrees to 180 degrees in steps of 1 degree
    servo1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
    }
    ARM_IS_RAISED = true;

    return;
}

// Input: degrees to lower the arm
void lower_arm(int deg) {
    if (ARM_IS_RAISED != true)
    return;
    for (pos = deg; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    servo1.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
    }
    ARM_IS_RAISED = false;

    return;
}

// Input: degrees to lower the arm
void close_claw(int deg) {
    if (CLAW_IS_OPEN != true) {
        return;
    }
    for (pos = deg; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
        claw_servo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
    }
    CLAW_IS_OPEN = false;

    return;
}

// Input: degrees to raise the arm
void open_claw(int deg) {
    if (CLAW_IS_OPEN != false){
        return;
    }

    for (pos = 0; pos <= deg; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        claw_servo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
    }
    CLAW_IS_OPEN = true;

    return;
}
