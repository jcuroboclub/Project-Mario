/*
 StateMachine
 
 Class to perform some state machine logic on the Arduino
*/

#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
 #include <pins_arduino.h>
#endif

class StateMachine 
{
  public:
  // Constructor
  StateMachine(void (*)(void));
  // Functions
  void update(void);
  void nextState(uint16_t, uint32_t);
  uint16_t currentState(void);
  void stop(void);

  private:
  void (*callback)(void);   // Callback to state machine code
  uint16_t state;      // Current state of the machine
  uint32_t delay;      // Delay until state change. Delay of -1 is stopped
  uint32_t timer;      // Timer to keep track of last run time
  uint8_t isRunning;   // Are we running?
  int16_t counter[2];  // Two counters for general use
};
