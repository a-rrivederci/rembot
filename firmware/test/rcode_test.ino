// Serial testing with python
// License is available in LICENSE
// @author eeshiken
// @since 04-FEB-2018

String cmd = ""; // a String to hold incoming data
byte cmd_complete = 0; // whether the string is complete

void setup() {
    // initialize serial:
    Serial.begin(9600);
    // reserve 200 bytes for the cmd:
    cmd.reserve(200);
}

void loop() {
    // print the string when a newline arrives:
    if (cmd_complete) {
        Serial.println("S"); // Success message
        // clear the string:
        decode_rcode(cmd);
        cmd = "";
        cmd_complete = 0;
    }
}

void decode_rcode(String command) {
}

/*
  SerialEvent occurs whenever a new data comes in the hardware serial RX. This
  routine is run between each time loop() runs, so using delay inside loop can
  delay response. Multiple bytes of data may be available.
*/
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the cmd:
    cmd += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      cmd_complete = 1;
    }
  }
}