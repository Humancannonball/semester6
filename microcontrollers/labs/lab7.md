Faculty of Electronics
Department of Computer and Communication Technologies

# Laboratory work 7

## Study of radio module NRF24L01

Report by: Mark Mikula, IRDfu-22

## Work objective

Learn how to transfer information between two IoT devices using the NRF24L01 transceiver.

## Task

While completing the tasks, in parallel, prepare the report of the laboratory work. Write
down the steps you take and notes.

1.  Make sure the NRF24L01 transceiver is connected to your EL_lab board. Make sure that the
    NR24 library is installed in the Arduino IDE environment (Tools->Manage Libraries. Type
    "NRF24L01" in the search box, the status of the RF24 library should be "installed").
2.  Open the scanner example: `File->examples->RF24->scanner`. Change program line 34 from
    `RF24 radio(7, 8);` to `RF24 radio(38, 40);`. Compile and upload the program to the Arduino
    board. Monitor the results of the radio broadcast scan in the Serial Monitor window. Record
    which radio channels are busy and which are free. Choose a free channel, write down its
    number. - 77
3.  Download the `U3.ino` program from moodle. When working in pairs, one student will need
    to configure the program to run in transmitter mode, and the other student will need to
    configure the program to run in receiver mode. Replace `radio.setChannel(1);` radio channel
    number to the one you selected in the previous point (the channel must be the same in the
    pair). Upload the modified programs to the Arduino. Open Serial Monitor and watch if the
    data is being transferred. The program sends a sequence of numbers 0,1,2,...255,0,1,... Are
    all the data (numbers) transmitted successfully? Does the connection quality
    improve/deteriorate if you change the distance between the transmitter/receiver? Change
    the line `radio.setAutoAck(false);` to `radio.setAutoAck(true);` on both Arduinos. Monitor data
    transfer. Has connection reliability changed? Why? – No.
4.  Download the `U4.ino` program from moodle. Upload this program to a pair of Arduinos.
    Change the communication channel number to your chosen one. Now with button M1 you
    can control LED1 of another Arduino. Change the program so that you can turn LED1 and
    LED2 on/off with buttons M1-M4.

### Comprehensive Code for All Lab 7 Tasks

