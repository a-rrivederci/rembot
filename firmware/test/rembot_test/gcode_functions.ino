// Serial control functions
// @version 0.1.0

// SerialEvent occurs whenever a new data comes in the hardware serial RX. This
// routine is run between each time loop() runs, so using delay inside loop can
// delay response. Multiple bytes of data may be available.
void serialEvent() {
    while (Serial.available()) {
        // get the new byte:
        char inChar = (char)Serial.read();

        #ifdef VERBOSE
        Serial.print(inChar);  // repeat it back so I know you got the message
        #endif

        // add it to the serial_buffer if space is available
        if (sofar < MAX_BUF-1) {
            serial_buffer[sofar++] = inChar;
        }

        // if the incoming character is a newline, set a flag so the main loop can
        // do something about it
        if (inChar == '\n') {
            serial_buffer[sofar] = 0;  // end the buffer so string functions work right
            line_complete = 1;
        }
    }
}

// Prints out control commands available
void helpMessage() {
    Serial.print(F("Rembot Firmare v"));
    Serial.print(VERSION_MAJOR);
    Serial.print(F("."));
    Serial.print(VERSION_MINOR);
    Serial.print(F("."));
    Serial.println(VERSION_PATCH);
    Serial.println(F("Commands:"));
    Serial.println(F("G00 - Reset"));
    Serial.println(F("G01 X[(steps)] Y[(steps)] F[(speed)] - line"));
    Serial.println(F("G02 P[(arm)] - arm"));
    Serial.println(F("G03 C[(claw)] - claw"));
    Serial.println(F("M90 X[(steps)] Y[(steps)] - Set position"));
    Serial.println(F("M100 - this help message"));
    Serial.println(F("All commands must end with a newline.")); 
}

// Prepares the input buffer to receive a new message 
// and tells the serial connected device it is ready for more.
void serialReady() {
    sofar = 0;
    line_complete = 0;
    Serial.print(F(">"));  // signal ready to receive input
}

// Look for character /code/ in the buffer and read the float that immediately follows it.
// @return the value found.  If nothing is found, /val/ is returned.
// @input code the character to look for.
// @input val the return value if /code/ is not found.
int parseNumber(char code, float val) {
    char *ptr = serial_buffer;  // start at the beginning of buffer
    while ((long)ptr > 1 && (*ptr) && (long)ptr < (long)serial_buffer+sofar) {  // walk to the end
        if (*ptr == code) {  // if you find code on your walk,
            return atof(ptr + 1);  // convert the digits that follow into a float and return it
        }
        ptr = strchr(ptr,' ') + 1;  // take a step from here to the letter after the next space
    }
    return val;  // end reached, nothing found, return default val.
}

// Read the input buffer and find any recognized commands. 
// One G or M command per line.
void decodeMessage() {
    // blank lines
    if (serial_buffer[0]==0) return;

    long cmd;
    int x,y,f,p;

    cmd = parseNumber('G',-1);
    switch(cmd) {
        case 0: 
            #ifdef VERBOSE
            Serial.println("G00");
            Serial.println("Reset steppers");
            #endif

            resetSteppers();
            break;
        case 1:
            x = parseNumber('X',0);
            y = parseNumber('Y',0);
            f = parseNumber('F',0);

            #ifdef VERBOSE
            #endif

            moveToCoordinate(x,y,f);
            break;
        case 2:
            p = parseNumber('P',0);

            #ifdef VERBOSE
            Serial.print("G02 P:");
            Serial.println(p);
            #endif

            break;
        default:
            break;
    }

    cmd = parseNumber('M',-1);
    switch(cmd) {
        case 90:
            x = parseNumber('X',0);
            y = parseNumber('Y',0);

            #ifdef VERBOSE
            Serial.print("M90 X:");
            Serial.print(x);
            Serial.print(" Y:");
            Serial.println(y);
            #endif

            global_coords.x = x;
            global_coords.y = y;
            break;
        case 100:
            #ifdef VERBOSE
            Serial.println("M100");
            #endif

            helpMessage();
            break;
        default: break;
    }
}
