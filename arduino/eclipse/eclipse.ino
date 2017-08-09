#include <OneWire.h>
#include <DallasTemperature.h>

//Pins
int solarPin = A0;
int tempPin = 7;
int tempPinShade = 5;

//Both temperature sensors
OneWire oneWire(tempPin);
OneWire oneWireShade(tempPinShade);
DallasTemperature sensors(&oneWire);
DallasTemperature sensorsShade(&oneWireShade);


void setup() 
{
  Serial.begin(9600);
  //pinMode(solarPin, INPUT);

  sensors.begin();
  sensorsShade.begin();
}

void loop() 
{
  logSolar();
 // delay(500);
  logTempShade();
 // delay(500);
  logTemp();
 // delay(500);
}


void logTemp()
{
  sensors.requestTemperatures();

  String output = buildString("TempPin", tempPin, sensors.getTempCByIndex(0));
  Serial.println(output);
}


void logTempShade()
{
  sensorsShade.requestTemperatures();

  String output = buildString("TempPinShade", tempPinShade, sensorsShade.getTempCByIndex(0));
  Serial.println(output);
}


void logSolar()
{
  int data = analogRead(solarPin);
  
  String output = buildString("SolarPin", solarPin, data);
  Serial.println(output);
}

//Concats everything for our raspberry pi to read
String buildString(String text, int pin, float data)
{
  String output = text;
  output.concat(",");
  output.concat(millis());
  output.concat(",");
  output.concat(pin);
  output.concat(",");
  output.concat(data);

  return output;
}


