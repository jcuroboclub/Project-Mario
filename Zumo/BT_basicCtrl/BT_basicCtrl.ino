#include <ZumoMotors.h>
#include <ZumoBuzzer.h>
#define LED_PIN       13 // user LED pin

ZumoBuzzer buzzer;
int left_speed, right_speed, silenceCount;

void setup()   {          
 //initialize the pins as digital outputs
  buzzer.play(">g32>>c32");
  pinMode(LED_PIN, OUTPUT); 
  Serial.begin(9600); // opens a serial port
  left_speed = 0;
  right_speed = 0;
}

void loop() {
  if (Serial.available() > 4) {
    silenceCount = 0;
    int len = Serial.available();
    
    // clear waste
    char ignore[len];
    if (len > 8) { Serial.readBytes(ignore, len-8); } // flush input
    Serial.readBytesUntil(0x0, ignore, len); // read up to start byte
    
    // read data
    char buf[4];
    Serial.readBytesUntil('/r', buf, 4);
    // 1st byte: lspeed 0=full rev, 64=halt, 127=full fwd
    // 2nd byte: rspeed 0=full rev, 64=halt, 127=full fwd
    left_speed = (buf[0]-64) * 25 / 4; // 400:64 maxSpeed:0.5byteRange
    right_speed = (buf[1]-64) * 25 / 4;
  } else {
    silenceCount++;
    if (silenceCount>10000) {
      left_speed = 0;
      right_speed = 0;
    }
  }
  ZumoMotors::setSpeeds(left_speed, right_speed);
}
