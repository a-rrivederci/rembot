// Custom stepper methods
// @version 0.1.0

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

    global_coords.y -= 1;

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

    global_coords.y += 1;

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

    global_coords.x -= 1;
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

    global_coords.x += 1;

    return;
}

// Reset steppers to limit swithces
void resetSteppers() {

    #ifdef VERBOSE
    Serial.println("Going to limit switches ... ");
    #endif

    for(int i = 0; i < 10000; i++)
        goUp();
    for(int i = 0; i < 2000; i++)
        goLeft();
    
    global_coords.x = 0;
    global_coords.y = 0;
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

// Move to page marigin
void findCorner() {

    #ifdef VERBOSE
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

/*
void findEdgeAndStepDown() {
    #ifdef VERBOSE
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
}
*/

// Move to  from current position to
// X coordinate and Y coordinate
void moveToCoordinate(int X, int Y, int F) { 
    // absolute not relative
    Serial.println(F);
    if (global_coords.x < X)
        while(global_coords.x != X)
            goRight();
    else 
        while (global_coords.x != X)
            goLeft();

    if (global_coords.y < Y)
        while (global_coords.y != Y)
            goDown();
    else 
        while (global_coords.y != Y)
            goUp();
}
