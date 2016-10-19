#include "DHT.h"



#include <Wire.h>

#define SLAVE_ADDRESS 0x04 //define slave address for Arduino

#define speedPin 11


#define DHTPIN 2     


#define DHTTYPE DHT22   



DHT dht(DHTPIN, DHTTYPE);



int number = 0;
int state = 0;
const int analogInPin1 = A0;  // Analog input from right solar panel
const int analogInPin2 = A1; // Analog input from left solar panel 
int voltage1 = 0;        // value read right solar panel
char dataString[5] = {0};


void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  analogWrite(speedPin, 100);

  dht.begin();
}

void getSensorData() {
  
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);

  
  if (isnan(h) || isnan(t) || isnan(f)) {
    //Serial.println("Failed to read from DHT sensor!");
    return;
  }

  
  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(t);
  Serial.print(" *C ");
  Serial.print(f);
  Serial.print(" *F\t");
  Serial.print("Heat index: ");
  Serial.print(hic);
  Serial.print(" *C ");
  Serial.print(hif);
  Serial.print(" *F;");
}

void loop() {
  // read the analog in value:
  voltage1 = analogRead(analogInPin1);
   // print the results to the serial monitor:
 
  //Serial.println(voltage1);
  //Serial.println(voltage2);
   getSensorData();
   
   String temp = "a";
   temp = temp + voltage1;
   temp.toCharArray(dataString , 5);
  // wait 1 second before the next loop
  // after the last reading:
  
  
  Serial.println(dataString);   // send the data
  delay(1000);                  // wait 1 second before the next loop
}

// callback for received data
void receiveData(int byteCount){

  while(Wire.available()) {
    number = Wire.read();

    analogWrite(speedPin, number);

    if (number){

      if (state == 0){
        digitalWrite(13, HIGH); // set the LED on
        state = 1;
      }
      else{
        digitalWrite(13, LOW); // set the LED off
        state = 0;
      }
    }
  }
}

// callback for sending data
void sendData(){
  Wire.write(number);
}


