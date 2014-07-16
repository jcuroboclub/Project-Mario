#include <AltSoftSerial.h>
/* A module I have been using, implementing a basic protocol. May not be the
final protocol, but works for now.
Simply relays data over standard serial pins. Connect BT to pins 8 and 9 as
outlined below.
*/

// AltSoftSerial always uses these pins:
//
// Board          Transmit  Receive   PWM Unusable
// -----          --------  -------   ------------
// Teensy 2.0         9        10       (none)
// Teensy++ 2.0      25         4       26, 27
// Arduino Uno        9         8         10
// Arduino Mega      46        48       44, 45
// Wiring-S           5         6          4
// Sanguino          13        14         12

AltSoftSerial altSerial;

void setup() {
  Serial.begin(9600);
  Serial.println("Zumo RF Test Begin");
  altSerial.begin(9600);
}

void loop() {
  char c;

  if (Serial.available()) {
    c = Serial.read();
    altSerial.print(c);
  }
  if (altSerial.available() > 4) {
    int len = altSerial.available();
    char ignore[len];
    if (len > 8) { altSerial.readBytes(ignore, len-8); } // flush input
    altSerial.readBytesUntil(0x0, ignore, len);
    char buf[4];
    altSerial.readBytesUntil('\r', buf, 4);
    Serial.print("Recieved ");
    Serial.print(len);
    Serial.print(" chars. ");
    for (int i=0; i<4; i++) {
      Serial.print(buf[i], HEX);
    }
    // 1st byte: lspeed 0=full rev, 64=halt, 127=full fwd
    // 2nd byte: rspeed 0=full rev, 64=halt, 127=full fwd
    Serial.print(" == left: ");
    Serial.print((buf[0]-64) * 25 / 4); // 400:64 maxSpeed:0.5byteRange
    Serial.print("  right: ");
    Serial.println((buf[1]-64) * 25 / 4);
  }
}

