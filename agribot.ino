#include <dht.h> // You have to download this liibrary. NAME: dht library

dht  DHT; 

#define DHT11_PIN 7 // define DHT pin (humidity sensor)

#define plant1Pin A0 // for soil sensor 
#define plant2Pin A1 // 2nd for soil sensor


int sensorPin=A2;//air quality sensor
int sensorData;

String msg = "";


void setup(){

  Serial.begin(9600);  // Start serial communication
  pinMode(sensorPin,INPUT);
}


/* void readSerialPort() {
msg = "";
if (Serial.available()) {
  delay(30);
  while (Serial.available() > 0) {
    msg += (char)Serial.read();
  }
  Serial.flush();
}
} */

void loop(){


  int chk = DHT.read11(DHT11_PIN);  // check the data coming from the DHT pin
  Serial.print("Temperature = ");  // print temperature on the serial monitor
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");// Print humidity on the serial monitor
  Serial.println(DHT.humidity);

  //soil sensor


  Serial.print("1Soil = ");
  float moisture1 = readSensor(plant1Pin) ; 
  Serial.println(readSensor(moisture1));

  float moisture2 = readSensor(plant2Pin) ; 

  Serial.print("2Soil = ");
  Serial.println(moisture2);


    //air quality

  sensorData = analogRead(sensorPin);       
  Serial.print("Air Quality:");
  Serial.print(sensorData, DEC);               

  Serial.print("\n");

  if(moisture1 < 50){ //when plants are watered they have 100-130 values

    //send msg to the cnc about the soil 1
    Serial.print("#3");
    Serial.println("\n");
    //Serial.println("pump should work for plant 1");
  }
  if(moisture2 > 100){
    //move to plant 2

    Serial.print("#4");
    Serial.println("\n");
    
  }
  delay(500); // delay of 1 second
}

      /*Here are the connections
      
      Take a DHT11 sensor.
      there, in the DHT11 sensor, there  are 3 or 4 pins.
      There, on the DHT11 sensor, there is writen S, +, -
      connect "S" on the digital pin 7.
      connect "+" on the 5V pin on  Arduino.
      connect "-" on the GND pin on Arduino.
      */ 

void recordSoil(){
  
}
      
int readSensor(int plantpin) {
 int sensorValue = analogRead(plantpin);  // Read the analog value from sensor
  int outputValue = map(sensorValue, 0, 1023, 255, 0); // map the 10-bit data to 8-bit data

 
  return outputValue;             // Return analog moisture value
}
