/*
 * Smart Clock Project for ESP8266 with OLED Display
 * 
 * Required Libraries:
 * - ESP8266WiFi (part of ESP8266 Arduino Core)
 * - WiFiUdp (part of ESP8266 Arduino Core)
 * - NTPClient by Fabrice Weinberg
 * - Adafruit_GFX and Adafruit_SSD1306 by Adafruit
 * 
 * Hardware:
 * - ESP8266 board
 * - 128x64 OLED display (I2C interface)
 * 
 * Connections:
 * - OLED SDA to D2 (GPIO 4)
 * - OLED SCL to D1 (GPIO 5)
 * - OLED VCC to 3.3V
 * - OLED GND to GND
 */

#include <ESP8266WiFi.h>  // Part of ESP8266 Arduino Core
#include <WiFiUdp.h>      // Part of ESP8266 Arduino Core
#include <NTPClient.h>     // By Fabrice Weinberg - https://github.com/arduino-libraries/NTPClient
#include <Wire.h>         // Built-in Arduino library for I2C
#include <Adafruit_GFX.h>     // By Adafruit - https://github.com/adafruit/Adafruit-GFX-Library
#include <Adafruit_SSD1306.h> // By Adafruit - https://github.com/adafruit/Adafruit_SSD1306

// OLED Display Configuration
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
#define SCREEN_ADDRESS 0x3C // Typical I2C address for OLED display

// Initialize display (I2C mode with default settings)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Hardware Pins
#define BUTTON_PIN 0   // Built-in IO0 button (GPIO 0)

// WiFi Credentials - replace with your network details
const char* ssid = "M&H";
const char* password = "jolynejolynejolyne";

// NTP Settings with timezone offset for local time (adjust as needed)
WiFiUDP ntpUDP;
// Define NTPClient with UTC offset (e.g., 3600 for UTC+1)
// Adjust this value based on your timezone: 3600 seconds per hour
// Examples: UTC+1: 3600, UTC+2: 7200, UTC-5: -18000
const long utcOffsetInSeconds = 0; // Change this to your UTC offset
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds, 60000);

// Time Variables
unsigned long lastNtpSync = 0;
unsigned long lastMillis = 0;
unsigned long ntpSyncInterval = 3600000; // Sync every hour (in ms)
bool timeInitialized = false;
bool ntpSyncFailed = false;

// Clock State Variables
enum ClockState {
  NORMAL_DISPLAY,
  SETTING_HOUR,
  SETTING_MINUTE,
  SETTING_ALARM_HOUR,
  SETTING_ALARM_MINUTE
};
ClockState currentState = NORMAL_DISPLAY;

// Alarm Variables
bool alarmEnabled = false;
bool alarmTriggered = false;
int alarmHour = 7;
int alarmMinute = 0;
unsigned long alarmStartTime = 0;
unsigned long alarmDuration = 30000; // 30 seconds

// Button Debouncing
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 50;
bool lastButtonState = HIGH;
bool buttonState = HIGH;

// Long Press Detection
unsigned long buttonPressTime = 0;
const unsigned long longPressTime = 2000; // 2 seconds for long press
bool isLongPress = false;

// Time variables for offline timekeeping
int hours = 0;
int minutes = 0;
int seconds = 0;
unsigned long lastSecond = 0;

// Display animation variables for alarm
int alarmAnimationFrame = 0;
unsigned long lastAnimationUpdate = 0;
const unsigned long animationSpeed = 150; // milliseconds between animation frames

void setup() {
  // Initialize Serial for debugging
  Serial.begin(115200);
  Serial.println("\nSmart Clock Initializing...");
  
  // Initialize I2C
  Wire.begin();
  
  // Initialize display
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  
  // Welcome message
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("Smart Clock");
  display.println("Initializing...");
  display.display();
  
  // Initialize button pin
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Connect to WiFi
  connectToWifi();
  
  // Initialize NTP
  timeClient.begin();
  syncTimeWithNTP();
  
  lastMillis = millis();
}

void loop() {
  // Update current time
  updateTime();
  
  // Check button input
  handleButtonInput();
  
  // Check if alarm should trigger
  checkAlarm();
  
  // Update display based on current state
  updateDisplay();
  
  // Brief delay to reduce power consumption
  delay(10);
}

