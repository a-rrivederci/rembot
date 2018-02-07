// Limit switch testing
//
// License is available in LICENSE
// @author eeshiken
// @since 02-FEB-2018
//04-FEB-2018, tony - implemented pin modes and ISC 

#define debug 0 // false
#define HORIZONTAL_INTERRUPT_PIN 2
#define LEFT_INTERRUPT_PIN 3 // Can only use 2 and 3 for Uno ISR
#define LED_PIN 13

void setup() {
    pinMode(LED_PIN, OUTPUT);
    pinMode(LEFT_INTERRUPT_PIN, INPUT_PULLUP);
    pinMode(HORIZONTAL_INTERRUPT_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(HORIZONTAL_INTERRUPT_PIN), stopVerticalMotors, RISING);
    attachInterrupt(digitalPinToInterrupt(LEFT_INTERRUPT_PIN), stopLeftMotor, RISING);
}

void stopHorizontalMotor()
{
    horizontal_stepper->stop();
    return;
}

void stopVerticalMotors()
{
    left_vertical_stepper->stop();
    right_vertical_stepper->stop();
    return;
}
