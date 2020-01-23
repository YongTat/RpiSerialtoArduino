#include <SPI.h>
#include <LoRa.h>

String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete
int mode = 0;
int askForMessage = 0;

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
  Serial.println("LoRa Sender");

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  switch (mode){
    case 0: {
      if (askForMessage == 0){
        Serial.println("Message?");
        askForMessage = 1;
      }
      if (stringComplete) {
        Serial.print("Sending packet: ");
        Serial.println(inputString);
        LoRa.beginPacket();
        LoRa.print(inputString);
        LoRa.endPacket();
        // clear the string:
        inputString = "";
        stringComplete = false;
        mode = 1;
        askForMessage = 0;
        Serial.print("Done");
      }
      break;
    }
    case 1: {
      int packetSize = LoRa.parsePacket();
      if (packetSize) {
        // received a packet
        Serial.print("Received packet:");
        while (LoRa.available()) {
           Serial.print((char)LoRa.read());
      }
      mode = 0;
      break;      
      }
    }  
  }
  delay(1);
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
