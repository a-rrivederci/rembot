// @version 2.0.0

void count_down() {
    for (byte i; i<5; i++) {
        Serial.println(i);
    }
    delay(100); // delay for 1/10 of a second
    Serial.println("DONE");
}