```c++
#include "RF24.h"
#include "printf.h"

// Pin definitions
#define M1 2
#define M2 3
#define M3 43
#define M4 44
#define LED1 A12
#define LED2 A13
#define LED3 A14
#define LED4 A15

// Radio configuration
RF24 radio(38, 40, 4000000);
unsigned char address0[] = "00001"; // Address for this device
unsigned char address1[] = "00002"; // Address for paired device
unsigned char broadcast[] = "BCAST"; // Broadcast address for chat feature

// Chat configuration
#define MAX_MESSAGE_LENGTH 30
char message[MAX_MESSAGE_LENGTH] = "";
int messageIndex = 0;
bool isInChatMode = false;

// Data structure for LED control
struct RadioPacket {
  uint8_t type;      // 0: LED command, 1: Chat message
  uint8_t ledPin;    // Which LED to control
  uint8_t ledState;  // 1: ON, 0: OFF
  char text[MAX_MESSAGE_LENGTH]; // Chat message
};

RadioPacket txPacket;
RadioPacket rxPacket;

void setup() {
  // Initialize buttons
  pinMode(M1, INPUT_PULLUP);
  pinMode(M2, INPUT_PULLUP);
  pinMode(M3, INPUT_PULLUP);
  pinMode(M4, INPUT_PULLUP);
  
  // Initialize LEDs
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);

  // Start serial communication
  Serial.begin(115200);
  printf_begin();
  Serial.println("NRF24L01 Demo");
  Serial.println("Commands:");
  Serial.println("1: Toggle Chat Mode");
  Serial.println("2: Send Test Message");
  Serial.println("3: Scan Channels");
  
  // Setup and configure rf radio
  radio.begin();
  radio.setAutoAck(true);
  radio.setChannel(77);  // Use the free channel you found with the scanner
  radio.setPayloadSize(sizeof(RadioPacket));
  radio.setRetries(15, 15);
  radio.openReadingPipe(1, address1);
  radio.openWritingPipe(address0);
  radio.setPALevel(RF24_PA_MAX);
  radio.startListening();
  radio.printDetails();
}

void loop() {
  // Process serial input for chat and commands
  if (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    
    // Command handling
    if (inChar == '1') {
      isInChatMode = !isInChatMode;
      Serial.print("Chat mode: ");
      Serial.println(isInChatMode ? "ON" : "OFF");
    }
    else if (inChar == '2') {
      sendChatMessage("Test Message");
    }
    else if (inChar == '3') {
      scanChannels();
    }
    // Chat message handling
    else if (isInChatMode) {
      if (inChar == '\n' || inChar == '\r') {
        if (messageIndex > 0) {
          message[messageIndex] = '\0'; // Null terminate
          sendChatMessage(message);
          messageIndex = 0;
        }
      } 
      else if (messageIndex < MAX_MESSAGE_LENGTH - 1) {
        message[messageIndex++] = inChar;
      }
    }
  }

  // Button handling for LED control
  if (digitalRead(M1) == 0) {
    sendLEDCommand(LED1, 1); // Turn ON LED1
    delay(200);
  }
  if (digitalRead(M2) == 0) {
    sendLEDCommand(LED2, 1); // Turn ON LED2
    delay(200);
  }
  if (digitalRead(M3) == 0) {
    sendLEDCommand(LED1, 0); // Turn OFF LED1
    delay(200);
  }
  if (digitalRead(M4) == 0) {
    sendLEDCommand(LED2, 0); // Turn OFF LED2
    delay(200);
  }
  
  // Listen for incoming messages
  receiveData();
}

void sendLEDCommand(uint8_t led, uint8_t state) {
  radio.stopListening();
  
  txPacket.type = 0; // LED command
  txPacket.ledPin = led;
  txPacket.ledState = state;
  
  if (radio.write(&txPacket, sizeof(txPacket))) {
    Serial.println("LED command sent successfully");
  } else {
    Serial.println("Failed to send LED command");
  }
  
  radio.startListening();
}

void sendChatMessage(const char* msg) {
  radio.stopListening();
  
  txPacket.type = 1; // Chat message
  strncpy(txPacket.text, msg, MAX_MESSAGE_LENGTH - 1);
  txPacket.text[MAX_MESSAGE_LENGTH - 1] = '\0'; // Ensure null termination
  
  if (radio.write(&txPacket, sizeof(txPacket))) {
    Serial.print("Sent: ");
    Serial.println(msg);
  } else {
    Serial.println("Failed to send message");
  }
  
  radio.startListening();
}

void receiveData() {
  if (radio.available()) {
    radio.read(&rxPacket, sizeof(rxPacket));
    
    if (rxPacket.type == 0) {
      // LED command
      uint8_t led = rxPacket.ledPin;
      uint8_t state = rxPacket.ledState;
      
      if (state == 1) {
        digitalWrite(led, HIGH);
        Serial.print("LED at pin ");
        Serial.print(led);
        Serial.println(" turned ON");
      } else {
        digitalWrite(led, LOW);
        Serial.print("LED at pin ");
        Serial.print(led);
        Serial.println(" turned OFF");
      }
    }
    else if (rxPacket.type == 1) {
      // Chat message
      Serial.print("Received: ");
      Serial.println(rxPacket.text);
    }
  }
}

void scanChannels() {
  Serial.println("Scanning RF channels...");
  radio.stopListening();
  
  for (uint8_t channel = 0; channel <= 125; channel++) {
    radio.setChannel(channel);
    
    radio.startListening();
    delayMicroseconds(225);
    
    if (radio.testRPD()) {
      Serial.print("Signal detected on channel ");
      Serial.println(channel);
    }
    
    radio.stopListening();
  }
  
  // Restore original channel
  radio.setChannel(77);
  radio.startListening();
  Serial.println("Scan complete");
}
```

5.  Modify the `U4.ino` program so that you can exchange messages between a pair of Arduinos
    t. i.e. create a Chat app.
6.  BONUS1. Try to intercept commands sent by other Arduino pairs.
7.  BONUS2. Create a program that allows all Arduinos to join the "chat".
8.  Prepare the report, upload it to moodle in pdf format.
