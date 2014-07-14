/* Packeted_433_Coms
Lachlan Hillam - 14/07/14
Collection of functions which utilise the RadioHead library for 433MHz communications.
This file is intended to be used as a resource only.
*/

#include <RHDatagram.h>
#include <RH_ASK.h>
#include <SPI.h>

// List of node addresses
const int MASTER = 0;
const int BOT_1 = 1;
const int BOT_2 = 2;
const int BOT_3 = 3;
const int BOT_4 = 4;

// Define the address of this node
const int THIS_ADDRESS = MASTER; //Change to applicable address

// Instantiate radio driver class
RH_ASK driver;

// Instantiate datagram manager class, set address to specified
RHDatagram manager(driver, THIS_ADDRESS);
  
// Set message buffer to maximum octet size
uint8_t buf[RH_ASK_MAX_MESSAGE_LEN];
// Get buffer length & save.
uint8_t bufSize = sizeof(buf);

void setup() 
{
  //Required for compiling & debugging
  Serial.begin(9600);
  if (!manager.init())
    Serial.println("init failed");
}

void loop()
{
  // Example transmitter code:
  // Send message to Bot 1:
  uint8_t data[] = "Hello!";
  if(txTo(data, BOT_1))
  {
    Serial.println("Message sent");
  } 
  else
  {
    Serial.println("Message failed!");
  }
  
  // Send message to all nodes
  if(txAll(data))
  {
    Serial.println("Message sent");
  }
  else
  {
    Serial.println("Message failed!");
  }
  
  // Example recevier code:
  if(checkRx())
  {
    if(getRx(buf, bufSize))
    {
      Serial.println("Received: ");
    }
    else
    {
      Serial.println("Receiver error!");
    }
  }
  
}

// Sends data to the specified node. Data must be in the form of a vector of unsigned bytes.
// Function will return true or false depending on operation success.
bool txTo(uint8_t* data, int destination)
{
  if (manager.sendto(data, sizeof(data), destination))
  {
    return true;
  }
  return false;
}

// Send data to all nodes. Data must be in the form of a vector of unsigned bytes.
// Function will return true or false depending on operation success.
bool txAll(uint8_t* data )
{
  if (driver.send(data, sizeof(data)))
  {
    return true;
  }
  return false;
}

// Check if data for this or all nodes has arrived.
bool checkRx()
{
  if (manager.available())
  {
    // Data has arrived
    return true;
  }
  return false;
}
  
// Read waiting data to specified buffer. Data will be in the form of a vector of unsigned bytes.
// Function will return true or false depending on operation success.
bool getRx(uint8_t* buf, uint8_t bufSize)
{
  if(manager.recvfrom(buf, &bufSize))
  {
    return true;
  }
  return false;
}
  
  
  
  
  
  
  
  
  
  
  
  
  
  