void connectToWifi() {
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("Connecting to WiFi");
  display.println(ssid);
  display.display();
  
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    display.print(".");
    display.display();
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("WiFi connected!");
    display.println(WiFi.localIP().toString());
    display.display();
    delay(2000);
  } else {
    Serial.println("");
    Serial.println("WiFi connection failed");
    
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("WiFi failed");
    display.println("Using manual time");
    display.display();
    delay(2000);
  }
}

void syncTimeWithNTP() {
  if (WiFi.status() == WL_CONNECTED) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Syncing time...");
    display.display();
    
    Serial.println("Attempting NTP sync...");
    bool updated = timeClient.update();
    
    if (updated) {
      // Extract hours, minutes, seconds directly from NTPClient
      hours = timeClient.getHours();
      minutes = timeClient.getMinutes();
      seconds = timeClient.getSeconds();
      
      timeInitialized = true;
      ntpSyncFailed = false;
      lastNtpSync = millis();
      
      Serial.println("NTP sync successful!");
      Serial.print("Time: ");
      Serial.print(hours);
      Serial.print(":");
      Serial.print(minutes < 10 ? "0" : "");
      Serial.print(minutes);
      Serial.print(":");
      Serial.print(seconds < 10 ? "0" : "");
      Serial.println(seconds);
      
      display.clearDisplay();
      display.setCursor(0, 0);
      display.println("Time synced!");
      display.display();
      delay(1000);
    } else {
      ntpSyncFailed = true;
      Serial.println("NTP sync failed");
      
      display.clearDisplay();
      display.setCursor(0, 0);
      display.println("Sync failed!");
      display.display();
      delay(1000);
    }
  } else {
    ntpSyncFailed = true;
    Serial.println("Cannot sync time: WiFi not connected");
  }
}

void updateTime() {
  // Try NTP sync if it's time to do so and we're connected
  unsigned long currentMillis = millis();
  if (WiFi.status() == WL_CONNECTED && 
      (currentMillis - lastNtpSync >= ntpSyncInterval || !timeInitialized)) {
    syncTimeWithNTP();
  }
  
  // Update time using millis() for accurate tracking between NTP syncs
  if (currentMillis - lastSecond >= 1000) {
    // Calculate how many seconds have actually passed (handles millis rollover)
    unsigned long secondsPassed = (currentMillis - lastSecond) / 1000;
    lastSecond = currentMillis;
    
    // Only update time if we've initialized it
    if (timeInitialized || ntpSyncFailed) {
      // Add the elapsed seconds
      seconds += secondsPassed;
      
      // Handle minute and hour rollovers
      if (seconds >= 60) {
        seconds %= 60;
        minutes++;
        
        if (minutes >= 60) {
          minutes %= 60;
          hours++;
          
          if (hours >= 24) {
            hours %= 24;
          }
        }
      }
      
      // Print time to serial
      Serial.print("Time: ");
      Serial.print(hours);
      Serial.print(":");
      Serial.print(minutes < 10 ? "0" : "");
      Serial.print(minutes);
      Serial.print(":");
      Serial.print(seconds < 10 ? "0" : "");
      Serial.println(seconds);
    }
  }
}

void handleButtonInput() {
  // Read the button state (LOW when pressed, HIGH when released)
  int reading = digitalRead(BUTTON_PIN);
  
  // Debounce the button
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }
  
  if ((millis() - lastDebounceTime) > debounceDelay) {
    // If the button state has changed
    if (reading != buttonState) {
      buttonState = reading;
      
      // Button pressed (LOW)
      if (buttonState == LOW) {
        buttonPressTime = millis();
        isLongPress = false;
      } 
      // Button released (HIGH)
      else {
        // Check if it was a long press
        if (isLongPress) {
          // Handle the completion of a long press
          handleLongPressComplete();
        } else {
          // It was a short press
          if (millis() - buttonPressTime < longPressTime) {
            handleShortPress();
          }
        }
      }
    }
  }
  
  // Check for ongoing long press
  if (buttonState == LOW && !isLongPress && (millis() - buttonPressTime > longPressTime)) {
    isLongPress = true;
    handleLongPress();
  }
  
  lastButtonState = reading;
}

