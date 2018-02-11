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
    Serial.begin(9600); // set the baud rate
    Serial.println("Ready"); // print "Ready" once
    pinMode(LED_PIN, OUTPUT);
    pinMode(LEFT_INTERRUPT_PIN, INPUT_PULLUP);
    pinMode(HORIZONTAL_INTERRUPT_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(HORIZONTAL_INTERRUPT_PIN), stopHorizontalMotor, RISING);
    attachInterrupt(digitalPinToInterrupt(LEFT_INTERRUPT_PIN), stopVerticallMotors, RISING);
}

void stopHorizontalMotor()
{
    //horizontal_stepper->stop();
    h_stepper.stop();
    //Serial.println("works_horiz");
    return;
}

void stopVerticalMotors()
{
    //left_vertical_stepper->stop();
    lv_stepper.stop();
    rv_stepper.stop();
    //right_vertical_stepper->stop();
    //Serial.println("works_vertil");
    return;
}

void loop() {    
}
