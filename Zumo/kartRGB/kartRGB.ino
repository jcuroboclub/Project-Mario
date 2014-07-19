/*
 * Let's Go!
 */
 
/* 
 To do:
 
 Convert timed events to use Timer library
 Breakout control logic to separate functions
 Wait for comms events instead of continuous looping
 Turn motors off if comms drops
 
 */

// Inlcudes
#include <QTRSensors.h>
#include <ZumoReflectanceSensorArray.h>
#include <ZumoMotors.h>
#include <ZumoBuzzer.h>
#include <Pushbutton.h>
#include "Adafruit_NeoPixel.h"
#include "StateMachine.h"

// Zumo stuff
ZumoBuzzer buzzer;
//ZumoReflectanceSensorArray reflectanceSensors;
ZumoMotors motors;
Pushbutton button(ZUMO_BUTTON);
#define MAX_SPEED 400

// Speed control
int leftSpeed = 0;
int rightSpeed = 0;
int averageSpeed = 0;
int previousAverageSpeed = 0;

//LEDs
Adafruit_NeoPixel ledStrip = Adafruit_NeoPixel(2, 11, NEO_GRB + NEO_KHZ800);

//LED state machine
#define LED_OFF 0
#define LED_BOOST 1
#define LED_BOOST2 2
#define LED_BRAKE 3
#define LED_REVERSE 4
StateMachine ledStateMachine = StateMachine(ledStateMachineCallback);

//Powerup state machine
#define POWERUP_NONE 0 
#define POWERUP_BOOST 1
StateMachine powerupStateMachine = StateMachine(powerupStateMachineCallback);

//Message buffer
unsigned char messageState = 0;
unsigned char messageInPtr = 0;
unsigned char message[4];

void setup()
{
  //Init comms
  Serial.begin(9600);
  Serial.println("Mario Kart");
  //message.attach(messageCompleted);
  
  //Init LEDs to blue
  ledStrip.begin();
  ledStrip.setPixelColor(0,0,0,0x33);
  ledStrip.setPixelColor(1,0,0,0x33);
  ledStrip.show();
  
  // Play a little welcome song
  buzzer.play(">g32>>c32");
  
  //Wait for button press
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
  button.waitForButton();
  
  //Turn off LED
  digitalWrite(13, LOW);
  
  //Play music to indicate ready
  buzzer.play("L16 cdegreg4");
  while(buzzer.isPlaying());
}

void loop()
{
  //Process any commes messages
  checkForComms();
  
  //State Machines
  ledStateMachine.update();
  powerupStateMachine.update();
    
  //Sanity check
  if (leftSpeed > MAX_SPEED) leftSpeed = MAX_SPEED;
  if (rightSpeed > MAX_SPEED) rightSpeed = MAX_SPEED;
  if (leftSpeed < -MAX_SPEED) leftSpeed = -MAX_SPEED;
  if (rightSpeed < -MAX_SPEED) rightSpeed = -MAX_SPEED; 
    
  //Set motor speed
  motors.setSpeeds(leftSpeed, rightSpeed);
}

//
// powerUpStateMachine
// 
// Game logic for power ups
//
void powerupStateMachineCallback()
{
  switch (powerupStateMachine.currentState()) {
    case POWERUP_BOOST:
      powerupStateMachine.nextState(POWERUP_NONE,10000);
      //Change LED state to boosted
      ledStateMachine.nextState(LED_BOOST,0);
      //Play song
      buzzer.play("L16 >d+16r>d+16r>d+8r>d+16r>d+16r>d+32r32>d+16r>d+16r>c+16r>c+16r>c+8r>c+16r>c+16r>c+32r32>c+16r>c+16r>d+16r>d+16r>d+8r>d+16r>d+16r>d+32r32>d+16r>d+16r>c+16r>c+16r>c+8r>c+16r>c+16r>c+32r32>c+16r>c+16r");
      break;
      
    case POWERUP_NONE:
      ledStateMachine.nextState(LED_OFF,0);
      powerupStateMachine.stop();
      break;
  }
}

//
// ledStateMachine
// 
// LEDs can indicate boosted, braking, reversing.
// State machine allows for timed / flashing LEDs
//
// To do: Convert to use timer library
void ledStateMachineCallback()
{
    //Led State Machine
    switch (ledStateMachine.currentState()) {
      case LED_BOOST :
        ledStrip.setPixelColor(0,0x77,0x77,0x00);
        ledStrip.setPixelColor(1,0x00,0x00,0x00);
        digitalWrite(13,HIGH);
        ledStrip.show();
        ledStateMachine.nextState(LED_BOOST2,50);
        break;
        
      case LED_BOOST2:
        ledStrip.setPixelColor(1,0x77,0x77,0x00);
        ledStrip.setPixelColor(0,0x00,0x00,0x00);
        digitalWrite(13,LOW);
        ledStrip.show();
        ledStateMachine.nextState(LED_BOOST,50);
        break;
        
      case LED_BRAKE:
        ledStrip.setPixelColor(0,0xaa,0x00,0x00);
        ledStrip.setPixelColor(1,0xaa,0x00,0x00);
        ledStrip.show();
        ledStateMachine.nextState(LED_OFF,500);
        break;
        
      case LED_REVERSE:
        ledStrip.setPixelColor(0,0x77,0x77,0x77);
        ledStrip.setPixelColor(1,0x77,0x77,0x77);
        ledStrip.show();
        ledStateMachine.nextState(LED_OFF,200);
        break;
        
      case LED_OFF:
        ledStrip.setPixelColor(0,0,0,0);
        ledStrip.setPixelColor(1,0,0,0);
        ledStrip.show();
        ledStateMachine.stop();
        break;
  }  
}

//
// Process incoming bytes
//
void checkForComms()
{
  while(Serial.available()) {
    byte b = Serial.read();
    
    switch (messageState) {
      //Waiting for start byte
      case 0:
      if(b == 0x00) {
        messageState = 1;
        messageInPtr = 0;
      }
      break;
      
      // Store bytes
      case 1:
      message[messageInPtr] = b;
      messageInPtr++;
      if (messageInPtr >= 3) messageState = 2;
      break;
      
      // Process bytes
      case 2:
      setSpeed(message[0],message[1]);
      setState(message[2]);
      messageState = 0;
      break;
    }
  }  
}


//
// Set speeds and check if brake lights need to come on
//
void setSpeed(unsigned char left, unsigned char right) 
{
  leftSpeed = ((int)left - 64) * 25 / 4;
  rightSpeed = ((int)right - 64) * 25 / 4;
  
  averageSpeed = (leftSpeed + rightSpeed) / 2;
  
  //If not boosted, check if brake or reverse lights required
  if(powerupStateMachine.currentState() == POWERUP_NONE) {
    //If going backwards, turn on brake lights
    if (averageSpeed < 0) {
      ledStateMachine.nextState(LED_REVERSE,0);
    }
    //If braking, turn on brake lights
    else if (averageSpeed < previousAverageSpeed - 20) {
      ledStateMachine.nextState(LED_BRAKE,0);
    }
    previousAverageSpeed = averageSpeed;
  }
}

//
// Kart states
//
// 1 = POWERUP_BOOST
void setState(unsigned char state) 
{
  if (state != 0) {
    //Enable state
    powerupStateMachine.nextState(state,0);
  }
}
  
