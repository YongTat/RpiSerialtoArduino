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

String incomingString = "";
int mode = 0;
int counter = 0;
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
        
        mode = 1;
      }
      break;
    }
    case 1: {
      incomingString = "";
      counter = 0;
      mode = 0;
      break;
    }
  delay(1);
  }
}
