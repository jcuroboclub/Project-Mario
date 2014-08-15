#include <MFRC522.h>
#include <SPI.h>


/*
== SPI Pinouts ==
 MISO - pin D12
 MOSI - pin D11
 SCK  - pin D13
 SS   - pin D8
 RST  - pin D7
 
 == RGB Pinouts ==
 (actual colour->pin may change)
 Red - pin D3
 Grn - pin D5
 Blu - pin D6
 */
#define SS_PIN1  8
#define RST_PIN1  7

#define SS_PIN2  9
#define RST_PIN2  10

MFRC522 mfrc522(SS_PIN1, RST_PIN1);	// Create MFRC522 instance.

void setup()
{
  // Init serial
  Serial.begin(9600);

  // Init SPI
  SPI.begin();

  // Init RFID module
  mfrc522.PCD_Init();
//  mfrc522_num2.PCD_Init();

}

void loop()
{

  if(!newUID())
  {
    return;
  }

  displayUIDSerial(1);
}

/*
 * Checks whether a new RFID card is present and then reads card
 *    obtaining the cards UID. If successful returns true, if fails
 *    at either stage returns false
 */
boolean newUID()
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return false;
  }

  // read from card
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    //Serial.println("No read!!");
    return false;
  }

  return true;
}

/*
 *  Displays each Byte of the UID as a HEX number setparted be ';'.
 *    Each instance if the UID display is betwn two balnk line.
 */
void displayUIDSerial(int reader)
{
  //Serial.println(reader);
  
  // all cards received with module have 4 Byte UIDs that have been tested
  for(int i = 0; i <= mfrc522.uid.size; i++)
  {
    // newline at end of UID
    if(i == mfrc522.uid.size)
    {
      Serial.println();
    }
    else
    {
      //
      if(mfrc522.uid.uidByte[i] < 0x10)
      {
        Serial.print("0");
      }
      Serial.print(mfrc522.uid.uidByte[i]);
      Serial.print(",");
    }
  }
  
  mfrc522.PICC_HaltA();
}