void handleShortPress() {
  Serial.println("Short press detected");
  
  switch (currentState) {
    case NORMAL_DISPLAY:
      // Toggle alarm on/off
      alarmEnabled = !alarmEnabled;
      if (alarmEnabled) {
        Serial.println("Alarm enabled");
      } else {
        Serial.println("Alarm disabled");
        // Also turn off alarm if it's currently triggered
        if (alarmTriggered) {
          alarmTriggered = false;
        }
      }
      break;
      
    case SETTING_HOUR:
      // Increment hour
      hours = (hours + 1) % 24;
      timeInitialized = true;
      break;
      
    case SETTING_MINUTE:
      // Increment minute
      minutes = (minutes + 1) % 60;
      seconds = 0; // Reset seconds when setting minutes
      timeInitialized = true;
      break;
      
    case SETTING_ALARM_HOUR:
      // Increment alarm hour
      alarmHour = (alarmHour + 1) % 24;
      break;
      
    case SETTING_ALARM_MINUTE:
      // Increment alarm minute
      alarmMinute = (alarmMinute + 1) % 60;
      break;
  }
}

void handleLongPress() {
  Serial.println("Long press detected");
  
  // If alarm is triggered, disable it with long press
  if (alarmTriggered) {
    alarmTriggered = false;
    return;
  }
  
  // Otherwise, long press is for mode changing
  switch (currentState) {
    case NORMAL_DISPLAY:
      // Enter time setting mode
      currentState = SETTING_HOUR;
      Serial.println("Entering hour setting mode");
      break;
      
    // No action needed here since we handle mode changes in handleLongPressComplete
    default:
      break;
  }
}

void handleLongPressComplete() {
  Serial.println("Long press complete");
  
  switch (currentState) {
    case SETTING_HOUR:
      // Move to minute setting
      currentState = SETTING_MINUTE;
      Serial.println("Entering minute setting mode");
      break;
      
    case SETTING_MINUTE:
      // Move to alarm hour setting
      currentState = SETTING_ALARM_HOUR;
      Serial.println("Entering alarm hour setting mode");
      break;
      
    case SETTING_ALARM_HOUR:
      // Move to alarm minute setting
      currentState = SETTING_ALARM_MINUTE;
      Serial.println("Entering alarm minute setting mode");
      break;
      
    case SETTING_ALARM_MINUTE:
      // Return to normal display
      currentState = NORMAL_DISPLAY;
      Serial.println("Returning to normal display mode");
      // Save the last time we updated in manual mode
      lastSecond = millis();
      break;
      
    default:
      break;
  }
}

void checkAlarm() {
  // Check if alarm should be triggered
  if (alarmEnabled && !alarmTriggered && 
      hours == alarmHour && minutes == alarmMinute && seconds < 30) {
    alarmTriggered = true;
    alarmStartTime = millis();
    Serial.println("ALARM TRIGGERED!");
  }
  
  // Handle active alarm
  if (alarmTriggered) {
    // Auto-disable after duration expires
    if (millis() - alarmStartTime > alarmDuration) {
      alarmTriggered = false;
      Serial.println("Alarm automatically stopped after timeout");
    }
    
    // Update animation frame for alarm visuals
    if (millis() - lastAnimationUpdate > animationSpeed) {
      lastAnimationUpdate = millis();
      alarmAnimationFrame = (alarmAnimationFrame + 1) % 4; // 4 animation frames
    }
  }
}

void updateDisplay() {
  display.clearDisplay();
  
  if (alarmTriggered) {
    // Display intense visual alarm notification with animation
    displayAlarmNotification();
  } else {
    // Normal display
    displayNormalContent();
  }
  
  display.display();
}

