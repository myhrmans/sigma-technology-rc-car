// -- Libs --
#include <Ethernet.h> //Load Ethernet Library
#include <EthernetUdp.h> //Load UDP Library
#include <SPI.h> //Load the SPI Library
#include <Servo.h>
#include <Arduino.h>
#include "ESC.h"
#include <ArduinoJson.h>

// -- Pins --
#define steeringControl 5
#define motorPin 4

// -- Motor and servo --
ESC esc(ESC::MODE_FORWARD_BACKWARD);
Servo steering;

// -- Network --
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE}; //Assign a mac address
IPAddress ip(10, 0, 0, 2); //Assign my IP adress
unsigned int localPort = 5005; //Assign a Port to talk over
char packetBuffer[130];
StaticJsonDocument<130> doc;
String datReq; //String for our data
int packetSize; //Size of Packet
EthernetUDP Udp; //Define UDP Object
EthernetServer server(5005);

// -- Functions --
void turn(int level);
void enableReverse();
void enableForward();
void setSpeed(int speed);
void speed(int speed);

int pwm_value_steering = 90;
int deadzone = 110;
int escSpeed = 0;

void setup() {
  esc.attach(motorPin);

  pinMode(steeringControl, OUTPUT); //Enable output on steering pin
  steering.attach(steeringControl);
  steering.write(pwm_value_steering); //Set the wheels forward on startup
  Serial.begin(9600); //Port 9600 to listen over USB
  Serial.println("----Ethernet Server-----");

  // start the Ethernet connection and the server:
  Ethernet.begin(mac, ip);

  // Check for Ethernet hardware present
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield was not found.  Sorry, can't run without hardware. :(");
    while (true) {
      delay(1); // do nothing, no point running without Ethernet hardware
    }
  }
  if (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("Ethernet cable is not connected.");
  }

  // start the server
  Serial.print("--Server is at ");
  Serial.print(Ethernet.localIP());
  Serial.print(" --");
  Udp.begin(localPort); //Initialize Udp

  delay(1500); //delay
  Serial.print("---READY TO RECEIVE PACKGES FROM JETSON---");
  enableForward();
}

void loop() {
  packetSize = Udp.parsePacket(); //Read theh packetSize
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());  //Initialize Packet send
  Udp.print("OK"); //Send string back to client
  Udp.endPacket(); //Packet has been sent
  if(packetSize>0){ //Check to see if a request is present
  Udp.read(packetBuffer, 130); //Reading the data request on the Udp
  String datReq(packetBuffer); //Convert packetBuffer array to string datReq
  DeserializationError error = deserializeJson(doc, datReq);
  if (error) {
   Serial.print(F("deserializeJson() failed: "));
   Serial.println(error.c_str());
   return;
 }
int steering = doc["steering"];
int spd = doc["speed"];
Serial.print("Speed: ");
Serial.print(spd);
Serial.print(" Turn: ");
Serial.println(steering);
turn(steering);
speed(spd);
Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());  //Initialize Packet send
Udp.print("OK"); //Send string back to jetson
Udp.endPacket(); //Packet has been sent
doc["speed"] = 0;
}
memset(packetBuffer, 0, 130);
}

void turn(int level){
  int turnDegree;
  turnDegree = 90-(level);
  steering.write(turnDegree);
}
void enableReverse(){
      if(esc.getDirection()==ESC::FORWARD){
            esc.setDirection(ESC::BACKWARD);
            setSpeed(500);
            delay(2000);
            setSpeed(0);
            delay(100);
      }
}
void enableForward(){
            esc.setDirection(ESC::FORWARD);
            setSpeed(0);
            delay(100);
}
void setSpeed(int speed){
  esc.setSpeed(speed);
  escSpeed=speed;
}
void speed(int speed){
  if(speed>0){
    if(esc.getDirection()==ESC::BACKWARD){
      enableForward();
    }
    setSpeed(((speed*4)+deadzone));
  }else if(speed<0){
    if(esc.getDirection()==ESC::FORWARD){
      enableReverse();
    }else{
    setSpeed((speed*-4)+deadzone);
    }
  }else{
    setSpeed(0);
  }
}
