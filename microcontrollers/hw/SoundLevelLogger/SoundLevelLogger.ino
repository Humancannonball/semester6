#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <EEPROM.h>

// OLED Display Configuration
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C // Common I2C address for 128x64 OLED
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Hardware Pins
#define BUTTON_PIN 0   // Built-in IO0 button (GPIO 0)
#define MIC_PIN A0     // Analog pin for KY-037 AO

// EEPROM Configuration
#define EEPROM_SIZE 512 // Total EEPROM size to use (bytes). ESP8266 can go up to 4096.
// Store numEntries (uint16_t = 2 bytes) at the beginning of EEPROM.
#define ADDR_NUM_ENTRIES 0
#define DATA_START_ADDR 2
struct LogEntry {
  uint16_t soundLevel; // Raw ADC value (0-1023)
};
const int MAX_ENTRIES = (EEPROM_SIZE - DATA_START_ADDR) / sizeof(LogEntry);

// Operational Modes
enum Mode {
  DISPLAY_LIVE,
  LOGGING_ACTIVE,
  MENU_SELECT,
  DATA_DUMPING,
  ERASE_CONFIRM
};
Mode currentMode = DISPLAY_LIVE;
int menuOption = 0; // 0: Start/Stop Log, 1: Dump Data, 2: Erase Data
const char* menuItems[] = {"Log ON/OFF", "Dump Data", "Erase Data"};

// Logging Variables
uint16_t numEntries = 0;
bool eepromFull = false;
unsigned long lastLogTime = 0;
const unsigned long LOG_INTERVAL = 5000; // Log every 5 seconds

// Button Handling Variables
bool buttonState = HIGH;
bool lastButtonState = HIGH;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;
unsigned long buttonPressTime = 0;
bool shortPressFlag = false;
bool longPressFlag = false;
const unsigned long LONG_PRESS_DURATION = 1500; // 1.5 seconds

void setup() {
  Serial.begin(115200);
  Serial.println("\nSound Level Logger Initializing...");

  Wire.begin(); // SDA:D2(GPIO4), SCL:D1(GPIO5) for ESP8266
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Loop forever
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);
  display.println("Sound Logger Booting...");
  display.display();
  delay(1000);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(MIC_PIN, INPUT);

  EEPROM.begin(EEPROM_SIZE);
  EEPROM.get(ADDR_NUM_ENTRIES, numEntries);
  if (numEntries > MAX_ENTRIES || numEntries < 0) { // Basic sanity check
    Serial.println("Invalid numEntries found in EEPROM, resetting.");
    numEntries = 0;
    EEPROM.put(ADDR_NUM_ENTRIES, numEntries);
    EEPROM.commit();
  }
  eepromFull = (numEntries >= MAX_ENTRIES);
  Serial.print("Initialized. Max Entries: "); Serial.println(MAX_ENTRIES);
  Serial.print("Current Entries: "); Serial.println(numEntries);
}

void loop() {
  handleButton();
  processMode();
  updateOledDisplay();
  
  // Reset press flags after one loop iteration
  shortPressFlag = false;
  longPressFlag = false;
  delay(10); // Small delay
}

void handleButton() {
  int reading = digitalRead(BUTTON_PIN);
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != buttonState) {
      buttonState = reading;
      if (buttonState == LOW) { // Button pressed
        buttonPressTime = millis();
      } else { // Button released
        if (millis() - buttonPressTime >= LONG_PRESS_DURATION) {
          longPressFlag = true;
          Serial.println("Long Press");
        } else {
          shortPressFlag = true;
          Serial.println("Short Press");
        }
      }
    }
  }
  lastButtonState = reading;
}

void processMode() {
  switch (currentMode) {
    case DISPLAY_LIVE:
      if (shortPressFlag) currentMode = MENU_SELECT;
      break;

    case LOGGING_ACTIVE:
      if (shortPressFlag) currentMode = MENU_SELECT;
      logData();
      break;

    case MENU_SELECT:
      if (shortPressFlag) {
        menuOption = (menuOption + 1) % 3; // Cycle through 3 menu items
      }
      if (longPressFlag) {
        executeMenuOption();
      }
      break;

    case DATA_DUMPING:
      dumpDataToSerial();
      currentMode = DISPLAY_LIVE; // Auto-return after dump
      break;

    case ERASE_CONFIRM:
      if (shortPressFlag) currentMode = MENU_SELECT; // Cancel
      if (longPressFlag) { // Confirm erase
        eraseAllData();
        currentMode = DISPLAY_LIVE;
      }
      break;
  }
}

