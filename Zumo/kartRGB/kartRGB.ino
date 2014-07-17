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
#include "Messenger.h"
#include "Adafruit_NeoPixel.h"
#include "StateMachine.h"

// Zumo stuff
ZumoBuzzer buzzer;
ZumoReflectanceSensorArray reflectanceSensors;
ZumoMotors motors;
Pushbutton button(ZUMO_BUTTON);
int lastError = 0;

// Program control
// Start flag
byte startMessageReceived = 0;
// Boost flag
#define BOOST_DURATION_MS 10000
unsigned char boostEnable = 0;
unsigned long boostTime = 0; // Timer to turn off boost

// Speed control
const int MAX_SPEED = 400; // 400 is full bore
const int NORM_SPEED = 300;
int topSpeed = NORM_SPEED;
int kartSpeed = 0;
int previousKartSpeed = 0;
int turnSpeed = 0;

//Communications
Messenger message = Messenger(',');

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


void setup()
{
  //Init comms
  Serial.begin(57600);
  Serial.println("Mario Kart");
  message.attach(messageCompleted);
  
  //Init LEDs
  ledStrip.begin();
  ledStrip.setPixelColor(0,0,0,0x33);
  ledStrip.setPixelColor(1,0,0,0x33);
  ledStrip.show();
  
  // Play a little welcome song
  buzzer.play(">g32>>c32");
  //Turn on LED to indicate waiting for comms init message
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);

  //Stop motors
  motors.setSpeeds(0,0);
  
  //Wait for init message:  *i\r\n
  while(startMessageReceived == 0) checkForComms();
  Serial.println("Let's Go!!!");

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
    
  //Calculate motor speed
  long baseSpeed = ((long)kartSpeed) * topSpeed / 100;
  long dirAdjust = baseSpeed * ((long)turnSpeed) / 100;
  int m1Speed = (int) (baseSpeed + dirAdjust);
  int m2Speed = (int) (baseSpeed - dirAdjust);

  //Set motor speed
  if (m1Speed > MAX_SPEED)
    m1Speed = MAX_SPEED;
  if (m2Speed > MAX_SPEED)
    m2Speed = MAX_SPEED;
  motors.setSpeeds(m1Speed, m2Speed);
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
      topSpeed = MAX_SPEED;
      powerupStateMachine.nextState(POWERUP_NONE,10000);
      //Change LED state to boosted
      ledStateMachine.nextState(LED_BOOST,0);
      //Play song
      buzzer.play("L16 >d+16r>d+16r>d+8r>d+16r>d+16r>d+32r32>d+16r>d+16r>c+16r>c+16r>c+8r>c+16r>c+16r>c+32r32>c+16r>c+16r>d+16r>d+16r>d+8r>d+16r>d+16r>d+32r32>d+16r>d+16r>c+16r>c+16r>c+8r>c+16r>c+16r>c+32r32>c+16r>c+16r");
      break;
      
    case POWERUP_NONE:
      topSpeed = NORM_SPEED;
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
        ledStrip.show();
        ledStateMachine.nextState(LED_BOOST2,50);
        break;
        
      case LED_BOOST2:
        ledStrip.setPixelColor(1,0x77,0x77,0x00);
        ledStrip.setPixelColor(0,0x00,0x00,0x00);
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
// Passes any incoming bytes to message object
//
void checkForComms()
{
  while(Serial.available())  message.process(Serial.read());
}

//
// message callback
//
void messageCompleted()
{
  // Boost 
  // Format:  *b/r/n
  // Function: boosts top speed for 10 seconds
  if (message.checkString("*b")) {
    setPowerup();
  }
  // Comms init
  // Format:  *i\r\n
  // Function: Indicate comms system connected
  if (message.checkString("*i")) {
    startMessageReceived = 1;
  }
  // Speed
  // Format: *s,speed,direction\r\n
  // Function: Set speed and direction of zumo
  if (message.checkString("*s")) {
    setSpeedDir(message.readInt(),message.readInt());
  }
}

void setSpeedDir(int speed, int dir) 
{
  kartSpeed = speed;
  turnSpeed = dir;
  
  //If not boosted, check if brake or reverse lights required
  if(powerupStateMachine.currentState() == POWERUP_NONE) {
    //If going backwards, turn on brake lights
    if (kartSpeed < 0) {
      ledStateMachine.nextState(LED_REVERSE,0);
    }
    //If braking, turn on brake lights
    else if (kartSpeed < previousKartSpeed - 20) {
      ledStateMachine.nextState(LED_BRAKE,0);
    }
    previousKartSpeed = kartSpeed;
  }
}

void setPowerup() 
{
  //Enable boost state
  powerupStateMachine.nextState(POWERUP_BOOST,0);
}
  
