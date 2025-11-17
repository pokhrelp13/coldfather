#include "DHT.h"

#define DHTPIN 2      // DHT11 data pin
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

int red = 9;
int green = 10;
int blue = 11;

void setup() {
  dht.begin();
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(blue, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float temp = dht.readTemperature();   // in °C
  float hum = dht.readHumidity();       // in %

  Serial.print("Temp: "); Serial.print(temp); Serial.print(" C, ");
  Serial.print("Humidity: "); Serial.print(hum); Serial.println(" %");

  // Simple if-else logic for freshness
  if (temp <= 25 && hum >= 40 && hum <= 60) {
    // Fresh → Green
    setColor(0, 255, 0);
  }
  else if ((temp > 25 && temp <= 30) || (hum < 40 || hum > 60)) {
    // Risk → Yellow
    setColor(255, 255, 0);
  }
  else {
    // Spoiled → Red
    setColor(255, 0, 0);
  }

  delay(2000); // wait 2 seconds
}

// Function to set RGB LED color
void setColor(int r, int g, int b) {
  analogWrite(red, r);
  analogWrite(green, g);
  analogWrite(blue, b);
}