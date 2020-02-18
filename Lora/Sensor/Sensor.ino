#include <dht.h>

dht DHT;

#define DHT11_PIN 4

int temp = 0;
int humid = 0;

void setup(){
  Serial.begin(9600);
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  temp = DHT.temperature;
  humid = DHT.humidity;
  Serial.println(temp);
  Serial.println(humid);
  delay(1000);
}
