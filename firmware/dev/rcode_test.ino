// Serial testing with python
// License is available in LICENSE
// @author eeshiken
// @since 04-FEB-2018

// Constants
// Program defines
#define DEBUG
#define VERBOSE
#define VERSION_MAJOR       (2)
#define VERSION_MINOR       (0)
#define VERSION_PATCH       (0)
#define FINE_SPEED          (1000)
#define MAX_SPEED           (1000)
#define ARM_TURN_TIME       (80)
#define CLAW_TURN_TIME      (140)
#define STEP                (50)
#define MAX_BUF             (64)
// Hardware defines
#define BAUD_RATE           (9600)
#define ARM_PIN             (10)
#define CLAW_PIN            (9)
#define HOR_INTERRUPT_PIN   (2)
#define LEFT_INTERRUPT_PIN  (3)
#define RIGHT_INTERRUPT_PIN (3)

char serial_buffer[MAX_BUF];  // where we store the message until we get a ';'
byte sofar;  // how much is in the buffer
byte LINE_COMPLETE; // whether the input line is complete

/**
 * Read the input buffer and find any recognized commands.  One G or M command per line.
 */
void decode() {
    // blank lines
    if(serial_buffer[0]==';') return;

    long cmd;

    cmd = parsenumber('R',-1);
    switch(cmd) {
        case 0: 
            Serial.println("Resetting ...");
            break;
        case 1: 
            Serial.println(parsenumber('X',0));
            Serial.println(parsenumber('Y',0));
            Serial.println(parsenumber('F',0));
            Serial.println("Draw line ...");
            break;
        case 2:
            Serial.println(parsenumber('P',0));
            Serial.println("Actuate arm ...");
            break;
        case 3:
            Serial.println(parsenumber('C',0));
            Serial.println("Actuate claw ...");
            break;
        default:
            break;
    }

    cmd = parsenumber('M',-1);
    switch(cmd) {
        case 90:
            Serial.println(parsenumber('X',0));
            Serial.println(parsenumber('Y',0));
            Serial.println("Setting Coords ...");
            break;
        case 100:
            help();
            break;
        default: break;
    }
}

/**
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the serial_buffer if space is available
    #ifdef DEBUG
    Serial.print(inChar);  // repeat it back so I know you got the message
    #endif
    if(sofar < MAX_BUF-1) serial_buffer[sofar++] = inChar;
    // if the incoming character is a newline, set a FLAG so the main loop can
    // do something about it:
    if (inChar == '\n') {
        serial_buffer[sofar] = 0;  // end the buffer so string functions work right
        LINE_COMPLETE = 1;
    }
  }
}


/**
 * 
 */
void help() {
    Serial.print(F("Rembot Firmare v"));
    Serial.print(VERSION_MAJOR);
    Serial.print(F("."));
    Serial.print(VERSION_MINOR);
    Serial.print(F("."));
    Serial.println(VERSION_PATCH);
    Serial.println(F("Commands:"));
    Serial.println(F("R00 - Reset"));
    Serial.println(F("R01 X[(steps)] Y[(steps)] F[(speed)]; - line"));
    Serial.println(F("R02 P[(arm)]; - arm"));
    Serial.println(F("R03 C[(claw)]; - claw"));
    Serial.println(F("M90 X[(steps)] Y[(steps)]; - Set position"));
    Serial.println(F("M100; - this help message"));
    Serial.println(F("All commands must end with a newline.")); 
}

/**
 * prepares the input buffer to receive a new message and tells the serial connected device it is ready for more.
 */
void ready() {
    sofar = 0;
    LINE_COMPLETE = 0;
    Serial.print(F(">"));  // signal ready to receive input
}

/**
 * Look for character /code/ in the buffer and read the float that immediately follows it.
 * @return the value found.  If nothing is found, /val/ is returned.
 * @input code the character to look for.
 * @input val the return value if /code/ is not found.
 **/
float parsenumber(char code,float val) {
  char *ptr = serial_buffer;  // start at the beginning of buffer
  while((long)ptr > 1 && (*ptr) && (long)ptr < (long)serial_buffer+sofar) {  // walk to the end
    if(*ptr==code) {  // if you find code on your walk,
      return atof(ptr+1);  // convert the digits that follow into a float and return it
    }
    ptr=strchr(ptr,' ')+1;  // take a step from here to the letter after the next space
  }
  return val;  // end reached, nothing found, return default val.
}

void setup() {
    // initialize serial:
    Serial.begin(BAUD_RATE);
    help();
    ready();
}

void loop() {
    // print the string when a newline arrives:
    if (LINE_COMPLETE) {
        Serial.println("S"); // Success message
        #ifdef DEBUG
        Serial.println(serial_buffer);
        #endif
        decode();
        // Get ready to receive more
        ready();
    }
}
