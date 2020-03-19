#include <avr/sleep.h>
#include <avr/wdt.h>
#include <EduIntro.h>
#include <dht.h>
#include <LoRa.h>

volatile char sleepcount = 0;

String NodeName = "A8";
String incomingString = "";
DHT11 dht11(D4);
int C;
int H;
long counter = 0;
long randsendback = 0;

void setup() {
  Serial.begin(9600);
  incomingString.reserve(200);
  Serial.println("Hello");
  Serial.println("LoRa Receiver");

  if (!LoRa.begin(923E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop(){
  // put your main code here, to run repeatedly:

  //To send the data
  sendData();

  //Disable ADC
  static byte prevADCSRA = ADCSRA;
  ADCSRA = 0;

  /* Set the type of sleep mode we want. Can be one of (in order of power saving):
   SLEEP_MODE_IDLE (Timer 0 will wake up every millisecond to keep millis running)
   SLEEP_MODE_ADC
   SLEEP_MODE_PWR_SAVE (TIMER 2 keeps running)
   SLEEP_MODE_EXT_STANDBY
   SLEEP_MODE_STANDBY (Oscillator keeps running, makes for faster wake-up)
   SLEEP_MODE_PWR_DOWN (Deep sleep)
   */
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();


  while(sleepcount < 4){
    // Turn of Brown Out Detection (low voltage). This is automatically re-enabled upon timer interrupt
    sleep_bod_disable();

    // Ensure we can wake up again by first disabling interrupts (temporarily) so
    // the wakeISR does not run before we are asleep and then prevent interrupts,
    // and then defining the ISR (Interrupt Service Routine) to run when poked awake by the timer
    noInterrupts();

    // clear various "reset" flags
    MCUSR = 0;  // allow changes, disable reset
    WDTCSR = bit (WDCE) | bit(WDE); // set interrupt mode and an interval
    WDTCSR = bit (WDIE) | bit(WDP2) | bit(WDP1) | bit(WDP0);    // set WDIE, and 1 second delay
    wdt_reset();

    // Send a message just to show we are about to sleep
    Serial.println("Good night!");
    Serial.flush();

    // Allow interrupts now
    interrupts();

    // And enter sleep mode as set above
    sleep_cpu();
    
  }

  sleep_disable();

  Serial.println("Awake");
  sleepcount = 0;
  
  ADCSRA = prevADCSRA;
 }

ISR(WDT_vect){
  wdt_disable();
  sleepcount++;
}

 void sendData(){
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
 }
