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

String NodeName = "A2";
String incomingString = "";
int mode = 0;
int ledstate = 0;
const int NUM_LEDS = 30;
CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(9600);
  incomingString.reserve(200);
  Serial.println("LoRa Receiver");

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  FastLED.addLeds<WS2812, 5, BRG>(leds, NUM_LEDS);
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
        if (incomingString.startsWith(NodeName)){
          if (incomingString.endsWith("LED")){
            if (ledstate == 0){
              delay(1);
              leds[0]= CRGB::Red;
              FastLED.show();
              ledstate = 1;
            }
            else{
              delay(1);
              leds[0]= CRGB::Black;
              FastLED.show();
              ledstate = 0;
            }
            mode = 1;
          }
        }
      }
      break;
    }
    case 1: {
      delay(10);
      Serial.println("Sending Confirm ");
      LoRa.beginPacket();
      LoRa.print(NodeName);
      LoRa.endPacket();
      incomingString = "";
      mode = 0;
      break;
    }
  }
  incomingString = "";
  delay(1);
}
