// Custom stepper methods
// @version 0.1.0

// Motor left and right vertical steppers up
void go_up() {
    step = STEP;
    v_stepper.setMaxSpeed(MAX_SPEED);
    v_stepper.setAcceleration(Y_ACCEL);
    v_stepper.moveTo(v_stepper.currentPosition() - step);
    
    #ifdef VERBOSE
    Serial.println("Going up ... ");
    #endif

    v_stepper.runToPosition();

    global_coords.y -= 1;

    return;
}

// Move left and right vertical steppers down
void go_down() {
    step = -1*STEP;
    v_stepper.setMaxSpeed(MAX_SPEED);
    v_stepper.setAcceleration(Y_ACCEL);
    v_stepper.moveTo(v_stepper.currentPosition() - step);

    #ifdef VERBOSE
    Serial.println("Going down ... ");
    #endif

    v_stepper.runToPosition();

    global_coords.y += 1;

    return;
}

// Move horizontal stepper left
void go_left() {
    step = STEP;
    h_stepper.setMaxSpeed(MAX_SPEED);
    h_stepper.setAcceleration(X_ACCEL);
    h_stepper.moveTo(h_stepper.currentPosition() - step);

    #ifdef VERBOSE
    Serial.println("Going left ... ");
    #endif

    h_stepper.runToPosition();

    global_coords.x -= 1;
    return;
}

// Move horizontal stepper right
void go_right() {
    step = -1*STEP;
    h_stepper.setMaxSpeed(MAX_SPEED);
    h_stepper.setAcceleration(Y_ACCEL);
    h_stepper.moveTo(h_stepper.currentPosition() - step);

    #ifdef VERBOSE
    Serial.println("Going right ... ");
    #endif

    h_stepper.runToPosition();

    global_coords.x += 1;

    return;
}

// Reset steppers to limit swithces
void reset_steppers() {

    #ifdef VERBOSE
    Serial.println("Going to limit switches ... ");
    #endif

    for(int i = 0; i < 10000; i++)
        go_up();
    for(int i = 0; i < 2000; i++)
        go_left();
    
    global_coords.x = 0;
    global_coords.y = 0;
    //step = STEP;
    //v_stepper.setMaxSpeed(MAX_SPEED);
    //v_stepper.setAcceleration(Y_ACCEL);
    //v_stepper.moveTo(v_stepper.currentPosition() - 10000000*step);

    //h_stepper.setMaxSpeed(MAX_SPEED);
    //h_stepper.setAcceleration(Y_ACCEL);
    //h_stepper.moveTo(v_stepper.currentPosition() + 10000000*step);

    //v_stepper.runToPosition();
    //h_stepper.runToPosition();

    return;
}

// Move to page marigin
void find_corner() {

    #ifdef VERBOSE
    Serial.println("Finding corner of the page ... ");
    #endif

    for(int i = 0; i < 7500; i++)
        go_down();
    for(int i = 0; i < 500; i++)
        go_right();

    //step = STEP;
    //v_stepper.setMaxSpeed(MAX_SPEED);
    //v_stepper.setAcceleration(Y_ACCEL);
    //v_stepper.moveTo(v_stepper.currentPosition() + 7500*step);

    //h_stepper.setMaxSpeed(MAX_SPEED);
    //h_stepper.setAcceleration(Y_ACCEL);
    //h_stepper.moveTo(v_stepper.currentPosition() - 500*step);

    //v_stepper.runToPosition();
    //h_stepper.runToPosition();

    return;
}

/*
void findEdgeAndStepDown() {
    #ifdef VERBOSE
    Serial.println("Going to the beginnig of the margin ... ");
    #endif

    go_down();

    for(int i = 0; i < 1000; i++)
        go_left();

    //step = STEP;

    //v_stepper.setMaxSpeed(MAX_SPEED);
    //v_stepper.setAcceleration(Y_ACCEL);
    //v_stepper.moveTo(v_stepper.currentPosition() + step);

    //h_stepper.setMaxSpeed(MAX_SPEED);
    //h_stepper.setAcceleration(Y_ACCEL);
    //h_stepper.moveTo(v_stepper.currentPosition() + 50000*step);

    //h_stepper.runToPosition();

    return;
}
*/

// Move to  from current position to
// X coordinate and Y coordinate
void move_to_coordinate(int X, int Y) { 
    // absolute not relative
    if (global_coords.x < X)
        while(global_coords.x != X)
            go_right();
    else 
        while (global_coords.x != X)
            go_left();

    if (global_coords.y < Y)
        while (global_coords.y != Y)
            go_down();
    else 
        while (global_coords.y != Y)
            go_up();
}
