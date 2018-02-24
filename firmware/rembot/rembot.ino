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
#define VERSION_MAJOR               (0)
#define VERSION_MINOR               (1)
#define VERSION_PATCH               (0)
#define FINE_SPEED                  (1000)
#define MAX_SPEED                   (1000)
#define ARM_TURN_TIME               (80)
#define CLAW_TURN_TIME              (140)
#define STEP                        (1)
#define MAX_BUF                     (64)
// Hardware defines
#define BAUD_RATE                   (9600)
#define ARM_PIN                     (10)
#define CLAW_PIN                    (9)
#define HORIZONTAL_INTERRUPT_PIN    (2)
#define RIGHT_INTERRUPT_PIN         (3)

// Program variables
double X_ACCEL = 100.0;
double Y_ACCEL = 100.0;
char cmd;
int step;
char serial_buffer[MAX_BUF];    // where we store the message until we get a 
byte sofar = 0;                 // how much is in the buffer
byte line_complete = 0;         // whether the input line is complete

// Will have value of 0 at corner (limit switch) and max at other end,
// units are in per step defined, 
// initialized with garbage value of -1, must call resetSteppers()!
struct Coordinates{
    int x = -1; 
    int y = -1;
} global_coords;


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
AccelStepper v_stepper(v_forwardstep, v_backwardstep);


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
    // Depends of serialEvent to update line_complete
    if (line_complete) {
        Serial.println("S"); // print success message

        #ifdef VERBOSE
        Serial.println(serial_buffer);
        #endif

        decodeMessage();
        // Get ready to receive more
        serialReady();
    }
}
