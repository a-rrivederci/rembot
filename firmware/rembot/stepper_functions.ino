// Custom stepper methods
// @version 0.1.0

// @Cartesian Control
// Motor left and right vertical steppers up
void goUp() {
    step = STEP;
    vStepper.setMaxSpeed(MAX_SPEED);
    vStepper.setAcceleration(Y_ACCEL);
    vStepper.moveTo(vStepper.currentPosition() - step);
    
    #ifdef VERBOSE
    Serial.println("Going up ... ");
    #endif

    vStepper.runToPosition();

    global_coords.Y -= 1;

    return;
}
// Move left and right vertical steppers down
void goDown() {
    step = -1*STEP;
    vStepper.setMaxSpeed(MAX_SPEED);
    vStepper.setAcceleration(Y_ACCEL);
    vStepper.moveTo(vStepper.currentPosition() - step);

    #ifdef VERBOSE
    Serial.println("Going down ... ");
    #endif

    vStepper.runToPosition();

    global_coords.Y += 1;

    return;
}
// Move horizontal stepper left
void goLeft() {
    step = STEP;
    hStepper.setMaxSpeed(MAX_SPEED);
    hStepper.setAcceleration(X_ACCEL);
    hStepper.moveTo(hStepper.currentPosition() - step);

    #ifdef VERBOSE
    Serial.println("Going left ... ");
    #endif

    hStepper.runToPosition();

    global_coords.X -= 1;
    return;
}
// Move horizontal stepper right
void goRight() {
    step = -1*STEP;
    hStepper.setMaxSpeed(MAX_SPEED);
    hStepper.setAcceleration(Y_ACCEL);
    hStepper.moveTo(hStepper.currentPosition() - step);

    #ifdef VERBOSE
    Serial.println("Going right ... ");
    #endif

    hStepper.runToPosition();

    global_coords.X += 1;

    return;
}


// @Z Control
// Move horizontal stepper right
void liftPen() {
    // Check if arm is raised
    if (ARM_STATUS != 0) {
        #ifdef VERBOSE
        Serial.println("Arm is already raised\n");
        #endif

        return;
    }

    // Raise arm
    // Start turning anti-clockwise
    arm_servo.attach(ARM_PIN);
    arm_servo.write(180);
    // Go on turning for the right duration
    delay(ARM_TURN_TIME);
    // Stop turning
    arm_servo.detach();

    ARM_STATUS = 1;

    #ifdef VERBOSE
    Serial.println("Arm is raised\n");
    #endif

    return;
}
// Move horizontal stepper right
void dropPen() {
    // Check if arm is already lowered
    if (ARM_STATUS != 1) {
        #ifdef VERBOSE
        Serial.println("Arm is already lowered\n");
        #endif

        return;
    }

    // Lower arm
    //Start turning clockwise
    arm_servo.attach(ARM_PIN);
    arm_servo.write(0);
    // Go on turning for the right duration
    delay(ARM_TURN_TIME);
    // Stop turning
    arm_servo.detach();

    ARM_STATUS = 0;

    #ifdef VERBOSE
    Serial.println("Arm is lowered\n");
    #endif

    return;
}
// Control the pen to be raised or dropped
// @Z Can be 0 or 1
void heightControl(float Z) {
    if (Z) {
        dropPen();
    }
    else {
        liftPen();
    }
    return;
}


// @Stepper control
// Reset steppers to limit swithces
void resetSteppers() {
    #ifdef VERBOSE
    Serial.println("Going to limit switches ... ");
    #endif

    hStepper.setMaxSpeed(MAX_SPEED);
    hStepper.setAcceleration(X_ACCEL);
    hStepper.moveTo(-hStepper.currentPosition()-10);

    vStepper.setMaxSpeed(MAX_SPEED);
    vStepper.setAcceleration(X_ACCEL);
    vStepper.moveTo(-vStepper.currentPosition()-10);

    FLAG = 1;

    // Poll the switches
    while (FLAG == 1) {
        FLAG = 0;

        if ((hStepper.distanceToGo() != 0) && (digitalRead(H_INTERRUPT_PIN) != 1)) {
            hStepper.run();
            FLAG = 1;
        }
        if ((vStepper.distanceToGo() != 0) && (digitalRead(V_INTERRUPT_PIN) != 1)) {
            vStepper.run();
            FLAG = 1;
        }
    }
    
    // Set absolute position
    global_coords.X = 0;
    global_coords.Y = 0;
    hStepper.setCurrentPosition(0);
    vStepper.setCurrentPosition(0); 

    return;
}
// Move to  from current position to
// X coordinate and Y coordinate and Z coordinate
void actuateSteppers(float X = global_coords.X, float Y = global_coords.Y, float Z, float F = MAX_SPEED) {
    float dx = X - global_coords.X;
    float dy = Y - global_coords.Y;

    hStepper.setMaxSpeed(F);
    hStepper.moveTo(-hStepper.currentPosition() - dx);

    vStepper.setMaxSpeed(F);
    vStepper.moveTo(-vStepper.currentPosition() - dy);

    heightControl(Z);

    // Update with end global position
    global_coords.X = X;
    global_coords.Y = Y;

    return ;
}
// Continuously move steppers until they reach their
// predefined targets
void runSteppers() {
    byte FLAG = 1;
    while(FLAG == 1) {
        FLAG = 0;
        if (hStepper.distanceToGo() != 0) {
            hStepper.runSpeed();
            FLAG = 1;
        }
        if (vStepper.distanceToGo() != 0) {
            vStepper.runSpeed();
            FLAG = 1;
        }
    }
    return;
}
