// Runs the three stepper motors, and the servo
// License is available in LICENSE
// @since 23-FEB-2018
// @version 0.1.0
// @authors Harsimranjeet Eeshiken


// Imports
#include <AccelStepper.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <Wire.h>
#include <Servo.h>

// Constants
// Program defines
#define VERBOSE
#define VERSION_MAJOR           (0)
#define VERSION_MINOR           (1)
#define VERSION_PATCH           (0)
#define FINE_SPEED              (1000)
#define MAX_SPEED               (1000)
#define ARM_TURN_TIME           (80)
#define STEP                    (1)
#define MAX_BUF                 (64)
// Hardware defines
#define BAUD_RATE               (9600)
#define ARM_PIN                 (10)
#define H_INTERRUPT_PIN         (2)
#define V_INTERRUPT_PIN         (3)

// Program variables
double X_ACCEL = 100.0;
double Y_ACCEL = 100.0;
byte LINE_COMPLETE = 0;         // whether the input line is complete
byte ARM_STATUS = 0;            // status of z-axis pen
byte FLAG = 0;                  // FLAG for motor reading
byte sofar = 0;                 // how much is in the buffer
char serial_buffer[MAX_BUF];    // where we store the message until we get ';'
int step;

// Will have value of 0 at corner (limit switch) and max at other end,
// units are in per step defined, 
// initialized with garbage value of -1, must call resetSteppers()!
struct Coordinates{
    float X = -1; 
    float Y = -1;
} global_coords;


// Adafruit MotorShield AFMS bottom - 0 and AFSM top - 1
Adafruit_MotorShield AFMS0(0x60); // default address, no jumpers
Adafruit_MotorShield AFMS1(0x61); // rightmost jumper closed

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
AccelStepper vStepper(vForwardStep, vBackwardStep);


// Program methods
void setup() {
    // Initialize serial    
    Serial.begin(BAUD_RATE);

    // Print out serial messages
    helpMessage();

    // Interrupt
    // pinMode(RIGHT_INTERRUPT_PIN, INPUT_PULLUP);
    // pinMode(HORIZONTAL_INTERRUPT_PIN, INPUT_PULLUP);
    // attachInterrupt(digitalPinToInterrupt(RIGHT_INTERRUPT_PIN), stopVerticalMotors, RISING);
    // attachInterrupt(digitalPinToInterrupt(HORIZONTAL_INTERRUPT_PIN), stopHorizontalMotor, RISING);

    // Start shileds
    AFMS0.begin();
    AFMS1.begin();

    // Begin program
    serialReady(); 
}

void loop() {
    // Depends of serialEvent to update LINE_COMPLETE
    if (LINE_COMPLETE) {
        Serial.println("S"); // return success message
        decodeMessage();
        // Get ready to receive more
        serialReady();
    }
}
