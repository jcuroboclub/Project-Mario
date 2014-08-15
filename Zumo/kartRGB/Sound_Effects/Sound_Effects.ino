// Lachlan Hillam - 23/07/14
// Project Mario Sound Effects
// Imporved buzzer sounds for the mario kart zumos. All melodies are stored in & played from flash memory.
// This mitigates the need to load into RAM first.

#include <ZumoBuzzer.h>
#include <avr/pgmspace.h> // Required for flash storage

ZumoBuzzer buzzer;

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
  
void setup() {
  
  // A demonstration of each melody
  buzzer.playFromProgramSpace(coin);
  delay(1000);
  buzzer.playFromProgramSpace(getPowerUp);
  delay(2000);
  buzzer.playFromProgramSpace(usePowerUp);
  delay(12000);
  buzzer.playFromProgramSpace(hazard);
}

void loop() {
  

}