void displayNormalContent() {
  // Show WiFi status and alarm status at the top
  display.setCursor(0, 0);
  if (WiFi.status() == WL_CONNECTED) {
    display.print("WiFi: OK");
  } else {
    display.print("WiFi: --");
  }
  
  // Show alarm status
  display.setCursor(70, 0);
  if (alarmEnabled) {
    display.print("Alarm: ON");
  } else {
    display.print("Alarm: OFF");
  }
  
  // Display current mode
  display.setCursor(0, 10);
  switch (currentState) {
    case NORMAL_DISPLAY:
      display.println("Time:");
      break;
      
    case SETTING_HOUR:
      display.println("Set Hour:");
      break;
      
    case SETTING_MINUTE:
      display.println("Set Minute:");
      break;
      
    case SETTING_ALARM_HOUR:
      display.println("Set Alarm Hour:");
      break;
      
    case SETTING_ALARM_MINUTE:
      display.println("Set Alarm Minute:");
      break;
  }
  
  // Display time in big digits in the center
  display.setTextSize(3);
  
  // Format hours and minutes with leading zeros
  char timeStr[9];
  sprintf(timeStr, "%02d:%02d:%02d", hours, minutes, seconds);
  
  int16_t x, y;
  uint16_t w, h;
  display.getTextBounds(timeStr, 0, 0, &x, &y, &w, &h);
  int centerX = (SCREEN_WIDTH - w) / 2;
  
  display.setCursor(centerX, 25);
  display.print(timeStr);
  
  // Display alarm time at the bottom
  display.setTextSize(1);
  display.setCursor(0, 56);
  
  char alarmStr[15];
  sprintf(alarmStr, "Alarm: %02d:%02d", alarmHour, alarmMinute);
  display.print(alarmStr);
  
  // Highlight the field being edited
  if (currentState != NORMAL_DISPLAY) {
    int highlightX = centerX;
    int highlightWidth = 36; // Width of each time component (HH/MM/SS)
    
    // Adjust highlight position based on the current setting mode
    if (currentState == SETTING_MINUTE || currentState == SETTING_ALARM_MINUTE) {
      highlightX += 36; // Move to minutes position
    }
    
    // Draw highlight rectangle
    if (currentState == SETTING_HOUR || currentState == SETTING_MINUTE) {
      display.drawRect(highlightX - 2, 22, highlightWidth, 30, SSD1306_WHITE);
    }
    
    // For alarm setting, highlight the alarm time at the bottom
    if (currentState == SETTING_ALARM_HOUR || currentState == SETTING_ALARM_MINUTE) {
      int alarmHighlightX = 42; // Starting X position for alarm hour
      
      if (currentState == SETTING_ALARM_MINUTE) {
        alarmHighlightX += 18; // Move to alarm minutes position
      }
      
      display.drawRect(alarmHighlightX, 55, 18, 10, SSD1306_WHITE);
    }
  }
}

void displayAlarmNotification() {
  // Create an eye-catching alarm display
  switch(alarmAnimationFrame) {
    case 0:
      // Inverted full screen flash
      display.fillScreen(SSD1306_WHITE);
      display.setTextColor(SSD1306_BLACK);
      break;
      
    case 1:
      // Normal screen with big text
      display.setTextColor(SSD1306_WHITE);
      break;
      
    case 2:
      // Checkered pattern
      for (int y = 0; y < SCREEN_HEIGHT; y += 8) {
        for (int x = 0; x < SCREEN_WIDTH; x += 8) {
          if ((x/8 + y/8) % 2 == 0) {
            display.fillRect(x, y, 8, 8, SSD1306_WHITE);
          }
        }
      }
      display.setTextColor((alarmAnimationFrame % 2) ? SSD1306_WHITE : SSD1306_BLACK);
      break;
      
    case 3:
      // Border flash
      display.drawRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SSD1306_WHITE);
      display.drawRect(2, 2, SCREEN_WIDTH-4, SCREEN_HEIGHT-4, SSD1306_WHITE);
      display.drawRect(4, 4, SCREEN_WIDTH-8, SCREEN_HEIGHT-8, SSD1306_WHITE);
      display.setTextColor(SSD1306_WHITE);
      break;
  }
  
  // Display alarm text
  display.setTextSize(2);
  display.setCursor(10, 5);
  display.println("ALARM!");
  
  // Show the time
  display.setTextSize(2);
  char timeStr[6];
  sprintf(timeStr, "%02d:%02d", hours, minutes);
  display.setCursor(25, 32);
  display.print(timeStr);
  
  // Instructions to dismiss
  display.setTextSize(1);
  display.setCursor(10, 55);
  display.print("Press button to stop");
  
  // Reset text color to default white
  display.setTextColor(SSD1306_WHITE);
}
