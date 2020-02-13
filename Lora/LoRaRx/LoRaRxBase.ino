#include <bitswap.h>
#include <chipsets.h>
#include <color.h>
#include <colorpalettes.h>
#include <colorutils.h>
#include <controller.h>
#include <cpp_compat.h>
#include <dmx.h>
#include <FastLED.h>
#include <fastled_config.h>
#include <fastled_delay.h>
#include <fastled_progmem.h>
#include <fastpin.h>
#include <fastspi.h>
#include <fastspi_bitbang.h>
#include <fastspi_dma.h>
#include <fastspi_nop.h>
#include <fastspi_ref.h>
#include <fastspi_types.h>
#include <hsv2rgb.h>
#include <led_sysdefs.h>
#include <lib8tion.h>
#include <noise.h>
#include <pixelset.h>
#include <pixeltypes.h>
#include <platforms.h>
#include <power_mgt.h>

#include <SPI.h>
#include <LoRa.h>

String NodeName = "<NodeNamehere>"
String incomingString = "";
int mode = 0;
bool ledstate = False;
const int NUM_LEDS = 1;
CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  incomingString.reserve(200);
  Serial.println("LoRa Receiver");

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  FastLED.addLeds<NEOPIXEL, 6>(leds, NUM_LEDS);
}

void loop() {
  switch (mode){
    case 0: {
      int packetSize = LoRa.parsePacket();
      if (packetSize) {
        Serial.print("Recieved packet:");
        while (LoRa.available()){
          incomingString += (char)LoRa.read();
        }
        Serial.println(incomingString);
        if (incomingString == NodeName){
          if (ledstate == False){
            leds[incomingString.toInt()-1]= CRGB::Red;
            FastLED.show();
          }
          else{
            leds[incomingString.toInt()-1]= CRGB::Black;
            FastLED.show();
          }
        mode = 1;
      }
      break;
    }
    case 1: {
      Serial.println("Sending Confirm ");
      LoRa.beginPacket();
      LoRa.print("CFM");
      LoRa.endPacket();
      incomingString = "";
      mode = 0;
      break;
    }
  delay(1);
  }
}
