#include <QTRSensors.h>
#include <ZumoReflectanceSensorArray.h>
#include <ZumoMotors.h>
#include <ZumoBuzzer.h>
#define LED_PIN       13 // user LED pin

ZumoBuzzer buzzer;
ZumoReflectanceSensorArray reflectanceSensors;
int left_speed, right_speed, silenceCount;
unsigned int sensors[6];  // values from sensor array
int speed_reduction;      // speed reduction factor 
float minSpeed = 0.2;     // minimum speed after scaling
float scaleFactor = 0.0;  // scaling factor used for adjusting final speed

void setup()   {          
 //initialize the pins as digital outputs
  buzzer.play(">g32>>c32");
  pinMode(LED_PIN, OUTPUT); 
  Serial.begin(9600); // opens a serial port
  
  // Initialize the reflectance sensors module
  reflectanceSensors.init();
  
  // Initialise sensor:
  delay(1000);  // moves away from the mic to breath in
  for(int counter = 0; counter < 80; counter++)
  {
    if ((counter > 10 && counter <= 30) || (counter > 50 && counter <= 70))
    {
        left_speed = 200;
        right_speed = 200;
    }
    else
    {
        left_speed = -200;
        right_speed = -200;
    }
    ZumoMotors::setSpeeds(left_speed, right_speed);
    reflectanceSensors.calibrate(QTR_EMITTERS_ON);

    // Since our counter runs to 80, the total delay will be
    // 80*20 = 1600 ms.
    delay(20);    
  }

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
<<<<<<< HEAD
   
=======
    // Apply track detection / speed reduction
    reflectanceSensors.readCalibrated(sensors, QTR_EMITTERS_ON);
    
    speed_reduction = 0;
    for (int counter = 0; counter < 6; counter++)
    {
      if (sensors[counter] > 500) {speed_reduction++;};  // count the number of sensors ON the track
    }
    scaleFactor = minSpeed + (1 - minSpeed)*(speed_reduction/6);  // more sensonrs on the track means more speed

    left_speed *= scaleFactor;
    right_speed *= scaleFactor;
>>>>>>> origin/master
  } else {
    silenceCount++;
    if (silenceCount>10000) {
      left_speed = 0;
      right_speed = 0;
    }
  }
  ZumoMotors::setSpeeds(left_speed, right_speed);
}
