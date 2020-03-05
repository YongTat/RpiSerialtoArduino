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
#include <EduIntro.h>
#include <SPI.h>
#include <LoRa.h>

String NodeName = "A5";
String incomingString = "";
int mode = 0;
int ledstate = 0;
const int NUM_LEDS = 30;
CRGB leds[NUM_LEDS];
DHT11 dht11(D4);
int C;
int H;
long counter = 0;
long randsendback = 0;

void setup() {
  Serial.begin(9600);
  incomingString.reserve(200);
  Serial.println("LoRa Receiver");

  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  FastLED.addLeds<WS2812, 5, BRG>(leds, NUM_LEDS);
  randomSeed(analogRead(0));
  randsendback = random(60000, 90000);
  Serial.println(randsendback);
}

void loop() {
  //main counter for sensor data relay
  if (counter == randsendback){
    Serial.println("Sending Temp and humidity");
    dht11.update();
    C = dht11.readCelsius();
    H = dht11.readHumidity();
    LoRa.beginPacket();
    LoRa.print(NodeName);
    LoRa.print("NS");
    LoRa.print(C);
    LoRa.print("C");
    LoRa.print(H);
    LoRa.print("%");
    LoRa.endPacket();
    counter = 0;
  }
  else{
    counter++;
    delay(1);
  }
  //switch case for data from Rpi
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
              Serial.println("On");
              ledstate = 1;
            }
            else{
              delay(1);
              leds[0]= CRGB::Black;
              FastLED.show();
              Serial.println("Off");
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
      LoRa.print("NL");
      LoRa.print(ledstate);
      LoRa.endPacket();
      incomingString = "";
      mode = 0;
      break;
    }
  }
  incomingString = "";
  delay(1);
}
