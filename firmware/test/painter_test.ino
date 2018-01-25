// Painter bot testing with python
//
// License is available in LICENSE
// @author eeshiken
// @since 21-JAN-2018

#define DEBUG 0 // false
#define VERSION_MAJOR 2
#define VERSION_MINOR 0
#define VERSION_PATCH 0

// Flags
byte CONNECTED = 0; //false

// Variables
char cmd;

void setup() {
    Serial.begin(BAUD_RATE); // set the baud rate
    Serial.print("Rembot Uno v");
    Serial.print(VERSION_MAJOR);
    Serial.print(".");
    Serial.print(VERSION_MINOR);
    Serial.print(".");
    Serial.println(VERSION_PATCH);
}

void loop() {
  switch (CONNECTED) {
    case 0:
        if (Serial.available()) {
            cmd = Serial.read();
            switch(cmd) {
                case 'c': 
                    CONNECTED = 1;
                    Serial.println('C');
                    break;
            }
        }
        break;
    case 1:
        if (Serial.available()) {
            cmd = Serial.read();
            switch(cmd) {
                case 'k':
                    count_down();
                    break;
                case 'd':
                    CONNECTED = 0;
                    Serial.println('D');
                    break;
            }
        }
        break;
  } 
}

void count_down() {
    for (byte i; i<5; i++) {
        Serial.println(i);
    }
    delay(100); // delay for 1/10 of a second
    Serial.println("DONE");
}
