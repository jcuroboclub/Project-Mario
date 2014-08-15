/*
 StateMachine
 
 Class to perform some state machine logic on the Arduino
*/

#include "StateMachine.h"

//
// Constructor
//
StateMachine::StateMachine(void (*callbackFunction) (void)) {
  state = 0;
  delay = 0;
  timer = 0;
  isRunning = 0;
  callback = callbackFunction;
  counter[0] = 0;
  counter[1] = 0;
}

//
// Update the state machine
//
// Use in loop()
// Will keep running over and over unless stop()ed
//
void StateMachine::update(void) {
  if (isRunning) {
    if(millis() - timer >= delay) {
      timer = millis();
      //Call the state machine
      callback();
    }
  }
}

//
// Current state
//
uint16_t StateMachine::currentState() {
  return state;
}

//
// Next state
//
void StateMachine::nextState(uint16_t nextState, uint32_t nextDelay) {
  state = nextState;
  delay = nextDelay;
  isRunning = 1;
  //Restart timer
  timer = millis();
}

//
// Stop
//
void StateMachine::stop()
{
  isRunning = 0;  
}