void executeMenuOption() {
  switch (menuOption) {
    case 0: // Log ON/OFF
      if (currentMode == LOGGING_ACTIVE || eepromFull) { // If logging or full, stop/attempt stop
        currentMode = DISPLAY_LIVE;
        Serial.println("Logging Stopped.");
      } else { // If not logging and not full, start
        currentMode = LOGGING_ACTIVE;
        Serial.println("Logging Started.");
      }
      break;
    case 1: // Dump Data
      currentMode = DATA_DUMPING;
      break;
    case 2: // Erase Data
      currentMode = ERASE_CONFIRM;
      break;
  }
}

void logData() {
  if (eepromFull) {
    currentMode = DISPLAY_LIVE; // Stop logging if somehow re-entered while full
    return;
  }
  if (millis() - lastLogTime >= LOG_INTERVAL) {
    lastLogTime = millis();
    if (numEntries < MAX_ENTRIES) {
      LogEntry newEntry;
      newEntry.soundLevel = analogRead(MIC_PIN);
      
      unsigned int entryAddress = DATA_START_ADDR + (numEntries * sizeof(LogEntry));
      EEPROM.put(entryAddress, newEntry);
      numEntries++;
      EEPROM.put(ADDR_NUM_ENTRIES, numEntries);
      
      if (!EEPROM.commit()) {
        Serial.println("EEPROM commit failed");
      } else {
        Serial.print("Logged entry "); Serial.print(numEntries);
        Serial.print(": "); Serial.println(newEntry.soundLevel);
      }

      if (numEntries >= MAX_ENTRIES) {
        eepromFull = true;
        currentMode = DISPLAY_LIVE; // Automatically stop logging
        Serial.println("EEPROM Full. Logging stopped.");
      }
    }
  }
}

void dumpDataToSerial() {
  Serial.println("\n--- Logged Data ---");
  Serial.println("Index,SoundLevel");
  for (uint16_t i = 0; i < numEntries; i++) {
    LogEntry entry;
    unsigned int entryAddress = DATA_START_ADDR + (i * sizeof(LogEntry));
    EEPROM.get(entryAddress, entry);
    Serial.print(i);
    Serial.print(",");
    Serial.println(entry.soundLevel);
    display.clearDisplay();
    display.setCursor(0,0);
    display.setTextSize(1);
    display.println("Dumping to Serial...");
    display.print(i + 1); display.print("/"); display.println(numEntries);
    display.display();
    delay(10); // Slow down dump slightly for display update
  }
  Serial.println("--- End of Data ---");
}

void eraseAllData() {
  numEntries = 0;
  EEPROM.put(ADDR_NUM_ENTRIES, numEntries);
  // Optional: clear all data bytes, but just updating numEntries is usually enough
  // for (int i = DATA_START_ADDR; i < EEPROM_SIZE; i++) { EEPROM.write(i, 0); }
  if (EEPROM.commit()) {
    Serial.println("EEPROM data erased.");
  } else {
    Serial.println("EEPROM erase commit failed.");
  }
  eepromFull = false;
}

void updateOledDisplay() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);

  if (currentMode == DATA_DUMPING) { // Special display handled in dumpDataToSerial
      return;
  }

  // Line 1: Current Sound Level
  display.print("Sound: ");
  display.println(analogRead(MIC_PIN));

  // Line 2: EEPROM Status
  display.print(numEntries);
  display.print("/");
  display.print(MAX_ENTRIES);
  display.print(" entries");
  if (eepromFull) {
    display.setCursor(0, 18); // Approx next line for status
    display.println("EEPROM FULL!");
  } else if (currentMode == LOGGING_ACTIVE) {
    display.setCursor(70, 8); // Position next to entries count
    display.println("Logging");
  }
  
  display.setCursor(0, 28); // Approx line 4
  display.drawLine(0, 26, SCREEN_WIDTH, 26, SSD1306_WHITE);

  switch (currentMode) {
    case DISPLAY_LIVE:
    case LOGGING_ACTIVE: // Also shows this instruction
      display.println("SP: Menu");
      break;
    case MENU_SELECT:
      display.println("MENU (LP:Select SP:Next)");
      for (int i = 0; i < 3; i++) {
        display.setCursor(0, 38 + (i * 9));
        if (i == menuOption) display.print("> "); else display.print("  ");
        
        if (i == 0) { // Special handling for Log ON/OFF text
            if (numEntries < MAX_ENTRIES && currentMode != LOGGING_ACTIVE) display.print("Start Log");
            else display.print("Stop Log");
        } else {
            display.print(menuItems[i]);
        }
      }
      break;
    case ERASE_CONFIRM:
      display.println("ERASE ALL DATA?");
      display.setCursor(0, 40);
      display.println("LP: YES (Confirm)");
      display.setCursor(0, 50);
      display.println("SP: NO (Cancel)");
      break;
    default:
      display.println("Unknown Mode");
  }
  display.display();
}
