#include <ZumoBuzzer.h>
#include <ZumoMotors.h>
#include <Adafruit_NeoPixel.h>
#include <avr/pgmspace.h> // Required for flash storage

//=================
//       AUX
//=================
//**** No Aux ****
#define NO_AUX 1

//**** Colours ****
#define BLACK 2
#define RED 3
#define YELLOW 4
#define GREEN 5
#define CYAN 6
#define BLUE 7
#define MAGENTA 8
#define WHITE 9

//**** Buzzer ****
#define POWERUP 10
#define POWERDOWN  11

//**** sounds ****
const char getPowerUp[] PROGMEM =
// Powerup sound from Mario
"T500 L8 V15 ML gb>d>g>b a->c>e->a->>c b->d>f>b->>d";

const char usePowerUp[] PROGMEM =
// The classic star theme
"T300 L4 V15 MS >c>c>c ML d8>c8 R8 MS >c ML d8>c8d8 MS >c bbb ML c8b8 r8 MS b ML c8b8c8 MS b"
"MS >c>c>c ML d8>c8 R8 MS >c ML d8>c8d8 MS >c bbb ML c8b8 r8 MS b ML c8b8c8 MS b"
"MS >c>c>c ML d8>c8 R8 MS >c ML d8>c8d8 MS >c bbb ML c8b8 r8 MS b ML c8b8c8 MS b"
"MS >c>c>c ML d8>c8 R8 MS >c ML d8>c8d8 MS >c";

const char hazard[] PROGMEM = 
// Just the powerup theme, lowered an octave and in reverse
"T400 O3 L8 V15 ML >>d>b->f>db- >>c>a->e->ca- >b>g>dbg";

const char coin[] PROGMEM = 
// Optional sound effect; the "coin" sound from Mario 64
"T400 L8 V15 ML >b8 >>e2..";
//-------------------------------------------------------------------------------

uint32_t colour[] = {0x00000000,  //BLACK
                     0x0000FF00,  //RED
                     0x00FFFF00,  //YELLOW
                     0x00FF0000,  //GREEN
                     0x00FF00FF,  //CYAN
                     0x000000FF,  //BLUE
                     0x00FF00FF,  //MAGENTA
                     0x00FFFFFF}; //WHITE
                     
#define stripLen 2
#define stripPin 2

ZumoBuzzer buzzer;
Adafruit_NeoPixel ledStrip(stripLen, stripPin, NEO_RGB + NEO_KHZ800);

int left_speed, right_speed, silenceCount,AUX;


void setup()
{
  //initialize the pins as digital outputs
  buzzer.play(">g32>>c32");
  ledStrip.begin(); 
  Serial.begin(9600); // opens a serial port
  left_speed = 0;
  right_speed = 0;
}

void loop()
{
  if (Serial.available() > 4) {
    silenceCount = 0;
    int len = Serial.available();

    // clear waste
    char ignore[len];
    if (len > 8) { 
      Serial.readBytes(ignore, len-8); 
    } // flush input
    Serial.readBytesUntil(0x0, ignore, len); // read up to start byte

    // read data
    char buf[4];
    Serial.readBytesUntil('/r', buf, 4);
    // 1st byte: lspeed 0=full rev, 64=halt, 127=full fwd
    // 2nd byte: rspeed 0=full rev, 64=halt, 127=full fwd
    left_speed = (buf[0]-64) * 25 / 4; // 400:64 maxSpeed:0.5byteRange
    right_speed = (buf[1]-64) * 25 / 4;
    AUX = buf[2];

  } 
  else {
    silenceCount++;
    if (silenceCount>10000) {
      left_speed = 0;
      right_speed = 0;
    }
  }
  ZumoMotors::setSpeeds(left_speed, right_speed);

  if(AUX != NO_AUX)
  {
    if(AUX >= BLACK && AUX <= WHITE)
    {
      setRGB(AUX);
    }
    else if(AUX == POWERUP)
    {
      buzzer.playFromProgramSpace(getPowerUp);
    }
    else if(AUX == POWERDOWN)
    {
      buzzer.playFromProgramSpace(hazard);
    }
  }
}

// Using Neo_Pixel, set both rear LED to colour given by AUX byte
void setRGB(int col)
{
  for(int led = 0; led < stripLen; led++){
    ledStrip.setPixelColor(led,colour[col-2]);
  }
  ledStrip.show();
}


