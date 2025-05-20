# Creating Schematics in Tinkercad for Microcontroller Labs

This guide provides detailed instructions for recreating the laboratory project circuits using Tinkercad's online circuit simulator.

## Table of Contents
- [Getting Started with Tinkercad](#getting-started-with-tinkercad)
- [Lab 5: Ultrasonic Distance Sensors](#lab-5-ultrasonic-distance-sensors)
- [Lab 6: Digitalization of Analog Signals](#lab-6-digitalization-of-analog-signals)
- [Lab 9: Examining WD Timer and Sleep Modes](#lab-9-examining-wd-timer-and-sleep-modes)
- [Limitations for Other Labs](#limitations-for-other-labs)
- [Tips for Better Schematics](#tips-for-better-schematics)

#### Connection Examples for Lab 6
1. **Temperature Sensor Middle Pin to A0**:
   - Click on the middle pin of the TMP36
   - Drag directly to the A0 pin on the Arduino
   - A single wire should connect them

2. **Photoresistor with Voltage Divider to A1**:
   - Connect one leg of photoresistor to 5V
   - Connect the other leg to the 10kΩ resistor
   - Connect the other end of the resistor to GND
   - **Creating the junction**: Click on the wire between the photoresistor and resistor
   - Drag from this junction to analog pin A1
   - A dot should appear at the T-junction

3. **Adding Multiple Components to Power Rails**:
   - Instead of individual wires to 5V and GND, create power rails on the breadboard
   - Connect Arduino 5V to the power rail once
   - Connect all components needing power to this rail
   - This reduces clutter and creates more reliable connections

## Lab 5: Ultrasonic Distance Sensors

### Components Required
- 1× Arduino board
- 1× HC-SR04 ultrasonic sensor
- 1× 7-segment display or LCD (optional)
- 7× 220Ω resistors (if using 7-segment display)

### Step-by-Step Schematic Creation
1. **Add Arduino**:
   - Place Arduino on workspace

2. **Add HC-SR04 sensor**:
   - Find HC-SR04 in component library (usually under "Sensor" category)
   - Place on breadboard
   - Connect VCC to Arduino 5V
   - Connect GND to Arduino GND
   - Connect Trig pin to Arduino pin 9
   - Connect Echo pin to Arduino pin 10

3. **Add 7-segment display (optional)**:
   - Place display on breadboard
   - Connect segments through 220Ω resistors to Arduino pins 2-8
   - Connect common pin to GND or VCC depending on type (common cathode/anode)

4. **Complete Working Code** (compatible with Tinkercad):
```cpp
// Complete code for Lab 5: Ultrasonic Distance Sensor with 7-segment display
// Pin definitions
const int trigPin = 9;
const int echoPin = 10;

// 7-segment display pins (common cathode)
const int segA = 2;
const int segB = 3;
const int segC = 4;
const int segD = 5;
const int segE = 6;
const int segF = 7;
const int segG = 8;

// Array for digits 0-9 on 7-segment display
byte seven_seg_digits[10][7] = {
  { 1,1,1,1,1,1,0 },  // = 0
  { 0,1,1,0,0,0,0 },  // = 1
  { 1,1,0,1,1,0,1 },  // = 2
  { 1,1,1,1,0,0,1 },  // = 3
  { 0,1,1,0,0,1,1 },  // = 4
  { 1,0,1,1,0,1,1 },  // = 5
  { 1,0,1,1,1,1,1 },  // = 6
  { 1,1,1,0,0,0,0 },  // = 7
  { 1,1,1,1,1,1,1 },  // = 8
  { 1,1,1,1,0,1,1 }   // = 9
};

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  
  // Configure ultrasonic sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  // Configure 7-segment display pins
  pinMode(segA, OUTPUT);
  pinMode(segB, OUTPUT);
  pinMode(segC, OUTPUT);
  pinMode(segD, OUTPUT);
  pinMode(segE, OUTPUT);
  pinMode(segF, OUTPUT);
  pinMode(segG, OUTPUT);
  
  // Initially clear the display
  clearDisplay();
}

void loop() {
  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Set trigPin HIGH for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);
  
  // Calculate distance
  int distance = duration * 0.034 / 2;
  
  // Print distance to Serial Monitor
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");
  
  // Display distance on 7-segment display (only showing single digit)
  if (distance <= 9) {
    displayDigit(distance);
  } else if (distance <= 99) {
    // For double digits, we would need two 7-segment displays
    // We'll just display the ones digit for this example
    displayDigit(distance % 10);
  } else {
    // Display "0" for out of range
    displayDigit(0);
  }
  
  delay(500);
}

// Function to display a digit on the 7-segment display
void displayDigit(int digit) {
  if (digit < 0 || digit > 9) {
    clearDisplay();
    return;
  }
  
  digitalWrite(segA, seven_seg_digits[digit][0]);
  digitalWrite(segB, seven_seg_digits[digit][1]);
  digitalWrite(segC, seven_seg_digits[digit][2]);
  digitalWrite(segD, seven_seg_digits[digit][3]);
  digitalWrite(segE, seven_seg_digits[digit][4]);
  digitalWrite(segF, seven_seg_digits[digit][5]);
  digitalWrite(segG, seven_seg_digits[digit][6]);
}

// Function to clear the display
void clearDisplay() {
  digitalWrite(segA, LOW);
  digitalWrite(segB, LOW);
  digitalWrite(segC, LOW);
  digitalWrite(segD, LOW);
  digitalWrite(segE, LOW);
  digitalWrite(segF, LOW);
  digitalWrite(segG, LOW);
}
```

## Lab 6: Digitalization of Analog Signals

### Components Required
- 1× Arduino board (Uno or Mega)
- 1× TMP36 temperature sensor (three-pin package)
- 1× Photoresistor (LDR) OR 1× Phototransistor (either component works)
- 1× 10kΩ resistor (for voltage divider)
- 1× Potentiometer (10kΩ)
- 1× LED with 220Ω resistor (for output indication)
- 1× Breadboard and connecting wires

### Step-by-Step Schematic Creation

1. **Add Arduino and breadboard**:
   - Place Arduino on the left side of the workspace
   - Place a breadboard to the right of the Arduino
   - Use red wires for power connections and black wires for ground

2. **Temperature sensor circuit (TMP36)**:
   - Find the TMP36 in the component library (may be under "Sensors" or "Temperature")
   - Place it on the breadboard with flat side facing left (pin orientation is critical)
   - Connect the pins as follows:
     * Left pin (pin 1) → Arduino 5V (red wire)
     * Middle pin (pin 2) → Arduino analog pin A0 (yellow wire)
     * Right pin (pin 3) → Arduino GND (black wire)
   - NOTE: If TMP36 isn't available, search for "temperature sensor" or use LM35

3. **Light sensor circuit (Photoresistor OR Phototransistor)**:
   - **For Photoresistor (LDR)**:
     * Place photoresistor on breadboard
     * Connect one leg to 5V (red wire)
     * Connect other leg to a 10kΩ resistor
     * Connect other end of resistor to GND (black wire)
     * Connect the junction between photoresistor and resistor to analog pin A1 (green wire)
   
4. **Potentiometer test circuit**:
   - Place 10kΩ potentiometer on breadboard
   - Connect left terminal to Arduino 5V (red wire)
   - Connect right terminal to Arduino GND (black wire)
   - Connect middle terminal (wiper) to Arduino analog pin A2 (blue wire)

5. **Add LED indicator**:
   - Place LED on breadboard (note the orientation - long leg is positive)
   - Connect LED anode (long leg) to a 220Ω resistor
   - Connect other end of resistor to Arduino digital pin 9
   - Connect LED cathode (short leg) to GND

### Reading Analog Values

1. **Understanding Voltage Dividers**:
   - For the photoresistor circuit, you've created a voltage divider
   - The voltage at the midpoint changes as the resistance changes
   - Formula: Vout = 5V × R2 / (R1 + R2)
   - Where R1 is the photoresistor and R2 is the fixed resistor

2. **Converting Analog Readings**:
   - ADC reading (0-1023) → Voltage: voltage = reading * (5.0 / 1023.0)
   - TMP36: temperature in °C = (voltage - 0.5) * 100
   - Photoresistor: light level is inversely proportional to resistance

3. **Complete Working Code** (compatible with Tinkercad):
```cpp
// Complete code for Lab 6: Analog Sensors with LED Indicator
// Pin definitions
const int tempSensorPin = A0;  // TMP36 temperature sensor
const int lightSensorPin = A1; // Photoresistor or phototransistor
const int potentiometerPin = A2; // Potentiometer
const int ledPin = 9;          // LED for visual output

// Global variables
unsigned long previousMillis = 0;
const long interval = 200;     // 200ms = 5 readings per second

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  
  Serial.println("Lab 6: Analog Sensor Readings");
  Serial.println("-----------------------------");
  Serial.println("Format: Temperature(°C), Light(%), Potentiometer");
  delay(1000);
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    // Read sensor values
    int tempRaw = analogRead(tempSensorPin);
    int lightRaw = analogRead(lightSensorPin);
    int potRaw = analogRead(potentiometerPin);
    
    // Convert TMP36 reading to temperature
    float voltage = tempRaw * (5.0 / 1023.0);
    float temperatureC = (voltage - 0.5) * 100;
    
    // Map light sensor value to percentage (0-100%)
    int lightPercent = map(lightRaw, 0, 1023, 0, 100);
    
    // Control LED brightness based on light level
    // If light is low (dark), LED will be bright and vice versa
    int ledBrightness = map(lightRaw, 0, 1023, 255, 0);
    analogWrite(ledPin, ledBrightness);
    
    // Print formatted data for serial monitor
    Serial.print("Temperature: ");
    Serial.print(temperatureC, 1);
    Serial.print("°C | Light: ");
    Serial.print(lightPercent);
    Serial.print("% (");
    Serial.print(lightRaw * (5.0 / 1023.0), 2);
    Serial.print("V) | Pot: ");
    Serial.print(potRaw);
    Serial.print(" (");
    Serial.print(potRaw * (5.0 / 1023.0), 2);
    Serial.println("V)");
    
    // Data for Serial Plotter (comma separated values)
    Serial.print(temperatureC);
    Serial.print(",");
    Serial.print(lightPercent);
    Serial.print(",");
    Serial.println(potRaw / 10.23); // Scale to approximately match other values
  }
}
```

## Lab 9: Examining WD Timer and Sleep Modes

### Components Required
- 1× Arduino board
- 1× LED with 220Ω resistor
- 1× Push button with 10kΩ pull-up resistor
- 1× Breadboard and connecting wires

### Step-by-Step Schematic Creation
1. **Add Arduino and breadboard**:
   - Place Arduino on workspace
   - Place breadboard next to it

2. **Add LED indicator circuit**:
   - Place LED on breadboard (note orientation - long leg is positive)
   - Connect LED anode (long leg) to a 220Ω resistor
   - Connect other end of resistor to Arduino digital pin 13
   - Connect LED cathode (short leg) to GND

3. **Add button for wake-up test**:
   - Place push button on breadboard
   - Connect one side to GND
   - Connect other side to Arduino pin 2 and to 5V through a 10kΩ resistor (pull-up)

4. **Working Code** (compatible with Tinkercad):
```cpp
// Lab 9: Watchdog Timer and Sleep Modes
// Note: Tinkercad doesn't fully support sleep modes but this demonstrates the concept

#include <avr/sleep.h>
#include <EEPROM.h>

const int ledPin = 13;
const int wakePin = 2;     // Use pin 2 for wake-up interrupt
volatile boolean awakened = false;
int bootCount = 0;         // Counter to track wake-up cycles

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  pinMode(wakePin, INPUT_PULLUP);
  
  // Read boot count from EEPROM
  bootCount = EEPROM.read(0);
  bootCount++;
  
  // Write updated boot count back to EEPROM
  EEPROM.write(0, bootCount);
  
  Serial.print("System started. Boot count: ");
  Serial.println(bootCount);
  Serial.println("Press button to simulate wake-up from sleep.");
  
  // Blink LED to show system is active
  for(int i = 0; i < 3; i++) {
    digitalWrite(ledPin, HIGH);
    delay(200);
    digitalWrite(ledPin, LOW);
    delay(200);
  }
  
  // Attach interrupt for wake-up button
  attachInterrupt(digitalPinToInterrupt(wakePin), wakeUp, FALLING);
}

void loop() {
  // Only in real hardware: if no activity for 5 seconds, go to sleep
  if (millis() > 5000 && !awakened) {
    Serial.println("Going to sleep now...");
    delay(200);  // Allow serial to complete
    
    // In real hardware: sleepNow();
    // In Tinkercad, we'll just simulate sleep with LED
    digitalWrite(ledPin, LOW);
    
    // Wait for button press (simulating sleep)
    while(!awakened) {
      // In real hardware this wouldn't execute - processor would be sleeping
      delay(100);
    }
    
    // Wake-up routine
    Serial.println("Waking up!");
    awakened = false;
    
    // Activity after wake-up
    for(int i = 0; i < 5; i++) {
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      delay(100);
    }
  }
  
  // Normal operation - LED breathing effect
  for (int brightness = 0; brightness < 255; brightness++) {
    analogWrite(ledPin, brightness);
    delay(5);
  }
  for (int brightness = 255; brightness >= 0; brightness--) {
    analogWrite(ledPin, brightness);
    delay(5);
  }
}

// Interrupt service routine for wake-up
void wakeUp() {
  awakened = true;
}

// Function for real hardware - not fully functional in Tinkercad
void sleepNow() {
  // Set sleep mode
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  
  // Enter sleep mode
  sleep_mode();
  
  // After waking up, execution continues from here
  sleep_disable();
}
```

## Lab 10: Controller chip SSD1306 (using LCD as alternative)

Since Tinkercad lacks support for SSD1306 OLED displays, we'll use the available LCD display as an alternative to demonstrate the concept.

### Components Required
- 1× Arduino board
- 1× 16x2 LCD display
- 1× 10kΩ potentiometer (for LCD contrast)
- 1× Breadboard and connecting wires

### Step-by-Step Schematic Creation
1. **Add Arduino and breadboard**:
   - Place Arduino on workspace
   - Place breadboard next to it

2. **Add LCD display**:
   - Place 16x2 LCD on breadboard
   - Connect LCD pins:
     * VSS (Pin 1) → GND
     * VDD (Pin 2) → 5V
     * V0 (Pin 3) → Middle pin of potentiometer (for contrast)
     * RS (Pin 4) → Arduino pin 12
     * RW (Pin 5) → GND
     * E (Pin 6) → Arduino pin 11
     * D4 (Pin 11) → Arduino pin 5
     * D5 (Pin 12) → Arduino pin 4
     * D6 (Pin 13) → Arduino pin 3
     * D7 (Pin 14) → Arduino pin 2
     * LED+ (Pin 15) → 5V (or through a resistor if needed)
     * LED- (Pin 16) → GND

3. **Add potentiometer for contrast**:
   - Connect left pin to 5V
   - Connect right pin to GND
   - Connect middle pin to LCD V0 (Pin 3)

4. **Working Code** (compatible with Tinkercad):
```cpp
// Lab 10: Display Control (LCD instead of SSD1306)
#include <LiquidCrystal.h>

// Initialize the LCD with interface pins
// (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Custom character for animation
byte customChar[8] = {
  0b00000,
  0b00000,
  0b01010,
  0b00000,
  0b10001,
  0b01110,
  0b00000,
  0b00000
};

byte customChar2[8] = {
  0b00000,
  0b00000,
  0b01010,
  0b00000,
  0b00000,
  0b01110,
  0b10001,
  0b00000
};

unsigned long previousMillis = 0;
const long interval = 500;  // Animation update interval
int animationFrame = 0;
int position = 0;

void setup() {
  // Set up the LCD's number of columns and rows
  lcd.begin(16, 2);
  
  // Create custom characters
  lcd.createChar(0, customChar);
  lcd.createChar(1, customChar2);
  
  // Display welcome message
  lcd.setCursor(0, 0);
  lcd.print("LCD Demo");
  lcd.setCursor(0, 1);
  lcd.print("Lab 10 Alt");
  delay(2000);
  
  // Clear the screen
  lcd.clear();
}

void loop() {
  unsigned long currentMillis = millis();
  
  // Update animation
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    // Clear the display
    lcd.clear();
    
    // Elapsed time
    lcd.setCursor(0, 0);
    lcd.print("Time: ");
    lcd.print(currentMillis / 1000);
    lcd.print("s");
    
    // Animated character
    lcd.setCursor(position, 1);
    lcd.write(animationFrame);
    
    // Alternate animation frames
    animationFrame = 1 - animationFrame;
    
    // Move position
    position++;
    if (position >= 16) {
      position = 0;
    }
  }
  
  // Temperature simulation (you could connect a real sensor from Lab 6)
  if (currentMillis % 3000 == 0) {  // Every 3 seconds
    int simulatedTemp = random(20, 30);
    lcd.setCursor(10, 0);
    lcd.print(simulatedTemp);
    lcd.print("C");
  }
}
```

## Lab 11: WS2812B Digital LED (NeoPixel)

### Components Required
- 1× Arduino board
- 1× NeoPixel strip (8 LEDs)
- 1× 470Ω resistor for data line
- 1× 1000μF capacitor (optional, between power and ground)
- 1× Breadboard and connecting wires

### Step-by-Step Schematic Creation
1. **Add Arduino and breadboard**:
   - Place Arduino on workspace
   - Place breadboard next to it

2. **Add NeoPixel strip**:
   - Find "Neopixel Strip" in component library (or "WS2812")
   - Place on breadboard
   - Connect GND to Arduino GND
   - Connect 5V or VCC to Arduino 5V 
   - Add 470Ω resistor between Arduino pin 6 and the NeoPixel data input
   - Optionally add 1000μF capacitor between 5V and GND for power stabilization

3. **Working Code** (compatible with Tinkercad):
```cpp
// Lab 11: WS2812B Digital LED (NeoPixel)
#include <Adafruit_NeoPixel.h>

#define PIN            6  // Data pin for NeoPixel strip
#define NUMPIXELS      8  // Number of LEDs in strip
#define BRIGHTNESS    50  // Set brightness (0-255)

// Initialize NeoPixel strip
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// Animation variables
int mode = 0;  // Animation mode
unsigned long lastModeChange = 0;
unsigned long previousMillis = 0;
int animationStep = 0;

void setup() {
  pixels.begin();
  pixels.setBrightness(BRIGHTNESS);
  pixels.show();  // Initialize all pixels to 'off'
  
  Serial.begin(9600);
  Serial.println("WS2812B (NeoPixel) Demo");
  Serial.println("Press 1, 2, 3 or 4 to change animation mode");
}

void loop() {
  // Check for serial input to change modes
  if (Serial.available() > 0) {
    char input = Serial.read();
    if (input >= '1' && input <= '4') {
      mode = input - '1';
      animationStep = 0;
      Serial.print("Mode changed to: ");
      Serial.println(mode);
    }
  }
  
  // Auto-change mode every 10 seconds
  if (millis() - lastModeChange > 10000) {
    mode = (mode + 1) % 4;
    animationStep = 0;
    lastModeChange = millis();
    Serial.print("Auto mode change to: ");
    Serial.println(mode);
  }
  
  // Update animation based on current mode
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= 30) {  // Animation speed
    previousMillis = currentMillis;
    
    switch(mode) {
      case 0:
        rainbow(animationStep);
        animationStep = (animationStep + 1) % 256;
        break;
      case 1:
        colorWipe(animationStep);
        animationStep = (animationStep + 1) % (NUMPIXELS * 3);
        break;
      case 2:
        theaterChase(animationStep);
        animationStep = (animationStep + 1) % 6;
        break;
      case 3:
        breathe(animationStep);
        animationStep = (animationStep + 1) % 512;
        break;
    }
  }
}

// Rainbow cycle animation
void rainbow(int cycleStep) {
  for (int i = 0; i < pixels.numPixels(); i++) {
    int pixelHue = (i * 256 / pixels.numPixels() + cycleStep) & 255;
    pixels.setPixelColor(i, colorWheel(pixelHue));
  }
  pixels.show();
}

// Color wipe animation
void colorWipe(int step) {
  pixels.clear();
  int color = step / NUMPIXELS;
  int pos = step % NUMPIXELS;
  
  for (int i = 0; i <= pos; i++) {
    switch(color) {
      case 0: // Red
        pixels.setPixelColor(i, pixels.Color(255, 0, 0));
        break;
      case 1: // Green
        pixels.setPixelColor(i, pixels.Color(0, 255, 0));
        break;
      case 2: // Blue
        pixels.setPixelColor(i, pixels.Color(0, 0, 255));
        break;
    }
  }
  pixels.show();
}

// Theater chase animation
void theaterChase(int step) {
  pixels.clear();
  int on = step % 3;
  int color = step / 3;
  
  for (int i = 0; i < pixels.numPixels(); i += 3) {
    uint32_t pixelColor;
    switch(color) {
      case 0: pixelColor = pixels.Color(255, 0, 0); break;
      case 1: pixelColor = pixels.Color(0, 255, 0); break;
    }
    pixels.setPixelColor(i + on, pixelColor);
  }
  pixels.show();
}

// Breathing effect
void breathe(int step) {
  int brightness;
  if (step < 256) {
    brightness = step;  // Increasing brightness
  } else {
    brightness = 511 - step;  // Decreasing brightness
  }
  
  for (int i = 0; i < pixels.numPixels(); i++) {
    // Calculate color with adjusted brightness
    uint32_t color = pixels.Color(
      (brightness * 64) / 255,  // Reddish
      (brightness * 20) / 255,  // hint of green
      (brightness * 100) / 255   // more blue
    );
    pixels.setPixelColor(i, color);
  }
  pixels.show();
}

// Helper function to create color wheel
uint32_t colorWheel(byte pos) {
  pos = 255 - pos;
  if (pos < 85) {
    return pixels.Color(255 - pos * 3, 0, pos * 3);
  } else if (pos < 170) {
    pos -= 85;
    return pixels.Color(0, pos * 3, 255 - pos * 3);
  } else {
    pos -= 170;
    return pixels.Color(pos * 3, 255 - pos * 3, 0);
  }
}
```

## Bonus: Adding IR Remote Control to Labs

You can enhance your lab projects using the IRremote library available in Tinkercad.

### Components Required
- 1× Arduino board
- 1× IR receiver module
- 1× IR remote control
- Components from the lab you want to control
- Breadboard and connecting wires

### Step-by-Step Schematic Addition
1. **Add IR Receiver**:
   - Place IR Receiver on breadboard
   - Connect VCC to 5V, GND to GND
   - Connect output pin to Arduino pin 11

2. **Example Code for IR Control of LED Brightness**:
```cpp
// IR Remote Control example for Arduino labs
#include <IRremote.h>

#define IR_RECEIVE_PIN 11
#define LED_PIN 9

// IR remote control button codes (example values - may differ with your remote)
#define IR_UP    0xFF629D
#define IR_DOWN  0xFFA857
#define IR_LEFT  0xFF22DD
#define IR_RIGHT 0xFFC23D
#define IR_OK    0xFF02FD

int brightness = 127;  // Initial LED brightness (0-255)

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  
  // Initialize IR receiver
  IrReceiver.begin(IR_RECEIVE_PIN);
  
  Serial.println("IR Remote Control Ready");
  Serial.println("Use UP/DOWN to control brightness");
}

void loop() {
  // Check for IR signals
  if (IrReceiver.decode()) {
    unsigned long irCode = IrReceiver.decodedIRData.decodedRawData;
    
    // Process based on button pressed
    switch(irCode) {
      case IR_UP:
        brightness = min(255, brightness + 25);
        Serial.print("Brightness UP: ");
        Serial.println(brightness);
        break;
        
      case IR_DOWN:
        brightness = max(0, brightness - 25);
        Serial.print("Brightness DOWN: ");
        Serial.println(brightness);
        break;
        
      case IR_OK:
        // Toggle between full on/off
        brightness = (brightness > 0) ? 0 : 255;
        Serial.print("Toggle: ");
        Serial.println(brightness);
        break;
    }
    
    // Update LED brightness
    analogWrite(LED_PIN, brightness);
    
    // Prepare for next code
    IrReceiver.resume();
  }
  
  // Put other lab code here
  delay(10);
}
```

## Bonus: Using LiquidCrystal to Display Sensor Data

This example shows how to integrate an LCD display with Lab 6 (Analog Sensors).

### Components Required
- All components from Lab 6
- 1× 16x2 LCD display
- 1× 10kΩ potentiometer (for LCD contrast)
- Additional connecting wires

### Example Code
```cpp
#include <LiquidCrystal.h>

// Initialize LCD (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Sensor pins
const int tempSensorPin = A0;  // TMP36 temperature sensor
const int lightSensorPin = A1; // Photoresistor
const int ledPin = 9;          // LED for visual output

unsigned long previousMillis = 0;
const long interval = 500;     // Update interval

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  
  // Initialize LCD
  lcd.begin(16, 2);
  lcd.print("Sensor Readings:");
  
  Serial.println("Lab 6 with LCD Display");
}

void loop() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    // Read sensor values
    int tempRaw = analogRead(tempSensorPin);
    int lightRaw = analogRead(lightSensorPin);
    
    // Convert TMP36 reading to temperature
    float voltage = tempRaw * (5.0 / 1023.0);
    float temperatureC = (voltage - 0.5) * 100;
    
    // Map light sensor value to percentage
    int lightPercent = map(lightRaw, 0, 1023, 0, 100);
    
    // Control LED brightness based on light level
    int ledBrightness = map(lightRaw, 0, 1023, 255, 0);
    analogWrite(ledPin, ledBrightness);
    
    // Update LCD
    lcd.setCursor(0, 1);
    lcd.print("Temp:");
    lcd.print(temperatureC, 1);
    lcd.print("C ");
    lcd.print("L:");
    lcd.print(lightPercent);
    lcd.print("%  ");
    
    // Output to Serial Monitor too
    Serial.print("Temperature: ");
    Serial.print(temperatureC);
    Serial.print("°C, Light: ");
    Serial.print(lightPercent);
    Serial.println("%");
  }
}
```

## Limitations for Other Labs

### Labs with Library Dependencies (Not Fully Supported in Tinkercad)

Tinkercad has limited support for external libraries. The following labs require specialized libraries that are difficult to use in Tinkercad:

#### Lab 10: Controller Chip SSD1306
- **Required libraries**: Adafruit_GFX, Adafruit_SSD1306
- **Limitation**: These libraries aren't built into Tinkercad
- **Alternative**: You can create a schematic showing the I2C connections (SDA to A4, SCL to A5), but the full functionality can't be simulated

#### Lab 11: WS2812B Digital LED
- **Required library**: Adafruit_NeoPixel
- **Limitation**: This library isn't built into Tinkercad
- **Alternative**: You can create a simple LED circuit instead to represent the concept

### Other Labs with Technical Limitations

#### Lab 1: Fundamentals of oscillograph use
- While Tinkercad has a simulated oscilloscope, the hands-on tuning experience is limited.
- You can generate simple waveforms with the function generator and observe them with the oscilloscope tool.

#### Lab 7: Study of radio module NRF24L01
- NRF24L01 modules are not available in Tinkercad.
- You can create a schematic showing pin connections to Arduino, but cannot simulate RF communication.

#### Lab 8: Ethernet Internet Module
- Ethernet shields aren't standard in Tinkercad.
- You can show basic connections but network functionality cannot be simulated.

#### Lab 9: Examining WD timer and sleep modes
- These are primarily software features with minimal hardware representation.
- You can create a basic circuit with an LED to indicate wake-up events.

## Tips for Better Schematics

1. **Organizing Your Circuit**:
   - Group related components together
   - Maintain a left-to-right signal flow where possible
   - Keep power and ground connections clean and organized

2. **Color Coding**:
   - Red for positive voltage (5V, 3.3V)
   - Black for ground
   - Yellow for I2C connections
   - Green or blue for signal lines
   - Orange for SPI connections

3. **Documentation**:
   - Add text notes to explain circuit sections
   - Create a bill of materials list
   - Add voltage/current measurements where critical

4. **Saving and Sharing**:
   - Save frequently using descriptive names
   - Use "Download as Image" for reports
   - Use "Share link" for submitting assignments
   - Create distinct circuits for each lab rather than one large project

5. **Testing and Debugging**:
   - Simulate frequently to catch errors early
   - Use the multimeter to check voltage and current
   - Use the oscilloscope to visualize signals
   - Break complex circuits into functional blocks and test each separately
